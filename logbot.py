from datetime import datetime
from threading import Thread

from vk_api.bot_longpoll import VkBotEventType

import server
from config import DEBUG


def get_fwd_message(fwd_message, attach):
    if len(fwd_message) != 0:
        message = ''
        second_fwd = ''
        for msg in fwd_message:
            if 'fwd_messages' in msg:
                second_fwd = get_fwd_message(msg['fwd_messages'], '\n[Пересланное сообщение внутри пересланного]\n')
            message = message + get_name(msg['from_id']) + msg['text'] + get_attachments(msg['attachments'],
                                                                                         '\n[Вложение в пересланном сообщении]\n') + '\n' + second_fwd
        messages = attach + message
        return messages
    else:
        return ''


def get_reply_message(reply_message):
    fwd = ''
    if 'fwd_messages' in reply_message:
        fwd = get_fwd_message(reply_message['fwd_messages'], '\n[Пересланное сообщение]\n')
    message = '\n[В ответ]\n' + get_name(reply_message['from_id']) + reply_message['text'] + \
              get_attachments(reply_message['attachments'], '\n[REPLY_Attachments]\n') + fwd
    return message


def get_attachments(attachments, attach):
    if len(attachments) != 0:
        all_attachments = ''
        for attachment in attachments:
            if attachment['type'] == 'sticker':  # Стикер
                # -128b-9 Постоянное качество стикера.
                investment = 'https://vk.com/sticker/1-' + str(attachment['sticker']['sticker_id']) + '-128b-9' + '\n'
            elif attachment['type'] == 'video':  # Вложенное видео
                investment = 'https://vk.com/video' + str(attachment['video']['owner_id']) + '_' + str(
                    attachment['video']['id'])
            elif attachment['type'] == 'wall':  # Вложенный пост
                investment = 'https://vk.com/wall' + str(attachment['wall']['to_id']) + '_' + str(
                    attachment['wall']['id'])
            elif attachment['type'] == 'audio':  # Вложенное аудио
                investment = '[🔊] ' + str(attachments[0]['audio']['artist']) + ' — ' + str(
                    attachments[0]['audio']['title'])
            elif attachment['type'] == 'photo':  # Вложенное фото
                data = []
                pos = 0
                for size in attachment['photo']['sizes']:
                    data.append(size['width'] * size['height'])
                maximum = data[0]
                for i in range(len(data)):
                    if data[i] > maximum:
                        maximum = data[i]
                        pos = i
                investment = attachment['photo']['sizes'][pos]['url']
            elif attachment['type'] == 'link':  # Вложенная ссылка, которая отобразилась после сообщения.
                investment = str(attachment['link']['url'])
            elif attachment['type'] == 'doc':  # Вложенный документ
                investment = 'https://vk.com/doc' + str(attachment['doc']['owner_id']) + '_' + str(
                    attachment['doc']['id'])
            elif attachment['type'] == 'audio_message':  # Голосовое сообщение
                investment = str(attachment['audio_message']['link_mp3'])
            else:
                print(attachment)
                investment = 'Неизвестное вложение: ' + attachment['type']
            all_attachments = all_attachments + investment + '\n'
        all_attachments = attach + all_attachments
        return all_attachments
    else:
        return ''


def get_name(user_id):
    if user_id > 0:
        request = server.moder_session.method('users.get', {'user_ids': user_id, 'fields': 'first_name'})
        return request[0]['first_name'] + ' ' + request[0]['last_name'] + ': '
    else:
        return "Some Bot: "


def get_log(event, name=''):  # name = префикс, если бесед несколько.
    reply = ''
    if 'reply_message' in event.obj:
        reply = (get_reply_message(event.obj.reply_message))
    log = name + \
          datetime.strftime(datetime.now(), "%H:%M:%S") + ' | ' + (
                      get_name(event.obj.from_id) + event.obj.text + get_attachments(event.obj.attachments,
                                                                                     '\n[Вложения]\n')) + get_fwd_message(
        event.obj.fwd_messages, '\n[FWD]\n') + reply
    print(log)
    return log


def log_bot():
    print('LogBot on')
    for event in server.LongPoll_Moder.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            log = get_log(event, '')
            if DEBUG:
                print(event)
