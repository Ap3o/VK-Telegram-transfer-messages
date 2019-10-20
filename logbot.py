import server
import VkLib
from datetime import datetime
from threading import Thread
from vk_api.bot_longpoll import VkBotEventType
from colorama import Fore, Style
from config import DEBUG
from modules.connect_telegram import bot


def get_log(event, prefix='', session=server.moder_session):  # name = префикс, если бесед несколько.
    message = VkLib.GetMessage(event, session)
    time = datetime.strftime(datetime.now(), "%H:%M")
    name = message.getName()
    text = message.getText()
    attachments = message.getAttachments()

    if len(event.obj.fwd_messages) != 0:
        fwd = message.getFwd()
    else:
        fwd = ''

    if "reply_message" in event.obj:
        reply = message.getReply()
    else:
        reply = ''

    log = prefix + time + " | " + name + ": " + text + attachments + fwd + reply
    if DEBUG:
        print(event)
        print(log)
    else:
        bot.send_message(chat_id=326594028, text=log)


def log_bot():
    try:
        for event in server.LongPoll_Moder.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                Thread_ = Thread(target=get_log, args=(event, "[PM] "))
                Thread_.start()
    except Exception as e:
        print(Fore.RED, "Exception: ", e, Style.RESET_ALL)
        log_bot()
