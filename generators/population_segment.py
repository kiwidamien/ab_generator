from scipy.stats import beta, poisson, dirichlet

DEFAULT_BETA_PARAMS = {
    'desktop': {'control': (10, 100), 'variation': (20, 120)},
    'mobile': {'control': (10, 100), 'variation': (20, 120)},
    'tablet': {'control': (10, 100), 'variation': (20, 120)}
}

class PopulationSegment:
    def __init__(self, name, beta_params = DEFAULT_BETA_PARAMS,
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
        self.mobile, self.tablet, self.desktop = 30, 1, 100
        self.device_distribution = self._get_distribution()

    def num_visits_in_hour(self, the_datetime):
        """Determines the number of visits starting at the_datetime, and going one hour"""
        rate = self.hr_visit_rate_func(the_datetime)
        num_visits = poisson(rate).rvs()
        return num_visits

    def _get_distribution(self):
        return dirichlet([self.mobile, self.tablet, self.desktop])

    def set_device_preferences(self, mobile, tablet, desktop):
        self.mobile, self.tablet, self.desktop = mobile, tablet, desktop
        self.device_distribution = self._get_distribution()

if __name__ == '__main__':
    import datetime
    the_segment = PopulationSegment('power_users', hr_visit_rate_func=lambda _: 12/139)
    print(the_segment.num_visits_in_hour(datetime.datetime(2018,1, 1, 10, 0)))
