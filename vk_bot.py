import requests
from datetime import date
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import re
import random


def create_keyboard(response):
    keyboard = VkKeyboard()

    if response == 'привет':
        keyboard.add_button('Поиск', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('Работа с избранными',
                            color=VkKeyboardColor.POSITIVE)

        keyboard.add_line()
        keyboard.add_button('Работа с черным списком',
                            color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('Пока', color=VkKeyboardColor.NEGATIVE)

    elif response == 'Не удалось найти пользователей для знакомств':
        keyboard.add_button('Проверьте свой возраст',
                            color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('Проверьте свой пол',
                            color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('Проверьте свой город',
                            color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('Вернуться в начало',
                            color=VkKeyboardColor.NEGATIVE)

    elif len(re.findall(r'Найдены записи о', response)) > 0:
        keyboard.add_button('Следующий в поиске',
                            color=VkKeyboardColor.POSITIVE)

    elif response == 'работа с избранными':
        keyboard.add_button('Список избранных целиком',
                            color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('Следующий в избранном',
                            color=VkKeyboardColor.POSITIVE)

        keyboard.add_line()
        keyboard.add_button('Вернуться в начало',
                            color=VkKeyboardColor.NEGATIVE)

    elif response == 'следующий в избранном':
        keyboard.add_button('Перенести в черный список',
                            color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('Следующий в избранном',
                            color=VkKeyboardColor.POSITIVE)

        keyboard.add_line()
        keyboard.add_button('Лайк/дизлайк', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('Вернуться в начало',
                            color=VkKeyboardColor.NEGATIVE)

    elif response == 'работа с черным списком':

        keyboard.add_button('Черный список целиком',
                            color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('Следующий в черном списке',
                            color=VkKeyboardColor.POSITIVE)

        keyboard.add_line()
        keyboard.add_button('Вернуться в начало',
                            color=VkKeyboardColor.NEGATIVE)

    elif response == 'следующий в черном списке':
        keyboard.add_button('Перенести в избранное',
                            color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('Следующий в черном списке',
                            color=VkKeyboardColor.POSITIVE)

        keyboard.add_line()
        keyboard.add_button('Лайк/дизлайк', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('Вернуться в начало',
                            color=VkKeyboardColor.NEGATIVE)

    elif response == 'поиск':
        keyboard.add_button('Следующий в поиске',
                            color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('Работа с избранными',
                            color=VkKeyboardColor.POSITIVE)

        keyboard.add_line()
        keyboard.add_button('Работа с черным списком',
                            color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('Пока', color=VkKeyboardColor.NEGATIVE)

    elif len(re.findall(r'(следующий в поиске)|(в избранное)|(в черный список)', response)) > 0:
        keyboard.add_button('Следующий в поиске',
                            color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('Лайк/дизлайк', color=VkKeyboardColor.POSITIVE)

        keyboard.add_line()
        keyboard.add_button('В избранное', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('В черный список', color=VkKeyboardColor.POSITIVE)

        keyboard.add_line()
        keyboard.add_button('Работа с избранными',
                            color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('Работа с черным списком',
                            color=VkKeyboardColor.POSITIVE)

        keyboard.add_line()
        keyboard.add_button('Вернуться в начало',
                            color=VkKeyboardColor.NEGATIVE)
        keyboard.add_button('Пока', color=VkKeyboardColor.NEGATIVE)

    elif response == 'пока':
        keyboard.add_button('Привет', color=VkKeyboardColor.POSITIVE)

    # else:
    #     # Если непонятно, то отрабатываем ПРИВЕТ
    #     keyboard.add_button('Поиск', color=VkKeyboardColor.POSITIVE)
    #     keyboard.add_button('Работа с избранными', color=VkKeyboardColor.POSITIVE)
    #     keyboard.add_button('Работа с черным списком', color=VkKeyboardColor.POSITIVE)
    #     keyboard.add_button('Пока', color=VkKeyboardColor.NEGATIVE)

    keyboard = keyboard.get_keyboard()
    return keyboard


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
        return self.users[user_id].pop(0)

    def erase_data(self, user_id):
        self.users[user_id] = []

    def randomize_data(self, user_id):
        random.shuffle(self.users[user_id])


class VkBot:
    base_url = 'https://api.vk.com/method/'

    def __init__(self, user_id, token_1, token_2, user_results, db_object):
        self.token_1 = token_1
        self.token_2 = token_2
        self._USER_ID = user_id
        # self.common_params = {"access_token": self.token, "v": "5.131"}
        self._USER_DATA = self._get_user_data_from_vk_id(user_id)
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
            "ПОКА"]
        self.user_results = user_results
        self.dbObject = db_object

    def get_common_params(self):
        # Common parameters required for VK API requests.
        return {
            'access_token': self.token_2,
            'v': '5.154'
        }

    def _build_url(self, method):
        # Build complete URL for a VK API method.
        return f'{self.base_url}/{method}'

    @staticmethod
    def safe_get_from_list(in_list: list, index: int):
        try:
            return in_list[index]
        except IndexError:
            return ''

    def safe_get_from_dict(self, in_dict: dict, key: str):
        try:
            return in_dict[key]
        except KeyError:
            return ''
        except TypeError:
            return ''

    @staticmethod
    def calculate_age(birth_date):
        data = [int(el) for el in birth_date.split('.')]
        if len(data) != 3:
            return 0
        today = date.today()
        age = today.year - data[2]-1 + ((today.month > data[1])
                                        or (today.month == data[1] and today.day >= data[0]))
        return age

    def _get_user_data_from_vk_id(self, user_id):
        # params = {"access_token": self.token_1, "v": "5.131"}
        # url = self.base_url + 'users.get?'
        url = self._build_url('users.get?')
        params = self.get_common_params()
        params.update({
            "user_ids": user_id,
            "fields": "sex,first_name,last_name,deactivated,is_closed,bdate,books,city,interests,movies,music,relation"
        })
        response = requests.get(url, params=params)
        try:
            response = response.json()['response'][0]
        except:
            return None
        if 'bdate' in response.keys():
            response['age'] = VkBot.calculate_age(response['bdate'])
            del response['bdate']
        else:
            response['age'] = 0

        return response

    def search_boy_girl_friends(self, user_data: dict):
        # url = self.base_url + 'users.search?'
        url = self._build_url('users.search?')
        params = self.get_common_params()
        if user_data['sex'] == 0:
            sex = 0
        elif user_data['sex'] == 1:
            sex = 2
        else:
            sex = 1
        if user_data['age'] == 0:
            min_age, max_age = 18, 30
        else:
            min_age, max_age = max(
                18, user_data['age'] - 3), max(18, user_data['age'] + 3)
        params.update({
            'city': user_data['city']['id'],
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
        except:
            return f"Не удалось найти пользователей для знакомств"
        self.user_results.add_user(self._USER_DATA['id'])
        # очистка от предыдущих результатов поиска
        self.user_results.erase_data(self._USER_DATA['id'])
        for _, item in enumerate(items):
            if self.safe_get_from_dict(item, 'bdate') == '':
                age = 0
            else:
                age = self.calculate_age(
                    self.safe_get_from_dict(item, 'bdate'))
            user_dict = {}
            user_dict = {
                'vk_id': str(item['id']),
                'name': self.safe_get_from_dict(item, 'first_name'),
                'surname': self.safe_get_from_dict(item, 'last_name'),
                'age': age,
                'sex': item['sex'],
                'city': self.safe_get_from_dict(self.safe_get_from_dict(item, 'city'), 'title'),
                'foto_a_1': '',
                'foto_a_2': '',
                'foto_a_3': '',
                'foto_fr_1': '',
                'foto_fr_2': '',
                'foto_fr_3': '',
                'interests': self.safe_get_from_dict(item, 'interests'),
                'books': self.safe_get_from_dict(item, 'books'),
                'movies': self.safe_get_from_dict(item, 'movies'),
                'music': self.safe_get_from_dict(item, 'music')
            }
            if not self.dbObject.add_user_db(user_dict):
                print(
                    f"Не удалось добавить пользователя {user_dict['vk_id']} в базу данных")
            else:
                self.user_results.add_data(self._USER_DATA['id'], item['id'])
                self.user_results.randomize_data(self._USER_DATA['id'])
        return f"Найдены записи о {_} пользователях для знакомства. Для просмотра нажмите кнопку 'Следующий в поиске'"

    def execute_command(self, command: str):
        # 0 "ПРИВЕТ"
        if command.strip().upper() == self._COMMANDS[0]:
            # сохраняем в память и в базу данные обратившегося
            photos = self.get_user_most_liked_photos(self._USER_DATA['id'])
            user_dict = {}
            prefix = 'photo' + str(self._USER_DATA['id']) + '_'
            photo1 = str(self.safe_get_from_list(
                self.safe_get_from_list(photos, 0), 3))
            photo2 = str(self.safe_get_from_list(
                self.safe_get_from_list(photos, 1), 3))
            photo3 = str(self.safe_get_from_list(
                self.safe_get_from_list(photos, 2), 3))
            user_dict = {
                'vk_id': str(self._USER_DATA['id']),
                'name': self.safe_get_from_dict(self._USER_DATA, 'first_name'),
                'surname': self.safe_get_from_dict(self._USER_DATA, 'last_name'),
                'age': self.safe_get_from_dict(self._USER_DATA, 'age'),
                'sex': self.safe_get_from_dict(self._USER_DATA, 'sex'),
                'city': self.safe_get_from_dict(self.safe_get_from_dict(self._USER_DATA, 'city'), 'title'),
                'foto_a_1': prefix + photo1 if photo1 != '' else '',
                'foto_a_2': prefix + photo2 if photo2 != '' else '',
                'foto_a_3': prefix + photo3 if photo3 != '' else '',
                'foto_fr_1': '',
                'foto_fr_2': '',
                'foto_fr_3': '',
                'interests': self.safe_get_from_dict(self._USER_DATA, 'interests'),
                'books': self.safe_get_from_dict(self._USER_DATA, 'books'),
                'movies': self.safe_get_from_dict(self._USER_DATA, 'movies'),
                'music': self.safe_get_from_dict(self._USER_DATA, 'music')
            }
            self.dbObject.add_user_db(user_dict)
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
            if next_item == '':
                keyboard = create_keyboard('Привет')
                message = 'Необходимо сначала сделать поиск'
                attachment = ''
                return message, keyboard, attachment

            user_details = self.dbObject.get_user_by_vk_id(next_item)
            first_name = user_details['name']
            last_name = user_details['surname']
            age = user_details['age']
            attachment = ''
            for photo in self.get_user_most_liked_photos(next_item):
                if attachment != '':
                    attachment += ',photo' + \
                        str(next_item) + '_' + str(photo[3])
                else:
                    attachment = 'photo' + str(next_item) + '_' + str(photo[3])
            url = f'https://vk.com/id{next_item}'
            message = f"Кандидат в поиске:\n Имя: {first_name}\nФамилия: {last_name}\nВозраст: {age}\nСсылка на профиль: {url}\n"
            keyboard = create_keyboard(command.strip().lower())
            next_user_pics = {
                'vk_id': next_item,
                'foto_a_1': self.safe_get_from_list(attachment.split(','), 0),
                'foto_a_2': self.safe_get_from_list(attachment.split(','), 1),
                'foto_a_3': self.safe_get_from_list(attachment.split(','), 2)
            }
            self.dbObject.actualize_user(next_user_pics)
            # Сохраняем в памяти ID последнего выведенного кандидата
            self.user_results.add_user(str(self._USER_DATA['id']) + 'last')
            self.user_results.add_data(
                str(self._USER_DATA['id']) + 'last', next_item)

            # Сохраняем id последнего просмотренного пользователя
            self.user_results.current_user[self._USER_DATA['id']] = next_item
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
            message = 'тут будет лайк/дизлайк'
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
                cur_user_data = self.dbObject.get_user_by_vk_id(
                    list_favorits[0])
                self.dbObject.remove_favorites(
                    str(self._USER_ID), cur_user_data["vk_id"])
                first_name = cur_user_data["name"]
                last_name = cur_user_data["surname"]
                age = cur_user_data["age"]

                self.user_results.current_user[self._USER_DATA['id']
                                               ] = cur_user_data["vk_id"]

                for photo in self.get_user_most_liked_photos(cur_user_data["vk_id"]):
                    if attachment != '':
                        attachment += ',photo' + \
                            str(cur_user_data["vk_id"]) + '_' + str(photo[3])
                    else:
                        attachment = 'photo' + \
                            str(cur_user_data["vk_id"]) + '_' + str(photo[3])
                url = f'https://vk.com/id{cur_user_data["vk_id"]}'
                message = f"Следующий в избранном:\n Имя: {first_name}\nФамилия: {last_name}\nВозраст: {age}\nСсылка на профиль: {url}\n"

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
                cur_user_data = self.dbObject.get_user_by_vk_id(
                    list_blacklist[0])
                self.dbObject.remove_blacklist(
                    str(self._USER_ID), cur_user_data["vk_id"])
                first_name = cur_user_data["name"]
                last_name = cur_user_data["surname"]
                age = cur_user_data["age"]

                self.user_results.current_user[self._USER_DATA['id']
                                               ] = cur_user_data["vk_id"]

                for photo in self.get_user_most_liked_photos(cur_user_data["vk_id"]):
                    if attachment != '':
                        attachment += ',photo' + \
                            str(cur_user_data["vk_id"]) + '_' + str(photo[3])
                    else:
                        attachment = 'photo' + \
                            str(cur_user_data["vk_id"]) + '_' + str(photo[3])
                url = f'https://vk.com/id{cur_user_data["vk_id"]}'
                message = f"Следующий в черном списке:\n Имя: {first_name}\nФамилия: {last_name}\nВозраст: {age}\nСсылка на профиль: {url}\n"

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
                    favorite = f"Следующий в избранном:\n Имя: {first_name}\nФамилия: {last_name}\nВозраст: {age}\nСсылка на профиль: {url}\n"
                    all_favorits.append(favorite)
                message = "\n\n".join(all_favorits)
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
                    black_user = f"Следующий в черном списке:\n Имя: {first_name}\nФамилия: {last_name}\nВозраст: {age}\nСсылка на профиль: {url}\n"
                    all_black_users.append(black_user)
                message = "\n\n".join(all_black_users)
            return message, keyboard, attachment

        # 15 "ПОКА"
        elif command.strip().upper() == self._COMMANDS[15]:
            keyboard = create_keyboard("пока")
            message = f"Пока, {self._USER_DATA['first_name']}!"
            attachment = ''
            return message, keyboard, attachment

        else:
            message = "Не понимаю о чем вы..."
            keyboard = create_keyboard("привет")
            attachment = ""
            return message, keyboard, attachment

    def _user_photos(self, album: str, user_id: str) -> dict:
        # Retrieve user photos from a specified album.
        params = self.get_common_params()
        params.update({'owner_id': user_id, 'album_id': album,
                      'extended': 1, 'count': '1000'})
        response = requests.get(self._build_url('photos.get'), params=params)
        return response.json()

    def get_user_most_liked_photos(self, user_id: str, number_ph: int = 3) -> list:
        ph_urls = []
        ph_likes = []
        ph_type = []
        ph_id = []
        photos = self._user_photos('profile', user_id)
        if self.safe_get_from_dict(photos, 'error') == '':
            if photos['response']['count'] > 0:
                for ph in photos['response']['items']:
                    # Extract and store photo details.
                    ph_urls.append(ph['sizes'][-1]['url'])
                    ph_likes.append(ph['likes']['count'])
                    ph_type.append(ph['sizes'][-1]['type'])
                    ph_id.append(ph['id'])
                # Combine and sort photos based on likes.
                ph_urls_sorted = list(zip(ph_likes, ph_urls, ph_type, ph_id))
                ph_urls_sorted = sorted(ph_urls_sorted, reverse=True)
                return ph_urls_sorted[:number_ph]
            else:
                return ['Нет фотографий']
        else:
            return [photos['error']['error_msg']]
