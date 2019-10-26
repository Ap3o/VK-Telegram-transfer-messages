import sqlite3
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll
import random
import config

items = list(range(9999))


def shuffle(items=items):
    random.shuffle(items)
    array = items[:1]
    return array


class VK(object):
    def __init__(self, token, id):
        self.session = vk_api.VkApi(token=token)
        self.session_api = self.session.get_api()
        self.LongPoll = VkBotLongPoll(self.session, id)

    def send_msg(self, peer_id, text):
        self.session_api.messages.send(peer_id=peer_id, message=text, random_id=shuffle())


VkBot = VK(config.vk_token, config.vk_group_id)

conn = sqlite3.connect('mydb.sql', check_same_thread=False)
cursor = conn.cursor()

try:
    cursor.execute(
        'CREATE TABLE log (count INTEGER PRIMARY KEY AUTOINCREMENT, from_id int, event text, \
        date_message text, prefix text, peer_id int, time text, name text, message_text text, full_log text)')
except:
    pass
