import sys
import logging as log
from telegram import ReplyKeyboardMarkup

from const import *
#from data.card import Card
from data_base import DataBase
from card import Card

db = DataBase.instance()

def _send(text, keyboard = None, location = None):
    
    if keyboard:
        keyboard = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    ret = {'text': text, 'reply_markup': keyboard, 'location': location}
    return ret

def login_dialog(sender=None):
    user = yield _send('Enter login:password')
    try:
        login, password = user.text.split(':')
    except:
        return _send('wrong credentials')
    if db.process_creds(login, password):
        user = login
    else:
        return _send('wrong credentials')
    if user in USERS:
        ret = None
        while ret != EXIT:
            ret = yield from getattr(sys.modules[__name__], user)(sender)
    else: return _send("no dialogs for {}".format(user))

def operator(sender=None):
    command = yield _send(OPERATOR_START, [[OPERATOR_CLIENT_REGISTRATION],[SHOW_ALL_CLIENTS],[SHOW_ALL_COURIERS], [DELETE_CLIENT],
                                           [CREATE_MESSAGE],[SET_TIMETABLE], [EXIT]])
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

    if command.text == DELETE_CLIENT:
        
        card_id = yield _send(OPERATOR_REMOVING_PROFILE)
        a = db.delete_card(card_id.text)
        if (a != 0):
            print(a)
            yield _send('success')
        else:
            yield _send('delete error')
        
    if command.text == SHOW_ALL_CLIENTS:
        client_list = db.show_all_client_ids()
        if client_list != "":
            yield _send("<i>CLIENT'S ID LIST:</i> \n" + client_list)
        else:
            yield _send("No client's profiles in system!")
            
    if command.text == SHOW_ALL_COURIERS:
        courier_list = db.courier_id_list()
        yield _send("COURIER'S ID LIST: \n" + courier_list)
        
    
    if command.text == CREATE_MESSAGE:
        cour_id = yield _send("Input courier's ID for sending message:\n")
        mes = yield _send("Input message for this courier:\n")
        try:
            db.set_message(int(cour_id.text), mes.text)
        except:
            yield _send("Sending Error!")
            
    if command.text == SET_TIMETABLE:
        cour_id = yield _send("Input courier's ID for sending message:\n")
        scheldue = yield _send("Input data of scheldue for couriers:\n")
        try:
            if int(cour_id.text) < 0:
                yield _send('error, ID is invalid')
            db.set_timetable(cour_id.text, scheldue.text)
            yield _send('success')
        except:
            yield _send('error')
        
        

    if command.text == EXIT:
        return EXIT

    return _send(COMMAND_NOT_EXIST)


def doctor(sender=None):
    command  = yield _send(DOCTOR_START, [[DOCTOR_PROC], [EXIT]])
    if command.text == EXIT:
        return EXIT

    while command.text != EXIT:
        client_id = yield _send(DOCTOR_ID_INPUT)
        client_id = client_id.text
        cli_id_list = db.show_all_client_ids().split("\n")
        if client_id in cli_id_list:
            while command.text != EXIT:
                command = yield _send(DOCTOR_CHOSE_OPERATION,[[UPDATE_HISTORY], [SHOW_HISTORY], [CREATE_HISTORY], [EXIT]])
    
                if command.text == UPDATE_HISTORY:
                    card = db.get_card(client_id)
                    disease = yield _send("%s\n%s\n\n%s" % (DOCTOR_VIEW_PROFILE, card.disease, DOCTOR_UPDATE_PROFILE))
                    card.disease = disease.text
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
        else:
            yield _send("Client with this ID is not exist")
            break


def courier(sender=None):
    courier_id = yield _send('enter your id')
    command = yield _send(START_COURIER, [[CHECK_MESSAGE], [SHOW_TIMETABLE], [EXIT]])


    while command.text != EXIT:
        if command.text == CHECK_MESSAGE:
            msg = db.get_message(courier_id.text)
            yield _send(msg)
        elif command.text == SHOW_TIMETABLE:
            tt = db.get_timetable(courier_id.text)
            yield _send(tt, location=(59.9524056,30.3006592))
        command = yield _send(START_COURIER, [[CHECK_MESSAGE], [SHOW_TIMETABLE], [EXIT]])
    return EXIT



def admin(sender=None):

    
    command = yield _send('admin, enter command', [['add user'], ['del user'],["show all users"], [EXIT]])

    if command.text == EXIT:
        return EXIT

    while command.text != EXIT:
        if command.text == 'add user':
            user = yield _send('enter user')
            password = yield _send('enter password')
            db.add_account(user.text, password.text)

        elif command.text == 'del user':
            user = yield _send('enter user')
            a = db.del_account(user.text)
            if (a == 1):
                yield _send("User '" + user.text + "' deleted!")
            else:
                yield _send("Deleting Error! User is not exist!")
        
        elif command.text == 'show all users':
            user_list = db.show_users()
            yield _send("Registred users of sysem:" + "\n" + user_list)

        command = yield _send('admin, enter command', [['add user'], ['del user'], ["show all users"], [EXIT]])
