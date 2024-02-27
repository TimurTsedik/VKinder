import requests
from configparser import ConfigParser
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType


def get_ini_value(section: str, option: str) -> str:
    config = ConfigParser()
    config.read('config.ini')
    return config.get(section, option)


def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message})


vk_token = get_ini_value('VK', 'token')
vk = vk_api.VkApi(token=vk_token)
session_api = vk.get_api()
long_poll = VkLongPoll(vk)

# Основной цикл
for event in long_poll.listen():

    # Если пришло новое сообщение
    if event.type == VkEventType.MESSAGE_NEW:

        # Если оно имеет метку для меня(то есть бота)
        if event.to_me:

            # Сообщение от пользователя
            request = event.text

            # Каменная логика ответа
            if request == "привет":
                write_msg(event.user_id, "Хай")
            elif request == "пока":
                write_msg(event.user_id, "Пока((")
            else:
                write_msg(event.user_id, "Не поняла вашего ответа...")
