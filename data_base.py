#!/usr/bin/env python3
import redis
import logging as log
#from data.card import Card

class DataBase(object):

    singleton_instance = None

    #all object's keys look like type:id
    #and have dict type

    def __init__(self):
        self.conn = redis.Redis('localhost', decode_responses=True)

    @classmethod
    def instance(cls):
        if not cls.singleton_instance:
            cls.singleton_instance = DataBase()

        return cls.singleton_instance

    def get_card(self, card_id):
        log.debug('DataBase:get_card:card_id: %s' % card_id)
        card_dict = self.conn.hgetall('card:%s' % card_id)
        log.debug('DataBase:get_card:card_dict: %s' % card_dict)
        card = Card.card_from_dict(card_dict)
        return card

    def save_card(self, card):
        if not card.card_id: card_id = self._get_id('card')
        else: card_id = card.card_id
        card.set_card_id(card_id)
        self.conn.hmset('card:%s' % card_id, card.get_card_dict())
        return card_id

    def delete_card(self, card_id):
        self.conn.delete('card:%s' % card_id)
        log.info('{} card deleted'.format(card_id))

    def add_user(self, name):
        user_id = self._get_id('user')
        self.conn.hmset('user:%s' % user_id, name)
        return user_id

    def del_user(self, user_id):
        self.conn.delete('user:%s' % user_id)

    def _get_id(self, obj_type):
        obj_list = self.conn.keys(pattern='%s:*' % obj_type)
        if not obj_list:
            obj_id = 0
        else:
            obj_id = max([int(i.split(':')[1]) for i in obj_list]) + 1
        return obj_id

    def get_message(self, courier_id):
        return self.conn.get('courier:message:{}'.format(courier_id))

    def set_message(self, courier_id, msg):
        self.conn.set('courier:message:{}'.format(courier_id), msg)

    def get_timetable(self, courier_id):
        return self.conn.get('courier:timetable:{}'.format(courier_id))

    def set_timetable(self, courier_id, tt):
        self.conn.set('courier:timetable:{}'.format(courier_id), tt)

    def process_creds(self, login, password):
        return password == self.conn.get('user:{}'.format(login, password))

    def add_account(self, name, password):
        self.conn.set('user:{}'.format(name), password)

    def del_account(self, name):
        self.conn.delete('user:{}'.format(name))


if __name__ == '__main__':
    #simple test
    import sys
    d = DataBase.instance()
    method = sys.argv[1]

    if len(sys.argv) > 2:
        arg = sys.argv[2:]
        ret = getattr(d, method)(*arg)
        print(ret)
        sys.exit(0)
        
    ret = getattr(d, method)()
    print(ret)
