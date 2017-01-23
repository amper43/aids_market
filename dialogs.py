import sys
import logging as log
from telegram import ReplyKeyboardMarkup

from const import *

def login_dialog():
    user = yield {'text': START_MESSAGE}
    user = user.text
    if user in USERS:
        yield from getattr(sys.modules[__name__], user)()
    else: yield {'text': "%s %s" % (user, USER_NOT_EXIST)}

def operator():
    command = yield {'text': OPERATOR_START, 'reply_markup': ReplyKeyboardMarkup([[OPERATOR_CLIENT_REGISTRATION],[DELETE]], one_time_keyboard=True)}
    log.debug("COMMAND %s" % command)

def doctor():
    command = yield {'text': DOCTOR_START,
                     'reply_markup': ReplyKeyboardMarkup([[UPDATE_HISTORY], [DELETE_HISTORY],[SHOW_HISTORY],[CREATE_HISTORY]],
                                                         one_time_keyboard=True)}
    log.debug("COMMAND %s" % command)

def courier():
    pass

def admin():
    pass
