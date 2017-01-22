def login_dialog():
    user = yield START_MESSAGE
    user = user.text
    if user in USERS:
        yield "ok"
    else: yield "%s %s" % (user, USER_NOT_EXIST)

def operator():
    pass

def doctor():
    pass

def courier():
    pass

def admin():
    pass
