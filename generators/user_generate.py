from faker import Faker
from faker_web import WebProvider
from faker_cloud import BaseCloudProvider

fake = Faker()
fake.add_provider(WebProvider)
fake.add_provider(BaseCloudProvider)

print(fake.server_token())

class user:
    def __init__(self, sex=None, variation_assignment_function=None):
        self.user_info = fake.simple_profile(sex)
        self.user_info['default_user_agent'] = fake.user_agent()

        if variation_assignment_function:
            self.variation_info = variation_assignment_function(user_info)

    def __str__(self):
        return f'''
        username: {self.user_info['username']}
        gender: {self.user_info['sex']}
        default browser: {self.user_info['default_user_agent']}
        variation information: {self.variation_info}
        '''

    def __repr__(self):
        return f'{self.user_info['username']}'
    
