from threading import Thread
from logbot import log_bot


def start_log():
    log_bot()


thread1 = Thread(target=start_log)
thread1.start()
thread1.join()
