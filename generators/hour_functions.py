import datetime

def make_weekend_power_user(base_rate):
    def hour_rate(the_datetime):
        actual_rate = base_rate
        if the_datetime.weekday() in [5, 6]:
            actual_rate *= 1.3
        if the_datetime.hour < 10 or the_datetime.hour > 20:
            actual_rate *= 0.8
        return actual_rate
    return hour_rate

def make_humpday_daytime_power_user(base_rate):
    def hour_rate(the_datetime):
        actual_rate = base_rate
        if the_datetime.weekday() == 2:
            actual_rate *= 1.8
        if the_datetime.hour < 12 or the_datetime.hour > 18:
            actual_rate *= 0.7
        return actual_rate
    return hour_rate

def make_humpday_evening_power_user(base_rate):
    def hour_rate(the_datetime):
        actual_rate = base_rate
        if the_datetime.weekday() == 2:
            actual_rate *= 1.8
        if the_datetime.hour < 18:
            actual_rate *= 0.6
        return actual_rate
    return hour_rate

def make_generic_hour_function(base_rate, peak_days, peak_times, lull_days, lull_times, dead_times, peak_mult, lull_mult):
    """
    base_rate: float
    peak_days: list of ints (0=Mon, 6=Sun) where base_rate is multiplied by peak_mult
    lull_days: list of ints (0=Mon, 6=Sun) where base_rate is multiplied by lull_mult
    peak_times: list of ints (0-23)
    lull_times: list of ints (0-23)
    dead_times: times where the user won't have any activity
    peak_mult: multiplier when for peaks applied. Should be greater than 1
    lull_mult: multiplier for lulls applied. Should be less than 1.

    returns:
    a function that takes a datetime, and returns a rate
    """
    def hour_rate(the_datetime):
        actual_rate = base_rate
        if the_datetime.hour in dead_times:
            return 0
        if the_datetime.weekday() in peak_days:
            actual_rate *= peak_mult
        if the_datetime.weekday() in lull_days:
            actual_rate *= lull_mult
        if the_datetime.hour in peak_times:
            actual_rate *= peak_mult
        if the_datetime.hour in lull_times:
            actual_rate *= lull_mult
        return actual_rate
    return hour_rate

def make_weekday_ends_power_user(base_rate):
    return make_generic_hour_function(base_rate,
                                      peak_days=[0, 4],
                                      lull_days=[3, 5, 6],
                                      peak_times=range(8, 17),
                                      lull_times=range(17, 20),
                                      dead_times=range(0, 8),
                                      peak_mult=1.15, lull_mult=0.88)

f = make_humpday_daytime_power_user(2)
print(f(datetime.datetime(2018, 11, 26, 11, 00)))
