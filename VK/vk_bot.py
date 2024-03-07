import requests

from VK.vk_api_fuctions import create_keyboard, safe_get_from_dict, safe_get_from_list, calculate_age, build_url, \
    get_common_params, get_user_most_liked_photos, get_user_data_from_vk_id


class VkBot:
    base_url = 'https://api.vk.com/method/'

    def __init__(self, user_id, token_1, token_2, user_results, db_object):
        """
        Initializes the class with the provided user_id, token_1, token_2, user_results, and db_object.

        Parameters:
            user_id (int): The user ID.
            token_1 (str): The first token.
            token_2 (str): The second token.
            user_results: The user results.
            db_object: The database object.

        Returns:
            None
        """
        self.token_1 = token_1
        self.token_2 = token_2
        self._USER_ID = user_id
        # self.common_params = {"access_token": self.token, "v": "5.131"}
        self._USER_DATA = get_user_data_from_vk_id(self.base_url, self.token_2, str(user_id))
        self._COMMANDS = [
            "ПРИВЕТ",
            "ПОИСК",
            "СЛЕДУЮЩИЙ В ПОИСКЕ",
            'В ИЗБРАННОЕ', 'В ЧЕРНЫЙ СПИСОК', 'ЛАЙК/ДИЗЛАЙК', 'ВЕРНУТЬСЯ В НАЧАЛО',
            "РАБОТА С ИЗБРАННЫМИ",
            'ПЕРЕНЕСТИ В ЧЕРНЫЙ СПИСОК', 'СЛЕДУЮЩИЙ В ИЗБРАННОМ',
            "РАБОТА С ЧЕРНЫМ СПИСКОМ",
            'ПЕРЕНЕСТИ В ИЗБРАННОЕ', 'СЛЕДУЮЩИЙ В ЧЕРНОМ СПИСКЕ',
            "СПИСОК ИЗБРАННЫХ ЦЕЛИКОМ", "ЧЕРНЫЙ СПИСОК ЦЕЛИКОМ",
            "ПОКА", "УДАЛИТЬ ИЗ ИЗБРАННЫХ", "УДАЛИТЬ ИЗ ЧЕРНОГО СПИСКА"]
        self.user_results = user_results
        self.dbObject = db_object

    def search_boy_girl_friends(self, user_data: dict):
        """
        Performs a search for potential boy or girl friends based on the provided user_data.

        Args:
            self: the object instance
            user_data (dict): the user data containing information such as sex, age, and city

        Returns:
            str: a message indicating the success or failure of the search
        """
        url = build_url(self.base_url, 'users.search?')
        params = get_common_params(self.token_2)
        if user_data['sex'] == 0:
            sex = 0
        elif user_data['sex'] == 1:
            sex = 2
        else:
            sex = 1
        age = safe_get_from_dict(user_data, 'age')
        age = int(age) if age != '' else 0
        if age == 0:
            min_age, max_age = 18, 30
        else:
            min_age, max_age = max(
                18, age - 3), max(18, age + 3)
        city = safe_get_from_dict(safe_get_from_dict(user_data, 'city'), 'id')
        if city == '' or sex == 0 or age == 0:
            return f"Для поиска необходимо указать в своем профиле город, пол и возраст"
        params.update({
            'city': city,
            'sex': sex,
            'age_from': min_age,
            'age_to': max_age,
            'fields': "sex,first_name,last_name,deactivated,is_closed,bdate,books,city,interests,movies,music,relation",
            'count': 1000
        })
        response = requests.get(url, params=params)
        try:
            response = response.json()["response"]
            count, items = response["count"], response["items"]
        except KeyError:
            return f"Не удалось найти пользователей для знакомств"
        self.user_results.add_user(self._USER_DATA['id'])
        # очистка от предыдущих результатов поиска
        # self.user_results.erase_data(self._USER_DATA['id'])
        for _, item in enumerate(items):
            if safe_get_from_dict(item, 'bdate') == '':
                age = 0
            else:
                age = calculate_age(
                    safe_get_from_dict(item, 'bdate'))
            # adding user to database
            user_dict = {
                'vk_id': str(item['id']),
                'name': safe_get_from_dict(item, 'first_name'),
                'surname': safe_get_from_dict(item, 'last_name'),
                'age': age,
                'sex': item['sex'],
                'city': safe_get_from_dict(safe_get_from_dict(item, 'city'), 'title'),
                'foto_a_1': '',
                'foto_a_2': '',
                'foto_a_3': '',
                'foto_fr_1': '',
                'foto_fr_2': '',
                'foto_fr_3': '',
                'interests': safe_get_from_dict(item, 'interests'),
                'books': safe_get_from_dict(item, 'books'),
                'movies': safe_get_from_dict(item, 'movies'),
                'music': safe_get_from_dict(item, 'music')
            }
            if self.dbObject.add_user_db(user_dict) == 1 :
                print(
                    f"Не удалось добавить пользователя {user_dict['vk_id']} в базу данных. Возраст: {user_dict['age']}")
            elif self.dbObject.add_user_db(user_dict) == 0:
                self.user_results.add_data(self._USER_DATA['id'], item['id'])
            else:
                print(
                    f"Пользователь {user_dict['vk_id']} добавлен в базу данных. Возраст: {user_dict['age']}")
        # avoiding dups in users list
        self.user_results.make_list_distinct(self._USER_DATA['id'])
        self.user_results.randomize_data(self._USER_DATA['id'])
        return f"Найдены записи о {_} пользователях для знакомства. Для просмотра нажмите кнопку 'Следующий в поиске'"

    def execute_command(self, command: str):
        """
        A function to execute a command based on the provided input. It checks the command and
        returns the appropriate message, keyboard, and attachment based on the command passed as input.
        """
        # проверка наличия пользователя в базе
        if not self.dbObject.if_user_in_db(self._USER_DATA['id']):
            command = 'ПРИВЕТ'

        # 0 "ПРИВЕТ"
        if command.strip().upper() == self._COMMANDS[0]:
            # сохраняем в память и в базу данные обратившегося
            photos = get_user_most_liked_photos(self.token_2, self.base_url, self._USER_DATA['id'])
            prefix = 'photo' + str(self._USER_DATA['id']) + '_'
            photo1 = str(safe_get_from_list(
                safe_get_from_list(photos, 0), 3))
            photo2 = str(safe_get_from_list(
                safe_get_from_list(photos, 1), 3))
            photo3 = str(safe_get_from_list(
                safe_get_from_list(photos, 2), 3))
            user_dict = {
                'vk_id': str(self._USER_DATA['id']),
                'name': safe_get_from_dict(self._USER_DATA, 'first_name'),
                'surname': safe_get_from_dict(self._USER_DATA, 'last_name'),
                'age': safe_get_from_dict(self._USER_DATA, 'age'),
                'sex': safe_get_from_dict(self._USER_DATA, 'sex'),
                'city': safe_get_from_dict(safe_get_from_dict(self._USER_DATA, 'city'), 'title'),
                'foto_a_1': prefix + photo1 if photo1 != '' else '',
                'foto_a_2': prefix + photo2 if photo2 != '' else '',
                'foto_a_3': prefix + photo3 if photo3 != '' else '',
                'foto_fr_1': '',
                'foto_fr_2': '',
                'foto_fr_3': '',
                'interests': safe_get_from_dict(self._USER_DATA, 'interests'),
                'books': safe_get_from_dict(self._USER_DATA, 'books'),
                'movies': safe_get_from_dict(self._USER_DATA, 'movies'),
                'music': safe_get_from_dict(self._USER_DATA, 'music')
            }
            self.dbObject.add_user_db(user_dict)
            self.user_results.last_favorite_num[self._USER_DATA['id']] = -1
            self.user_results.last_blacklist_num[self._USER_DATA['id']] = -1
            keyboard = create_keyboard(command.strip().lower())
            message = f"Привет, {self._USER_DATA['first_name']}!"
            attachment = ''
            return message, keyboard, attachment

        # 1 "ПОИСК"
        elif command.strip().upper() == self._COMMANDS[1]:
            keyboard = create_keyboard(command.strip().lower())
            message = self.search_boy_girl_friends(self._USER_DATA)
            attachment = ''
            return message, keyboard, attachment

        # 2 "СЛЕДУЮЩИЙ В ПОИСКЕ"
        elif command.strip().upper() == self._COMMANDS[2]:
            next_item = str(self.user_results.get_data(self._USER_DATA['id']))
            # check if user in blacklist
            while self.dbObject.if_user_in_blacklist(self._USER_DATA['id'], next_item):
                next_item = str(self.user_results.get_data(self._USER_DATA['id']))
            if next_item == '':
                keyboard = create_keyboard('Привет')
                message = 'Необходимо сначала сделать поиск'
                attachment = ''
                return message, keyboard, attachment
            # get user data from DB
            user_details = self.dbObject.get_user_by_vk_id(next_item)
            first_name = user_details['name']
            last_name = user_details['surname']
            age = user_details['age']
            attachment = ''
            # if user actual and at least one photo
            if self.dbObject.actualize_user(user_details) and user_details['foto_a_1'] != '':
                # take from DB

                attachment = ','.join([user_details['foto_a_1'], user_details['foto_a_2'], user_details['foto_a_3']])
            else:
                # take from VK
                for photo in get_user_most_liked_photos(self.token_2, self.base_url, next_item):
                    if attachment != '':
                        attachment += ',photo' + \
                            str(next_item) + '_' + str(photo[3])
                    else:
                        attachment = 'photo' + str(next_item) + '_' + str(photo[3])
                # update DB
                next_user_pics = {
                    'vk_id': next_item,
                    'foto_a_1': safe_get_from_list(attachment.split(','), 0),
                    'foto_a_2': safe_get_from_list(attachment.split(','), 1),
                    'foto_a_3': safe_get_from_list(attachment.split(','), 2)
                }
                self.dbObject.actualize_user(next_user_pics)
            # create message
            url = f'https://vk.com/id{next_item}'
            message = (f"Кандидат в поиске:\n Имя: {first_name}\nФамилия: "
                       f"{last_name}\nВозраст: {age}\nСсылка на профиль: {url}\n")
            # Сохраняем id последнего просмотренного пользователя
            self.user_results.current_user[self._USER_DATA['id']] = next_item
            keyboard = create_keyboard(command.strip().lower())
            return message, keyboard, attachment

        # 3 'В избранное'
        elif command.strip().upper() == self._COMMANDS[3]:

            cur_user_id = self.user_results.current_user[self._USER_DATA['id']]
            result = self.dbObject.add_favorites(
                str(self._USER_ID), cur_user_id)

            if not result:
                message = 'Пользователь уже в избранных'
            else:
                message = f'Пользователь с id {cur_user_id} помещен в список избранных'
            keyboard = create_keyboard("поиск")
            attachment = ''
            return message, keyboard, attachment

        # 4 'В черный список'
        elif command.strip().upper() == self._COMMANDS[4]:

            cur_user_id = self.user_results.current_user[self._USER_DATA['id']]
            result = self.dbObject.add_blacklist(
                str(self._USER_ID), cur_user_id)
            if not result:
                message = 'Пользователь уже в черном списке'
            else:
                message = f'Пользователь с id {cur_user_id} помещен в черный список'
            keyboard = create_keyboard("поиск")
            attachment = ''
            return message, keyboard, attachment

        # 5 'Лайк/дизлайк'
        elif command.strip().upper() == self._COMMANDS[5]:
            keyboard = create_keyboard(command.strip().lower())
            message = 'тут будет лайк/дизлайк'
            attachment = ''
            return message, keyboard, attachment

        # 6 'Вернуться в начало'
        elif command.strip().upper() == self._COMMANDS[6]:
            keyboard = create_keyboard("привет")
            message = 'Возвращаемся в самое начало'
            attachment = ''
            return message, keyboard, attachment

        # 7 "РАБОТА С ИЗБРАННЫМИ"
        elif command.strip().upper() == self._COMMANDS[7]:

            self.user_results.current_user[self._USER_DATA['id']] = None
            list_favorits = self.dbObject.get_list_favorites(
                str(self._USER_ID))
            if not list_favorits:
                message = 'Ваш список избранных пуст'
                keyboard = create_keyboard('привет')
            else:
                message = f'В вашем списке избранных {len(list_favorits)} пользователей'
                keyboard = create_keyboard(command.strip().lower())
                self.user_results.last_favorite_num[self._USER_DATA['id']] = -1
            attachment = ''
            return message, keyboard, attachment

        # 8 'Перенести в черный список'
        elif command.strip().upper() == self._COMMANDS[8]:
            cur_user_id = self.user_results.current_user[self._USER_DATA['id']]

            result = self.dbObject.add_blacklist(
                str(self._USER_ID), cur_user_id)
            if not result:
                message = 'Пользователь уже в черном списке'
            else:
                message = f'Пользователь с id {cur_user_id} помещен в черный список'
            keyboard = create_keyboard("работа с избранными")
            attachment = ''

            return message, keyboard, attachment

        # 9 'СЛЕДУЮЩИЙ В ИЗБРАННОМ'
        elif command.strip().upper() == self._COMMANDS[9]:

            list_favorits = self.dbObject.get_list_favorites(
                str(self._USER_ID))
            attachment = ''
            if not list_favorits:
                message = 'Ваш список избранных пуст'
                keyboard = create_keyboard('привет')
            else:
                keyboard = create_keyboard(command.strip().lower())
                last_viewed_user_num = self.user_results.get_last_favorite_num(self._USER_DATA['id'])
                if last_viewed_user_num + 1 >= len(list_favorits):
                    message = 'Ваш список избранных подошел к концу'
                    keyboard = create_keyboard('привет')
                    self.user_results.last_favorite_num[self._USER_DATA['id']] = -1
                    return message, keyboard, attachment
                else:
                    cur_user_data = self.dbObject.get_user_by_vk_id(list_favorits[last_viewed_user_num + 1])
                # self.dbObject.remove_favorites(
                #     str(self._USER_ID), cur_user_data["vk_id"])
                first_name = cur_user_data["name"]
                last_name = cur_user_data["surname"]
                age = cur_user_data["age"]
                self.user_results.last_favorite_num[self._USER_DATA['id']] = last_viewed_user_num + 1
                self.user_results.current_user[self._USER_DATA['id']
                                               ] = cur_user_data["vk_id"]

                for photo in get_user_most_liked_photos(self.token_2, self.base_url, cur_user_data["vk_id"]):
                    if attachment != '':
                        attachment += ',photo' + \
                            str(cur_user_data["vk_id"]) + '_' + str(photo[3])
                    else:
                        attachment = 'photo' + \
                            str(cur_user_data["vk_id"]) + '_' + str(photo[3])
                url = f'https://vk.com/id{cur_user_data["vk_id"]}'
                message = (f"Следующий в избранном:\n Имя: {first_name}\n"
                           f"Фамилия: {last_name}\nВозраст: {age}\nСсылка на профиль: {url}\n")

            return message, keyboard, attachment

        # 10 "РАБОТА С ЧЕРНЫМ СПИСКОМ"
        elif command.strip().upper() == self._COMMANDS[10]:

            self.user_results.current_user[self._USER_DATA['id']] = None
            list_blacklist = self.dbObject.get_list_blacklist(
                str(self._USER_ID))
            if not list_blacklist:
                message = 'Ваш черный список пуст'
                keyboard = create_keyboard('привет')
            else:
                message = f'В вашем черном списке {len(list_blacklist)} пользователей'
                keyboard = create_keyboard(command.strip().lower())
                self.user_results.last_blacklist_num[self._USER_DATA['id']] = -1
            attachment = ''
            return message, keyboard, attachment

        # 11 'Перенести в избранное'
        elif command.strip().upper() == self._COMMANDS[11]:

            cur_user_id = self.user_results.current_user[self._USER_DATA['id']]

            result = self.dbObject.add_favorites(
                str(self._USER_ID), cur_user_id)
            if not result:
                message = 'Пользователь уже в избранных'
            else:
                message = f'Пользователь с id {cur_user_id} помещен в избранные'
            keyboard = create_keyboard("работа с черным списком")
            attachment = ''

            return message, keyboard, attachment

        # 12'Следующий в черном списке'
        elif command.strip().upper() == self._COMMANDS[12]:

            list_blacklist = self.dbObject.get_list_blacklist(
                str(self._USER_ID))
            attachment = ''
            if not list_blacklist:
                message = 'Ваш черный список пуст'
                keyboard = create_keyboard('привет')
            else:
                keyboard = create_keyboard(command.strip().lower())
                last_viewed_user_num = self.user_results.get_last_blacklist_num(self._USER_DATA['id'])
                if last_viewed_user_num + 1 >= len(list_blacklist):
                    message = 'Ваш черный список подошел к концу'
                    keyboard = create_keyboard('привет')
                    self.user_results.last_favorite_num[self._USER_DATA['id']] = -1
                    return message, keyboard, attachment
                else:
                    cur_user_data = self.dbObject.get_user_by_vk_id(list_blacklist[last_viewed_user_num + 1])

                # self.dbObject.remove_blacklist(
                #     str(self._USER_ID), cur_user_data["vk_id"])
                first_name = cur_user_data["name"]
                last_name = cur_user_data["surname"]
                age = cur_user_data["age"]
                self.user_results.last_blacklist_num[self._USER_DATA['id']] = last_viewed_user_num + 1
                self.user_results.current_user[self._USER_DATA['id']
                                               ] = cur_user_data["vk_id"]

                for photo in get_user_most_liked_photos(self.token_2, self.base_url, cur_user_data["vk_id"]):
                    if attachment != '':
                        attachment += ',photo' + \
                            str(cur_user_data["vk_id"]) + '_' + str(photo[3])
                    else:
                        attachment = 'photo' + \
                            str(cur_user_data["vk_id"]) + '_' + str(photo[3])
                url = f'https://vk.com/id{cur_user_data["vk_id"]}'
                message = (f"Следующий в черном списке:\n Имя: {first_name}\n"
                           f"Фамилия: {last_name}\nВозраст: {age}\nСсылка на профиль: {url}\n")

            return message, keyboard, attachment

        # 13 "СПИСОК ИЗБРАННЫХ ЦЕЛИКОМ"
        elif command.strip().upper() == self._COMMANDS[13]:
            list_favorits = self.dbObject.get_list_favorites(
                str(self._USER_ID))
            attachment = ''
            if not list_favorits:
                message = 'Ваш список избранных пуст'
                keyboard = create_keyboard('привет')
            else:
                keyboard = create_keyboard("работа с избранными")
                all_favorits = []
                for cur_user_id in list_favorits:
                    cur_user_data = self.dbObject.get_user_by_vk_id(
                        cur_user_id)
                    first_name = cur_user_data["name"]
                    last_name = cur_user_data["surname"]
                    age = cur_user_data["age"]
                    url = f'https://vk.com/id{cur_user_data["vk_id"]}'
                    favorite = (f"Следующий в избранном:\n Имя: {first_name}\n"
                                f"Фамилия: {last_name}\nВозраст: {age}\nСсылка на профиль: {url}\n")
                    all_favorits.append(favorite)
                message = "\n\n".join(all_favorits)
                self.user_results.last_favorite_num[self._USER_DATA['id']] = -1
            return message, keyboard, attachment

        # 14 "ЧЕРНЫЙ СПИСОК ЦЕЛИКОМ"
        elif command.strip().upper() == self._COMMANDS[14]:
            list_blacklist = self.dbObject.get_list_blacklist(
                str(self._USER_ID))
            attachment = ''
            if not list_blacklist:
                message = 'Ваш черный список пуст'
                keyboard = create_keyboard('привет')
            else:
                keyboard = create_keyboard("работа с черным списком")
                all_black_users = []
                for cur_user_id in list_blacklist:
                    cur_user_data = self.dbObject.get_user_by_vk_id(
                        cur_user_id)
                    first_name = cur_user_data["name"]
                    last_name = cur_user_data["surname"]
                    age = cur_user_data["age"]
                    url = f'https://vk.com/id{cur_user_data["vk_id"]}'
                    black_user = (f"Следующий в черном списке:\n Имя: {first_name}\n"
                                  f"Фамилия: {last_name}\nВозраст: {age}\nСсылка на профиль: {url}\n")
                    all_black_users.append(black_user)
                message = "\n\n".join(all_black_users)
                self.user_results.last_blacklist_num[self._USER_DATA['id']] = -1
            return message, keyboard, attachment

        # 15 "ПОКА"
        elif command.strip().upper() == self._COMMANDS[15]:
            keyboard = create_keyboard("пока")
            message = f"Пока, {self._USER_DATA['first_name']}!"
            attachment = ''
            return message, keyboard, attachment

        # 16 "УДАЛИТЬ ИЗ ИЗБРАННЫХ"
        elif command.strip().upper() == self._COMMANDS[16]:
            cur_user_data = self.dbObject.get_user_by_vk_id(self.user_results.current_user[self._USER_DATA['id']])
            self.dbObject.remove_favorites(
                str(self._USER_ID), cur_user_data["vk_id"])
            keyboard = create_keyboard("работа с избранными")
            attachment = ''
            message = f'Пользователь с id {cur_user_data["vk_id"]} удален из списка избранных'
            return message, keyboard, attachment

        # 17 "УДАЛИТЬ ИЗ ЧЕРНОГО СПИСКА"
        elif command.strip().upper() == self._COMMANDS[17]:
            cur_user_data = self.dbObject.get_user_by_vk_id(self.user_results.current_user[self._USER_DATA['id']])
            self.dbObject.remove_blacklist(
                str(self._USER_ID), cur_user_data["vk_id"])
            keyboard = create_keyboard("работа с черным списком")
            attachment = ''
            message = f'Пользователь с id {cur_user_data["vk_id"]} удален из списка избранных'
            return message, keyboard, attachment

        else:
            message = "Не понимаю о чем вы..."
            keyboard = create_keyboard("привет")
            attachment = ""
            return message, keyboard, attachment
