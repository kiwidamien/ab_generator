# pylint: disable=E0401, C0103, C301
from datetime import timedelta, datetime
from collections import namedtuple
import random

from faker import Faker

fake = Faker()

TrackedVisit = namedtuple('TrackedVisit', 'experiment date_visit user_agent variation success device')

class user:
    user_names = {}

    def __init__(self, segment, sex=None, experiment_start=datetime(1900, 1, 1)):
        self.user_info = fake.simple_profile(sex)
        while self.user_info['username'] in user.user_names:
            self.user_info = fake.simple_profile(sex)
            print(f'collision! Have {len(user.user_names)} names')
        user.user_names[self.user_info['username']] = True
        self.user_info['default_user_agent'] = fake.user_agent()
        self.segment = segment
        self.variation = 'control'

        self.ctr_rate = {}
        for device in segment.ctr:
            self.ctr_rate[device] = {
                'control': segment.ctr[device]['control'].rvs(),
                'variation': segment.ctr[device]['variation'].rvs()
            }
        self.actual_rates = {device: self.ctr_rate[device][self.variation] for device in self.ctr_rate}
        self.experiment_start = experiment_start

    def __str__(self):
        return f'''
        username: {self.user_info['username']}
        gender: {self.user_info['sex']}
        default browser: {self.user_info['default_user_agent']}
        segment: {self.segment.name}
        '''

    def assign_to_variation(self, is_control):
        if is_control:
            self.variation = 'control'
        else:
            self.variation = 'variation'
        self.actual_rate = {device: self.ctr_rate[device][self.variation] for device in self.ctr_rate}

    def generate_single_visit(self, the_datetime, device_type='desktop'):
        the_date = the_datetime + timedelta(seconds=random.randint(0, 3599))
        variation = self.variation

        if the_datetime < self.experiment_start:
            variation = 'control'

        actual_rate = self.ctr_rate[device_type][variation]
        success = (random.random() < actual_rate)

        return TrackedVisit(experiment='so_many_shoes', date_visit=the_date,
                            user_agent=f'{self.user_info["default_user_agent"]}',
                            device=device_type,
                            variation=variation, success=success)

    def generate_visits_in_hour(self, the_datetime, device=None):
        """stuff"""
        # Need a
        # * URL List
        # * A way to adjust hourly segments based on time and day of week
        # * either the function to generate the success probability from OR
        #   the result of the die roll. Think about which makes more sense
        num_visits = self.segment.num_visits_in_hour(the_datetime)
        if device is None:
            device = 'desktop'
        return [self.generate_single_visit(the_datetime, device) for _ in range(num_visits)]

    def generate_visits_between(self, start_time, end_time, device=None):
        if start_time > end_time:
            raise ValueError('Cannot start generating visits after end time.')

        current_time = start_time
        visits = []
        while current_time < end_time:
            visits.extend(self.generate_visits_in_hour(current_time, device))
            current_time += timedelta(hours=1)

        return visits

if __name__ == '__main__':
    from hour_functions import make_humpday_daytime_power_user
    from population_segment import PopulationSegment

    segment1 = PopulationSegment('default')
    segment2 = PopulationSegment('power_users',
                                 hr_visit_rate_func=make_humpday_daytime_power_user(2))

    for _ in range(4):
        my_user = user(segment1)
    print(my_user)
    start_time = datetime(2018, 1, 1)
    end_time = datetime(2018, 1, 7)
    my_user.assign_to_variation(False)
    for visit in my_user.generate_visits_between(start_time, end_time):
        print(visit)
