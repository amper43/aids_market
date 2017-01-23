import sys
import logging as log
from telegram import ReplyKeyboardMarkup

from const import *
from data.card import Card

c = Card

def _send(text, keyboard=None):

    if keyboard:
        keyboard = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    ret = {'text': text, 'reply_markup': keyboard}
    return ret

def login_dialog():
    user = yield _send(START_MESSAGE)
    user = user.text
    if user in USERS:
        ret = None
        while ret != 'exit':
            ret = yield from getattr(sys.modules[__name__], user)()
    else: yield _send("%s %s" % (user, USER_NOT_EXIST))

def operator():
    command = yield _send(OPERATOR_START, [[OPERATOR_CLIENT_REGISTRATION],[OPERATOR_REMOVING_PROFILE]])
    if command.text == OPERATOR_CLIENT_REGISTRATION:
        fio = yield _send(OPERATOR_FIO)
        fio = fio.text
        age = yield _send(OPERATOR_AGE)
        age = age.text
        mon_sum = yield _send(OPERATOR_SUM)
        mon_sum = mon_sum.text
        card = Card(str(fio), str(age), str(mon_sum))
        yield _send(str(card))
        return

    if command.text == OPERATOR_REMOVING_PROFILE:
        return

    yield {'text': 'wrong answer'}


def doctor():
    command = yield {'text': DOCTOR_START,
                     'reply_markup': ReplyKeyboardMarkup([[UPDATE_HISTORY], [DELETE_HISTORY],[SHOW_HISTORY],[CREATE_HISTORY],[EXIT]],
                                                         one_time_keyboard=True)}
    if command.text == UPDATE_HISTORY:
        yield _send(DOCTOR_UPDATE_PROFILE)
    elif command.text == SHOW_HISTORY:
        yield _send(DOCTOR_VIEW_PROFILE)
    elif command.text == DELETE_HISTORY:
        yield _send(DELETE_OK)
    elif command.text == CREATE_HISTORY:
        disease = yield _send(DOCTOR_CREATE_HISTORY)
        disease = disease.text
        card = Card(None,None,None,disease)
        yield _send(str(card))
    log.debug("COMMAND %s" % command)

def courier():
    command = yield _send(START_COURIER, [[CHECK_MESSAGE], [SHOW_TIMETABLE]])

def admin():
    pass
