import numpy as np
from scipy.stats import dirichlet

DEFAULT_DEVICE_LIST = {
    'mobile': 5,
    'tablet': 1,
    'desktop': 20
}

class DevicePreference:
    def __init__(self, device_params = DEFAULT_DEVICE_LIST):
        """
        device_parms is a dictionary of the form
        {
            'device1': param1,
            'device2': param2,
            ....
            'deviceN': paramN
        }
        The parameters are used in a dirichlet distribution to generate the user's
        probability of using a particular device. The higher paramI is, the more likely
        the user is to use deviceI.
        """
        self.device_names = list(device_params.keys())
        self.dirichlet_params = list(device_params.values())
        self.p_vector = dirichlet(self.dirichlet_params).rvs().reshape(-1,)

    def generate_device(self):
        """Return a specific device for user, drawn from user's probability distribution"""
        return np.random.choice(self.device_names, p=self.p_vector)
