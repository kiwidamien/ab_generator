from scipy.stats import beta, poisson

class PopulationSegment:
    def __init__(self, name, control_a_b=(10,100), variation_a_b=(20,120),
                 hr_visit_rate_func=None):
        self.name = name
        if not hr_visit_rate_func:
            self.hr_visit_rate_func = lambda _: 5/139
        else:
            self.hr_visit_rate_func = hr_visit_rate_func
        self.ctr_control = beta(*control_a_b)
        self.ctr_variation = beta(*variation_a_b)

    def num_visits_in_hour(self, the_datetime):
        """Determines the number of visits starting at the_datetime, and going one hour"""
        rate = self.hr_visit_rate_func(the_datetime)
        num_visits = poisson(rate).rvs()
        return num_visits
