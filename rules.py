from const import *


operation_map = {USERS[0]:[REGISTRATION,FIO,AGE,SUM],
				 USERS[1]:[UPDATE_HISTORY,SHOW_HISTORY,CREATE_HISTORY,DELETE_HISTORY],
				 USERS[2]:[CHECK_MESSAGE,SHOW_TIMETABLE]};


def user_operations(user, operation):
 	if(user in operation_map):
		if operation in operation_map[user]:
			return True
		else:
			return False
 	else:
 	 return False


