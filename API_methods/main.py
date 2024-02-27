import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from random import randrange
from vk_bot import VkBot
from vk_bot import UserResultsStorage


def get_tokens(file_name: str = "config.txt"):
    with open(file_name, "r", encoding="utf-8") as file:
        return file.read().strip().split('\n')


def start_vk_bot(token_1, token_2):

    vk = vk_api.VkApi(token=token_1)
    longpoll = VkLongPoll(vk)

    def write_msg(user_id, message):
        vk.method('messages.send', {
            'user_id': user_id, 'message': message, 'random_id': randrange(10 ** 7)})

    userResults = UserResultsStorage()
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:

                bot = VkBot(event.user_id, token_1, token_2, userResults)
                message = bot.execute_command(event.text)
                write_msg(event.user_id, message)


if __name__ == "__main__":

    token_1, token_2 = get_tokens()
    start_vk_bot(token_1, token_2)
