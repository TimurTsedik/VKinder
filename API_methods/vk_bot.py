import requests
from datetime import date


class VkBot:

    base_url = 'https://api.vk.com/method/'

    def __init__(self, user_id, token_1, token_2):

        self.token_1 = token_1
        self.token_2 = token_2
        self._USER_ID = user_id
        # self.common_params = {"access_token": self.token, "v": "5.131"}
        self._USER_DATA = self._get_user_data_from_vk_id(user_id)
        self._COMMANDS = ["ПРИВЕТ", "ПОИСК", "СЛЕДУЮЩИЙ",
                          "ДОБАВИТЬ В ИЗБРАННОЕ", "СПИСОК ИЗБРАННОГО", "ПОКА"]

    @staticmethod
    def calculate_age(bdate):
        data = [int(el) for el in bdate.split('.')]
        if len(data) != 3:
            return 0
        today = date.today()
        age = today.year - data[2]-1 + ((today.month > data[1])
                                        or (today.month == data[1] and today.day >= data[0]))
        return age

    def _get_user_data_from_vk_id(self, user_id):
        params = {"access_token": self.token_1, "v": "5.131"}
        url = self.base_url + 'users.get?'
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

        url = self.base_url + 'users.search?'
        params = {"access_token": self.token_2, "v": "5.131"}

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
                18, user_data['age'] - 5), max(18, user_data['age'] + 5)

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

        '''Необходим код для записи данных(список items) в БД'''

        return f"Найдены записи о {count} пользователях для знакомства. Для просмотра введите команду 'Следующий'"

    def execute_command(self, comand):

        # Привет
        if comand.strip().upper() == self._COMMANDS[0]:
            return f"Привет, {self._USER_DATA['first_name']}!"

        # Поиск
        elif comand.strip().upper() == self._COMMANDS[1]:
            message = self.search_boy_girl_friends(self._USER_DATA)
            return message

        # Выдача следующего пользователя
        elif comand.strip().upper() == self._COMMANDS[2]:
            '''Нужен код для выборки из БД данных по следующему подходящему пользователю'''
            return ' '

        # Добавление пользователя в избранное
        elif comand.strip().upper() == self._COMMANDS[3]:
            '''Нужен код для добавления метки избранное для пользователя в БД'''
            return ' '

        # Вывести список избранного
        elif comand.strip().upper() == self._COMMANDS[4]:
            '''Нужен код для вывода списка избранного'''
            return ' '

        # Пока
        elif comand.strip().upper() == self._COMMANDS[5]:
            return f"Пока, {self._USER_DATA['first_name']}!"

        else:
            return "Не понимаю о чем вы..."
