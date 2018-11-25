from scipy.stats import beta, poisson, dirichlet
from .DevicePreference import DevicePreference, DEFAULT_DEVICE_PARAMS

DEFAULT_BETA_PARAMS = {
    'desktop': {'control': (10, 100), 'variation': (20, 120)},
    'mobile': {'control': (10, 100), 'variation': (20, 120)},
    'tablet': {'control': (10, 100), 'variation': (20, 120)}
}

class PopulationSegment:
    def __init__(self, name, beta_params=DEFAULT_BETA_PARAMS,
                 device_params=DEFAULT_DEVICE_PARAMS,
                 hr_visit_rate_func=None):
        self.name = name
        if not hr_visit_rate_func:
            self.hr_visit_rate_func = lambda _: 5/139
        else:
            self.hr_visit_rate_func = hr_visit_rate_func
        self.ctr = {}
        for device in beta_params:
            self.ctr[device] = {
                'control': beta(*beta_params[device]['control']),
                'variation': beta(*beta_params[device]['variation'])
            }
        self.device_params = device_params

    def num_visits_in_hour(self, the_datetime):
        """Determines the number of visits starting at the_datetime, and going one hour"""
        rate = self.hr_visit_rate_func(the_datetime)
        num_visits = poisson(rate).rvs()
        return num_visits

    def set_device_preferences(self, mobile, tablet, desktop):
        self.device_params = {
            'mobile': mobile,
            'tablet': tablet,
            'desktop': desktop
        }

    def get_device_preference_for_user(self):
        return DevicePreference(self.device_params)

if __name__ == '__main__':
    import datetime
    the_segment = PopulationSegment('power_users', hr_visit_rate_func=lambda _: 12/139)
    print(the_segment.num_visits_in_hour(datetime.datetime(2018,1, 1, 10, 0)))
