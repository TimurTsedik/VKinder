import re
from datetime import date

import requests
from vk_api.keyboard import VkKeyboard, VkKeyboardColor


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


def safe_get_from_dict(in_dict: dict, key: str):
    try:
        return in_dict[key]
    except KeyError:
        return ''
    except TypeError:
        return ''


def safe_get_from_list(in_list: list, index: int):
    try:
        return in_list[index]
    except IndexError:
        return ''


def calculate_age(birth_date):
    data = [int(el) for el in birth_date.split('.')]
    if len(data) != 3:
        return 0
    today = date.today()
    age = today.year - data[2]-1 + ((today.month > data[1])
                                    or (today.month == data[1] and today.day >= data[0]))
    return age


def build_url(base_url, method):
    # Build complete URL for a VK API method.
    return f'{base_url}/{method}'


def get_common_params(token_2):
    # Common parameters required for VK API requests.
    return {
        'access_token': token_2,
        'v': '5.154'
    }


def get_user_most_liked_photos(token_2, base_url, user_id: str, number_ph: int = 3) -> list:
    ph_urls = []
    ph_likes = []
    ph_type = []
    ph_id = []
    photos = user_photos(token_2, base_url, 'profile', user_id)
    if safe_get_from_dict(photos, 'error') == '':
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


def user_photos(token_2, base_url, album: str, user_id: str) -> dict:
    # Retrieve user photos from a specified album.
    params = get_common_params(token_2)
    params.update({'owner_id': user_id, 'album_id': album,
                  'extended': 1, 'count': '1000'})
    response = requests.get(build_url(base_url, 'photos.get'), params=params)
    return response.json()


def get_user_data_from_vk_id(base_url, token_2, user_id):
    url = build_url(base_url, 'users.get?')
    params = get_common_params(token_2)
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
        response['age'] = calculate_age(response['bdate'])
        del response['bdate']
    else:
        response['age'] = 0

    return response
