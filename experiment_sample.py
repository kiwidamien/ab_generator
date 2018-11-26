"""
Generators a sample experiment
"""

from generators.user import user, TrackedVisit
from generators.population_segment import PopulationSegment
from generators.hour_functions import *

import random
import datetime
import os

# Make a difference between men and women.
# Women have higher purchase rate overall
# Men are more affected by the variation, but the effect is smaller on mobile devices
# Tablets are rare, but have the opposite effect (control is better)
#

MEN1_DESKTOP = {
    'beta_params': {
        'desktop': {'control': (10, 100), 'variation': (23, 200)},
        'mobile': {'control': (9, 100), 'variation': (8.3, 100)},
        'tablet': {'control': (8, 100), 'variation': (6, 100)}
    },
    'hr_visit_rate_func': make_humpday_daytime_power_user(6/168),
    'name': 'men_midweek_user',
    'device_params': {
        'mobile': 8,
        'desktop': 25,
        'tablet': 1
    }
}

WOMEN1_DESKTOP = {
    'beta_params': {
        'desktop': {'control': (12, 100), 'variation': (19, 140)},
        'mobile': {'control': (11, 100), 'variation': (10, 100)},
        'tablet': {'control': (4, 100), 'variation': (1, 100)}
    },
    'hr_visit_rate_func': make_humpday_daytime_power_user(5/168),
    'name': 'women_midweek_user',
    'device_params': {
        'mobile': 10,
        'desktop': 35,
        'tablet': 1
    }
}

MEN_WEEKEND_MIX = {
    'beta_params': {
        'desktop': {'control': (8, 100), 'variation': (20, 220)},
        'mobile': {'control': (8, 100), 'variation': (7.2, 100)},
        'tablet': {'control': (8, 100), 'variation': (8, 100)}
    },
    'hr_visit_rate_func': make_weekend_power_user(11/168),
    'name': 'men_weekend_user_mixed_usage',
    'device_params': {
        'mobile': 25,
        'desktop': 25,
        'tablet': 1
    }
}

WOMEN_WEEKEND_MIX = {
    'beta_params': {
        'desktop': {'control': (11, 100), 'variation': (35, 300)},
        'mobile': {'control': (11, 100), 'variation': (19, 200)},
        'tablet': {'control': (12, 100), 'variation': (8, 100)}
    },
    'hr_visit_rate_func': make_weekend_power_user(10/168),
    'name': 'women_weekend_user_mixed_usage',
    'device_params': {
        'mobile': 35,
        'desktop': 22,
        'tablet': 1
    }
}

GENERIC_USER = {
    'beta_params': {
        'desktop': {'control': (6, 100), 'variation': (14, 200)},
        'mobile': {'control': (7, 100), 'variation': (6, 100)},
        'tablet': {'control': (6, 100), 'variation': (3, 100)}
    },
    'hr_visit_rate_func': make_humpday_evening_power_user(4/168),
    'name': 'generic_user_low_ctr',
    'device_params': {
        'mobile': 5,
        'desktop': 8,
        'tablet': 1
    }
}

MEN1_DESKTOP_SEGMENT = PopulationSegment(**MEN1_DESKTOP)
MEN_WEEKEND_MIX_SEGMENT = PopulationSegment(**MEN_WEEKEND_MIX)
WOMEN1_DESKTOP_SEGMENT = PopulationSegment(**WOMEN1_DESKTOP)
WOMEN_WEEKEND_MIX_SEGMENT = PopulationSegment(**WOMEN_WEEKEND_MIX)
GENERIC_USER = PopulationSegment(**GENERIC_USER)

NUM_USERS = 15000
FRAC_WOMEN = 0.6

experiment_start = datetime.datetime(2018,10,1)
record_start = datetime.datetime(2018, 9, 24)
record_end = datetime.datetime(2018, 11, 5)

user_list = []

for _ in range(NUM_USERS):
    if random.random() < 0.6:
        gender = 'F'
    else:
        gender = 'M'
    segment = None
    if random.random() < 0.1:
        segment = GENERIC_USER
    else:
        if gender == 'M':
            if random.random() < 0.75:
                segment = MEN1_DESKTOP_SEGMENT
            else:
                segment = MEN_WEEKEND_MIX_SEGMENT
        else:
            if random.random() < 0.6:
                segment = WOMEN_WEEKEND_MIX_SEGMENT
            else:
                segment = WOMEN1_DESKTOP_SEGMENT

    # Assign 50% of users to the variation
    new_user = user(segment, gender, experiment_start=experiment_start)
    new_user.assign_to_variation(random.random() < 0.5)

    user_list.append(new_user)

def format_visit(visit, user):
    output = f'{user.user_info["username"]},{visit.experiment},{visit.date_visit},{visit.device},{visit.variation},{visit.success}'
    return output

def write_visits(the_user, filename):
    with open(filename, 'a') as file:
        visit_records = [format_visit(visit, the_user) for visit in the_user.generate_visits_between(record_start, record_end)]
        if len(visit_records) == 0:
            return
        record='\n'.join(visit_records)
        file.write(record+'\n')

def write_user(the_user, filename_public, filename_private):
    with open(filename_public, 'a') as file:
        file.write(the_user.write_line_public()+'\n')
    with open(filename_private, 'a') as file:
        file.write(the_user.write_line_private()+'\n')

for file in ['visits.csv', 'user_public.csv', 'user_private.csv']:
    try:
        os.remove(file)
    except:
        print(f'{file:12s} does not need to be removed')

for the_user in user_list:
    write_visits(the_user, 'visits.csv')
    write_user(the_user, 'user_public.csv', 'user_private.csv')
