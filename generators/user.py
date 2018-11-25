# pylint: disable=E0401, C0103
from datetime import timedelta
import random

from faker import Faker

fake = Faker()

TrackedVisit = namedtuple('TrackedVisit', 'experiment date_visit user_agent variation success device')

class user:
    def __init__(self, segment, sex=None):
        self.user_info = fake.simple_profile(sex)
        self.user_info['default_user_agent'] = fake.user_agent()
        self.segment = segment
        self.variation = 'control'
        self.ctr_rate = {
            'control': segment.ctr_control.rvs(),
            'variation': segment.ctr_variation.rvs()
        }
        self.actual_rate = self.ctr_rate[self.variation]

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
        self.actual_rate = self.ctr_rate[self.variation]

    def generate_single_visit(self, the_datetime, device_type='desktop'):
        the_date = the_datetime + timedelta(seconds=random.randint(0, 3599))
        success = (random.random() < self.actual_rate)

        return TrackedVisit(experiment='so_many_shoes', date_visit=the_date,
                            user_agent=f'{self.user_info["default_user_agent"]}',
                            device=device_type,
                            variation=self.variation, success=success)

    def generate_visits_in_hour(self, the_datetime, device=None):
        """stuff"""
        # Need a
        # * URL List
        # * A way to adjust hourly segments based on time and day of week
        # * either the function to generate the success probability from OR
        #   the result of the die roll. Think about which makes more sense
        num_visits = self.segment.num_visits_in_hour(the_datetime)
        if device is None:
            device='desktop'
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
