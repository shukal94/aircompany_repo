from user import User

class Guest(User):

    def __init__(self, id):
        self.id = id