import telebot
from datetime import datetime
from server import cursor
from config import telegram_token


bot = telebot.TeleBot(telegram_token, threaded=False)


class NoParameterSpecified(Exception):
    pass


def start_telegram_listen():

    @bot.message_handler(commands=["show"])
    def handle_show(message):
        split_message = message.text.split(" ")

        try:
            prefix = split_message[1]
        except:
            bot.send_message(message.chat.id, "Префикс чата для поиска не указан.")
            return

        try:
            datetime.strptime(split_message[2], "%d.%m.20%y")
            date = split_message[2]
        except:
            bot.send_message(message.chat.id, "День не указан или был введен неверно.")
            return

        try:
            limit = int(split_message[3])
        except:
            bot.send_message(message.chat.id, "Лимит не был введён")
            return
        count = cursor.execute("SELECT COUNT(*) FROM log WHERE prefix = ? AND date_message = ?", (prefix, date)).fetchall()[0][0]

        if int(count) < limit:
            bot.send_message(message.chat.id, "Вы пытаетесь выделить больше записей, чем есть в базе данных.")
            return

        offset = count - limit
        sql = 'SELECT full_log FROM log WHERE (prefix = "%s") AND (date_message = "%s") LIMIT %s OFFSET %s' % (prefix, date, limit, offset)

        cursor.execute(sql)
        result = cursor.fetchall()

        for i in result:
            bot.send_message(message.chat.id, date + ' ' + i[0])

    bot.polling(none_stop=True, interval=0)




