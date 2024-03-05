import random


class UserResultsStorage:
    def __init__(self):
        self.users = {}
        self.current_user = {}

    def add_user(self, user_id):
        if user_id not in self.users:
            self.users[user_id] = []

    def add_data(self, user_id, data):
        if user_id in self.users:
            self.users[user_id].append(data)
        else:
            self.add_user(user_id)
            self.users[user_id].append(data)

    def get_data(self, user_id):
        if user_id not in self.users:
            return ''
        if len(self.users[user_id]) == 0:
            return ''
        return self.users[user_id].pop(0)

    def erase_data(self, user_id):
        self.users[user_id] = []

    def randomize_data(self, user_id):
        random.shuffle(self.users[user_id])
