import sys
from telegram import ReplyMarkup, KeyboardButton

from const import *

def login_dialog():
    user = yield {'text': START_MESSAGE}
    user = user.text
    if user in USERS:
        yield from getattr(sys.modules[__name__], user)()
    else: yield {'text': "%s %s" % (user, USER_NOT_EXIST)}

def operator():
    yield {'test': , 'reply_markup': ReplyKeyboardMarkup([[1]], one_time_keyboard=True)}
    pass

def doctor():
    pass

def courier():
    pass

def admin():
    pass
