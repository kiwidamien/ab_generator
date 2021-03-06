"""
Make a very simple generator for users and page views with only two variations.

The idea is to see what we need to make, and then generalize with the appropriate parameters.

This is supposed to be somewhat ugly and hardcoded

Big Questions:
* Should we include signup dates?
* Should we include data from before the experiment started
    (i.e. see how users behaved before and after)
* Should we have uses join in the experiment?
"""

# Population
# ----------
# We will have several different segments of the population. Each of those segments will
# respond differently to the control and variation. Each user will be assigned to a segment
# based on his or her features.

from collections import namedtuple
from datetime import timedelta
import random
import numpy as np

from scipy.stats import beta, poisson
from scipy.stats import dirichlet

from dateutil import parser
from faker import Faker

fake = Faker()

segment = namedtuple('segment', 'name hourly_visit_rate ctr_control_beta ctr_variation_beta')
tracked_visit = namedtuple('tracked_visit', 'experiment date_visit user_agent variation success')

POPULATIONS = [
    segment(name='A', hourly_visit_rate=3/168, ctr_control_beta=beta(10, 100),
            ctr_variation_beta=beta(15, 100)),
    segment(name='B', hourly_visit_rate=12/168, ctr_control_beta=beta(20, 100),
            ctr_variation_beta=beta(30, 100)),
    segment(name='C', hourly_visit_rate=15/168, ctr_control_beta=beta(5, 100),
            ctr_variation_beta=beta(8, 100)),
    segment(name='D', hourly_visit_rate=30/168, ctr_control_beta=beta(7, 100),
            ctr_variation_beta=beta(11, 100))
]

class user:
    def __init__(self, sex=None):
        self.user_info = fake.simple_profile(sex)
        self.user_info['default_user_agent']=fake.user_agent()
        self.segment = None
        self.actual_rate = None
        self.variation = None
        self.ctr_rate = [None, None]

    def __str__(self):
        return f'''
        username: {self.user_info['username']}
        gender: {self.user_info['sex']}
        default browser: {self.user_info['default_user_agent']}
        '''

    def assign_to_segment(self, the_segment):
        """Some docstring"""
        self.segment = the_segment
        self.ctr_rate[0] = the_segment.ctr_control_beta.rvs()
        self.ctr_rate[1] = the_segment.ctr_variation_beta.rvs()

    def assign_to_variation(self, is_control):
        """Assigns to variation"""
        if not self.segment:
            raise ValueError('Assign user to segment before assigning to variation')

        if is_control:
            self.actual_rate = self.ctr_rate[0]
            self.variation = 'control'
        else:
            self.actual_rate = self.ctr_rate[1]
            self.variation = 'variation'

    def generate_single_visit(self, the_datetime):
        """stuff"""

        the_date = the_datetime + timedelta(seconds=random.randint(0, 3599))
        success = (random.random() < self.actual_rate)

        return tracked_visit(experiment='so_many_shoes', date_visit=the_date,
                             user_agent=f'{self.user_info["default_user_agent"]}',
                             variation=self.variation, success=success)

    def generate_visits_in_hour(self, the_datetime):
        """stuff"""
        # Need a
        # * URL List
        # * A way to adjust hourly segments based on time and day of week
        # * either the function to generate the success probability from OR
        #   the result of the die roll. Think about which makes more sense
        num_visits = poisson(self.segment.hourly_visit_rate).rvs()
        return [self.generate_single_visit(the_datetime) for _ in range(num_visits)]

    def generate_visits_between(self, start_time, end_time):
        if start_time > end_time:
            raise ValueError('Cannot start generating visits after end time.')

        current_time = start_time
        visits = []
        while current_time < end_time:
            visits.extend(self.generate_visits_in_hour(current_time))
            current_time += timedelta(hours=1)

        return visits

###
# This function should be rewritten per experiment -- it is how we are segmenting people
# into populations
def assign_user_to_pop(the_user, populations):
    base = np.array([1,1,1,1])
    if the_user.user_info['sex'] == 'M':
        base[2] += 10
    index = np.random.choice(range(len(base)), p=dirichlet(base).rvs().reshape(-1,))
    return 'ABCD'[int(index)]

my_user = user()
print(my_user)
print(assign_user_to_pop(my_user, POPULATIONS))

my_user.assign_to_segment(POPULATIONS[0])
my_user.assign_to_variation(is_control=False)
print(POPULATIONS[0].ctr_control_beta.rvs())

start_time = parser.parse('2018-01-05 8:00')
end_time = parser.parse('2018-01-07 9:00')

print(len(my_user.generate_visits_between(start_time, end_time)))
