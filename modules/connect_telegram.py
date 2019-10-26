import telebot
import os
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

        if len(split_message) > 4:
            write_as_file = True
        else:
            write_as_file = False

        if int(count) < limit:
            bot.send_message(message.chat.id, "Вы пытаетесь выделить больше записей, чем есть в базе данных.")
            return

        offset = count - limit
        sql = 'SELECT full_log FROM log WHERE (prefix = "%s") AND (date_message = "%s") LIMIT %s OFFSET %s' % (prefix, date, limit, offset)

        cursor.execute(sql)
        result = cursor.fetchall()
        if write_as_file:
            text = ''
            for i in result:
                text = text + date + ' ' + i[0] + '\n' + ("*" * 50) + '\n'
            text = sql + '\n\n' + text
            file_name = "log_{0}_{1}.txt".format(prefix, date)
            with open("modules/" + file_name, "w", encoding="UTF-8") as file:
                file.write(str(text))
            bot.send_document(message.chat.id, open("modules/" + file_name, encoding="UTF-8"))
            os.remove("modules/" + file_name)
        else:
            for i in result:
                bot.send_message(message.chat.id, date + ' ' + i[0])

        @bot.message_handler(commands=["id"])
        def _id(message):
            bot.send_message(message.chat.id, message.chat.id)

    @bot.message_handler(commands=["sql"])
    def sql(message):
        try:
            sql = message.text.split(" ", 1)[1]
        except:
            bot.send_message(message.chat.id, "Вы не указали sql запрос.")
            return
        try:
            cursor.execute(sql)
            result = cursor.fetchall()
        except Exception as e:
            bot.send_message(message.chat.id, "Произошла ошибка при выполнении запроса:\n" + str(e))
            return
        text = ''
        for i in result:
            text = text + str(i[0]) + '\n'
        file_name = 'SQL-{0}'.format(datetime.strftime(datetime.now(), "%d-%m-20%y"))
        with open("modules/" + file_name, "w", encoding="UTF-8") as file:
            file.write(str(text))
        bot.send_document(message.chat.id, open("modules/" + file_name, encoding="UTF-8"))
        os.remove("modules/" + file_name)
    bot.polling(none_stop=True, interval=0)




