class Card(object):

    card_id = None
    fio = None
    age = None
    month_sum = None
    disease = ""

    def __init__(self, fio, age, month_sum, disease):
        self.fio = fio
        self.age = age
        self.month_sum = month_sum
        self.disease = disease

    @classmethod
    def card_from_dict(cls, card_dict):
        card_id = card_dict['id']
        fio = card_dict['fio']
        age = card_dict['age']
        month_sum = card_dict['month_sum']
        disease = card_dict['disease']
        return Card(card_id, fio, age, month_sum, disease)


    def __str__(self):
        return "id:%s fi:%s age:%s month_sum:%s disease:%s" % (self.card_id, self.fio, self.age, self.month_sum, self.disease)

    def set_card_id(self, card_id):
        self.card_id = card_id

    def get_card_dict(self):
        return {
                'id': str(self.fio),
                'fio': str(self.fio),
                'age': str(self.age),
                'mon_sum': str(self.month_sum),
                'disease': str(self.disease),
               }
