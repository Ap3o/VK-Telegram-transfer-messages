import sqlite3

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll

import config

moder_session = vk_api.VkApi(token=config.vk_token)
session_api_moder = moder_session.get_api()
LongPoll_Moder = VkBotLongPoll(moder_session, config.vk_group_id)

conn = sqlite3.connect('mydb.sql', check_same_thread=False)
cursor = conn.cursor()
