#!/usr/bin/env python3
from telegram import ReplyKeyboardMarkup
import collections
import logging as log
import os

from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import Updater

from const import *
import dialogs

class AIDS_bot(object):

    def __init__(self, token):
        self.updater = Updater(token=token)
        handler = MessageHandler(Filters.text | Filters.command, self.handle_message)
        self.updater.dispatcher.add_handler(handler)

    def start(self, generator):
        self.handlers = collections.defaultdict(generator)
        self.updater.start_polling()

    def handle_message(self, bot, update):
        chat_id = update.message.chat_id

        if update.message.text == INIT_MESSAGE:
            self.handlers.pop(chat_id, None)

        if chat_id in self.handlers:
            try:
                print(update.message)
                answer = self.handlers[chat_id].send(update.message)
            except StopIteration as e:
                if e.value:
                    bot.sendMessage(chat_id=chat_id, **e.value)
                else:
                    bot.sendMessage(chat_id=chat_id, text='logout')
                del self.handlers[chat_id]
                return self.handle_message(bot, update)
        else:
            answer = next(self.handlers[chat_id])
        
        bot.sendMessage(chat_id=chat_id, **answer)


if __name__ == '__main__':
    log.basicConfig(level=log.DEBUG)

    dir_path = os.path.dirname(os.path.realpath(__file__))
    f = open(os.path.join(dir_path, 'token'), 'r')
    token = f.read() #'310046588:AAGqktDy4wf71g-wpZD_H84JTJLY7nOD9b8'
    token = token[:-1]
    bot = AIDS_bot(token)
    bot.start(dialogs.login_dialog)
