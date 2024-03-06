import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from random import randrange

from VK.vk_bot import VkBot
from VK.user_storage import UserResultsStorage

import configparser
from DB.ManageDB import ManageDB


def get_tokens(file_name: str = "config.ini"):
    """
    Retrieves tokens and database credentials from the specified or default configuration file.

    Args:
        file_name (str): The name of the configuration file to read. Defaults to "config.ini".

    Returns:
        tuple: A tuple containing group_token, personal_token, db_name, db_user_name, and db_user_password.
    """
    config = configparser.ConfigParser()
    config.read(file_name)
    group_token = config['VK']['group_token']
    personal_token = config['VK']['personal_token']
    db_name = config['DB']['DB_name']
    db_user_name = config['DB']['DB_user']
    db_user_password = config['DB']['DB_password']

    return group_token, personal_token, db_name, db_user_name, db_user_password


def start_vk_bot(token_1, token_2):
    """
    Function to start a VK bot and handle incoming messages.

    Args:
        token_1 (str): The first token for authentication.
        token_2 (str): The second token for authentication.

    Returns:
        None
    """
    vk = vk_api.VkApi(token=token_1)
    longpoll = VkLongPoll(vk)

    def write_msg(user_id, mess, keyboard=None, attachment=None):
        if keyboard is not None:
            vk.method('messages.send', {
                'user_id': user_id, 'message': mess, 'random_id': randrange(10 ** 7),
                'keyboard': keyboard, 'attachment': attachment})
        else:
            vk.method('messages.send', {
                'user_id': user_id, 'message': mess, 'random_id': randrange(10 ** 7), 'attachment': attachment})

    user_results = UserResultsStorage()
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                bot = VkBot(event.user_id, token_1, token_2, user_results, DB)
                message, keyboard, attachment = bot.execute_command(event.text)
                write_msg(event.user_id, message, keyboard, attachment)


if __name__ == "__main__":
    tok_1, tok_2, db_name, db_user_name, db_user_password = get_tokens()
    DB = ManageDB(db_name=db_name, user_name=db_user_name,
                  user_password=db_user_password)
    start_vk_bot(tok_1, tok_2)
