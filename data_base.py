import redis
from data.card import Card

class DataBase(object):

    singleton_instance = None

    #all object's keys look like type:id
    #and have dict type

    def __init__(self):
        self.conn = redis.Redis('localhost')

    @classmethod
    def instance(cls):
        if not cls.singleton_instance:
            cls.singleton_instance = DataBase()

        return cls.singleton_instance

    def get_card(self, card_id):
        card_dict = self.conn.hgetall('card:%s' % card_id)
        card = Card.card_from_dict(card_dict)
        return card

    def save_card(self, card):
        if not card.card_id: card_id = self._get_id('card')
        card.set_card_id(card_id)
        self.conn.hmset('card:%s' % card_id, card.get_card_dict())
        return card_id

    def delete_card(self, card_id):
        self.conn.delete('card:%s' % card_id)

    def add_user(self, name):
        user_id = self._get_id('user')
        self.conn.hmset('user:%s' % user_id, user)
        return user_id

    def del_user(self, user_id):
        self.conn.delete('user:%s' % user_id)

    def _get_id(self, obj_type):
        obj_list = self.conn.keys(pattern='%s:*' % obj_type)
        if not obj_list:
            obj_id = 0
        else:
            obj_id = max([int(i.decode('utf-8').split(':')[1]) for i in obj_list]) + 1
        return obj_id

if __name__ == '__main__':
    #simple test
    d = DataBase.instance()
    c_id = d.save_card({'1': '2'})
    c_id2 = d.save_card({'3': '4'})
    c = d.get_card(c_id)
    print(c)
