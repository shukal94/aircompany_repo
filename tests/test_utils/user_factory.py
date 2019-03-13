import string
import random

class UserFactory(object):

    def __init__(self):
        self.username = None
        self.first_name = None
        self.last_name = None
        self.email = None
        self.password = 12345
        self.password2 = self.password
        self.address = None
        self.postal_code = 123

    def create_minimal_user(self):
        size = 6
        chars = string.ascii_letters
        self.username = ''.join(random.choice(chars) for _ in range(size))
        self.first_name = ''.join(random.choice(chars) for _ in range(size))
        self.last_name = ''.join(random.choice(chars) for _ in range(size))
        self.email = ''.join(random.sample((string.ascii_lowercase + string.digits), 4)) + '@' +\
                     ''.join(random.sample((string.ascii_lowercase + string.digits), 4)) + '.com'
        self.address = ''.join(random.choice(chars) for _ in range(size))
        return self
