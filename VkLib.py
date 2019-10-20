class GetMessage(object):
    def __init__(self, event, session):
        """
        :param event: Ивент от вк.
        :param session: Сессия, созданная в сервере, нужна для некоторых действий
        """
        self.event = event
        self.session = session

    def getName(self, user_id=None):
        if user_id is None:
            user_id = self.event.obj.from_id
        if user_id > 0:
            request = self.session.method('users.get', {'user_ids': user_id, 'fields': 'first_name'})
            return request[0]['first_name'] + ' ' + request[0]['last_name']
        else:
            return "Some Bot"

    def getText(self):
        return self.event.obj.text

    def getAttachments(self, attachments=None):

        if attachments is None:
            attachments = self.event.obj.attachments
        if len(attachments) != 0:
            answer = ''
            for attachment in attachments:
                if attachment['type'] == 'sticker':  # Стикер
                    # -128b-9 Постоянное качество стикера.
                    investment = 'https://vk.com/sticker/1-' + str(attachment['sticker']['sticker_id']) + '-128b-9'
                elif attachment['type'] == 'video':  # Вложенное видео
                    investment = 'https://vk.com/video' + str(attachment['video']['owner_id']) + '_' + str(
                        attachment['video']['id'])
                elif attachment['type'] == 'wall':  # Вложенный пост
                    investment = 'https://vk.com/wall' + str(attachment['wall']['to_id']) + '_' + str(
                        attachment['wall']['id'])
                elif attachment['type'] == 'audio':  # Вложенное аудио
                    investment = '[🔊] ' + str(attachment['audio']['artist']) + ' — ' + str(
                        attachment['audio']['title'])
                elif attachment['type'] == 'photo':  # Вложенное фото
                    data = []
                    for size in attachment['photo']['sizes']:
                        data.append(size['width'] * size['height'])
                    investment = attachment['photo']['sizes'][data.index(max(data))]['url']
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
                answer = answer + investment + '\n'
            return "\n[Вложения]\n" + answer
        else:
            return ''

    def getReply(self, reply=None):
        if reply is None:
            reply = self.event.obj.reply_message

        fwd = ''
        if 'fwd_messages' in reply:
            fwd = self.getFwd(reply['fwd_messages'], "[FWD IN REPLY]")

        reply_user_name = self.getName(reply['from_id']) + ": "
        reply_text = reply['text']
        reply_attachments = self.getAttachments(reply['attachments'])

        reply_message = reply_user_name + reply_text + reply_attachments + fwd

        return "\n[REPLY]\n" + reply_message

    def getFwd(self, fwd=None, prefix="\n[FWD]\n"):

        if fwd is None:
            fwd = self.event.obj.fwd_messages

        full_message = ''
        print(fwd)
        for message in fwd:
            next_fwd = ''
            if 'fwd_messages' in message:
                next_fwd = self.getFwd(message['fwd_messages'], "[FWD IN FWD]\n")
            full_message = full_message + self.getName(message['from_id']) + ": " + message['text'] + \
                           self.getAttachments(message['attachments']) + '\n' + next_fwd
        return prefix + full_message
