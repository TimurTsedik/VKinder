import random


class UserResultsStorage:
    """
    Initializes the object with an empty dictionary for users and an empty dictionary for the current user.
    """
    def __init__(self):
        self.users = {}
        self.current_user = {}
        self.last_favorite_num = {}
        self.last_blacklist_num = {}

    def add_user(self, user_id):
        """
        Add a new user to the list of users if the user does not already exist.

        Parameters:
            user_id (int): The ID of the user to be added.

        Returns:
            None
        """
        if user_id not in self.users:
            self.users[user_id] = []

    def add_data(self, user_id, data):
        """
        Add data to the user's record or create a new user and add the data.

        :param user_id: The ID of the user
        :param data: The data to be added
        :return: None
        """
        if user_id in self.users:
            self.users[user_id].append(data)
        else:
            self.add_user(user_id)
            self.users[user_id].append(data)

    def get_data(self, user_id):
        """
        Retrieve data for a given user ID and remove it from the user's data list.

        Args:
            user_id (int): The ID of the user whose data is to be retrieved.

        Returns:
            str: The data associated with the user ID, or an empty string if the
            user ID is not found or the user's data list is empty.
        """
        if user_id not in self.users:
            return ''
        if len(self.users[user_id]) == 0:
            return ''
        return self.users[user_id].pop(0)

    def erase_data(self, user_id):
        """
        Method to erase data for a specific user identified by user_id.

        Args:
            self: The object itself.
            user_id: The identifier of the user whose data will be erased.

        Returns:
            None
        """
        self.users[user_id] = []

    def randomize_data(self, user_id):
        """
        Randomizes the data associated with the given user ID.

        Args:
            self: The object instance
            user_id: The ID of the user whose data needs to be randomized

        Returns:
            None
        """
        random.shuffle(self.users[user_id])


    def make_list_distinct(self, user_id):
        """
        Makes the list of data for the given user ID distinct.

        Args:
            self: The object instance
            user_id: The ID of the user whose data needs to be made distinct

        Returns:
            None
        """
        self.users[user_id] = list(set(self.users[user_id]))

    def get_last_favorite_num(self, user_id):
        if user_id not in self.last_favorite_num:
            self.last_favorite_num[user_id] = 0
        return self.last_favorite_num[user_id]
        

    def get_last_blacklist_num(self, user_id):
        if user_id not in self.last_blacklist_num:
            self.last_blacklist_num[user_id] = 0
        return self.last_blacklist_num[user_id]
