import sys
import logging as log
from telegram import ReplyKeyboardMarkup

from const import *

def _send(text, keyboard=None):

    if keyboard:
        keyboard = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    ret = {'text': text, 'reply_markup': keyboard}
    return ret

def login_dialog():
    user = yield _send(START_MESSAGE)
    user = user.text
    if user in USERS:
        yield from getattr(sys.modules[__name__], user)()
    else: yield _send("%s %s" % (user, USER_NOT_EXIST))

def operator():
<<<<<<< HEAD
    command = yield {'text': OPERATOR_START, 'reply_markup': ReplyKeyboardMarkup([[OPERATOR_CLIENT_REGISTRATION],[DELETE]], one_time_keyboard=True)}
    log.debug("COMMAND %s" % command)
=======
    command = yield _send(OPERATOR_START, [[OPERATOR_CLIENT_REGISTRATION],[OPERATOR_REMOVING_PROFILE]])
    return
    if command.text == OPERATOR_CLIENT_REGISTRATION:
        pass

    if command.text == OPERATOR_REMOVING_PROFILE:
        pass

    yield {'text': 'wrong answer'}
>>>>>>> fe4c9097e6cf2a49a285798310d711295883b1a2

def doctor():
    command = yield {'text': DOCTOR_START,
                     'reply_markup': ReplyKeyboardMarkup([[UPDATE_HISTORY], [DELETE_HISTORY],[SHOW_HISTORY],[CREATE_HISTORY]],
                                                         one_time_keyboard=True)}
    log.debug("COMMAND %s" % command)

def courier():
    pass

def admin():
    pass
