import sqlite3
from datetime import datetime
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll

import config


class VK(object):
    def __init__(self, token, id):
        self.session = vk_api.VkApi(token=token)
        self.session_api = self.session.get_api()
        self.LongPoll = VkBotLongPoll(self.session, id)

    # TODO
    def send_msg(self):
        pass


VkBot = VK(config.vk_token, config.vk_group_id)

conn = sqlite3.connect('mydb.sql', check_same_thread=False)
cursor = conn.cursor()

try:
    cursor.execute(
        'CREATE TABLE log (count INTEGER PRIMARY KEY AUTOINCREMENT, from_id int, event text, \
        date_message text, prefix text, peer_id int, time text, name text, message_text text, full_log text)')
except:
    pass
