import server
import VkLib
from datetime import datetime
from threading import Thread
from vk_api.bot_longpoll import VkBotEventType
from colorama import Fore, Style
from config import DEBUG, logging_in_db
from modules.connect_telegram import bot


def get_log(event, chat_transfer, prefix='', session=server.session):  # name = префикс, если бесед несколько.
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

    log = prefix + ' ' + time + " | " + name + ": " + text + attachments + fwd + reply
    if DEBUG:
        print(event)
        print(log)
    else:
        bot.send_message(chat_id=chat_transfer, text=log)

    if logging_in_db:  # Запись в БД
        log_in_db(event, prefix, time, name, text, log)


def log_in_db(event, prefix, time, name, text,  full_log):
    server.cursor.execute("INSERT INTO log (from_id, event, prefix, peer_id, time, name, message_text, full_log, date_message) VALUES \
    (?, ?, ?, ?, ?, ?, ?, ?, ?)", (int(event.obj.from_id), str(event), str(prefix), int(event.obj.peer_id), str(time), name, text, full_log, str(datetime.strftime(datetime.today(), "%d.%m.20%y"))))
    server.conn.commit()


def log_bot():
    try:
        for event in server.LongPoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                Thread_ = Thread(target=get_log, args=(event, 326594028, "[PM]"))
                Thread_.start()
    except Exception as e:
        print(Fore.RED, "Exception: ", e, Style.RESET_ALL)
        log_bot()
