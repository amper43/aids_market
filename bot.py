#!/usr/bin/env python3
import collections
import logging as log

from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import Updater


class AIDS_bot(object):

    def __init__(self, token, generator):
        self.updater = Updater(token=token)
        handler = MessageHandler(Filters.text | Filters.command, self.handle_message)
        self.updater.dispatcher.add_handler(handler)
        self.handlers = collections.defaultdict(generator)


    def start(self):
        self.updater.start_polling()


    def handle_message(self, bot, update):
        log.debug("Received {} from {}".format(update.message, update.chat_id))
        chat_id = update.message.chat_id
        if update.message.text == "/start":


            self.handlers.pop(chat_id, None)
        if chat_id in self.handlers:


            try:
                answer = self.handlers[chat_id].send(update.message)
            except StopIteration:

                del self.handlers[chat_id]

                return self.handle_message(bot, update)
        else:



            answer = next(self.handlers[chat_id])
        
        bot.sendMessage(chat_id=chat_id, text=answer)


def dialog():
    answer = yield "hello. what is your name?"
    log.debug("Answer {}".format(answer.text))


if __name__ == '__main__':
    token = '310046588:AAGqktDy4wf71g-wpZD_H84JTJLY7nOD9b8'
    bot = AIDS_bot(token, dialog)
    bot.start()
