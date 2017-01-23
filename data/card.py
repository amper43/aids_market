class Card(object):

    fio = None
    age = None
    month_sum = None
    disease = ""

    def __init__(self, fio, age, month_sum):

        self.fio = fio
        self.age = age
        self.month_sum = month_sum

    def __str__(self):
        return "%s %s %s %s" % (self.fio, self.age, self.month_sum, self.disease)
