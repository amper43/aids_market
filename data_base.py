from data.card import Card

class DataBase(object):


    def __init__(self):
        pass

    def get_card(self, card_id):
        return Card(0, 'test', 'test', '41', '300', 'history')

    def save_card(self, card):
        return 0 #card id

    def add_user(self):
        pass

    def del_user(self):
        pass

