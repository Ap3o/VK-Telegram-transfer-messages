import sqlite3

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll

import config

session = vk_api.VkApi(token=config.vk_token)
session_api = session.get_api()
LongPoll = VkBotLongPoll(session, config.vk_group_id)

conn = sqlite3.connect('mydb.sql', check_same_thread=False)
cursor = conn.cursor()
