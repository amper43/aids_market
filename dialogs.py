import sys
import logging as log
from telegram import ReplyKeyboardMarkup

from const import *
from data.card import Card
from data_base import DataBase

db = DataBase.instance()

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
        while ret != EXIT:
            ret = yield from getattr(sys.modules[__name__], user)()
    else: yield _send("%s %s" % (user, USER_NOT_EXIST))

def operator():
    command = yield _send(OPERATOR_START, [[OPERATOR_CLIENT_REGISTRATION],[OPERATOR_REMOVING_PROFILE], [EXIT]])
    if command.text == OPERATOR_CLIENT_REGISTRATION:
        fio = yield _send(OPERATOR_FIO)
        fio = fio.text
        age = yield _send(OPERATOR_AGE)
        age = age.text
        mon_sum = yield _send(OPERATOR_SUM)
        mon_sum = mon_sum.text
        card = Card(fio, age, mon_sum, "")
        card_id = db.save_card(card)
        card.set_card_id(card_id)
        yield _send(str(card))
        return

    if command.text == OPERATOR_REMOVING_PROFILE:
        card_id = yield _send(OPERATOR_REMOVING_PROFILE)
        db.delete_card(card_id)
        return

    if command.text == EXIT:
        return EXIT

    yield _send(COMMAND_NOT_EXIST)


def doctor():
    client_id = yield _send(DOCTOR_START)
    command = yield _send(DOCTOR_CHOSE_OPERATION,[[UPDATE_HISTORY], [SHOW_HISTORY], [CREATE_HISTORY], [EXIT]])

    if command.text == UPDATE_HISTORY:
        card = db.get_card(client_id)
        disease = yield _send("%s\n%s\n\n%s" % (DOCTOR_VIEW_PROFILE, card.disease, DOCTOR_UPDATE_PROFILE))
        card.disease = disease
        db.save_card(card)
        yield _send(DOCTOR_UPDATE_TEXT_OK)

    elif command.text == SHOW_HISTORY:
        card = db.get_card(client_id)
        yield _send("%s\n%s" % (DOCTOR_VIEW_PROFILE, card.disease))

    elif command.text == DELETE_HISTORY:
        card = db.get_card(client_id)
        card.disease = ""
        db.save_card(card)
        yield _send(DELETE_OK)

    elif command.text == CREATE_HISTORY:
        disease = yield _send(DOCTOR_CREATE_HISTORY)
        disease = disease.text
        card = db.get_card(client_id)
        card.disease = disease
        db.save_card(card)
        yield _send(str(card))

    elif command.text == EXIT:
        return EXIT

def courier():
    command = yield _send(START_COURIER, [[CHECK_MESSAGE], [SHOW_TIMETABLE]])

def admin():
    pass
