from threading import Thread
from logbot import log_bot
from modules.connect_telegram import start_telegram_listen


thread1 = Thread(target=log_bot)
thread1.start()

thread2 = Thread(target=start_telegram_listen)
thread2.start()

