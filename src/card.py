import card_data

class Card:
    def __init__(self,id):
        data = card_data.get_data(id)
        self._name = data[0]
        self._stats = [data[1], data[2]]

    def print_details(self):
        print(self._name + ": "+str(self._stats[0])+" ATK, "+str(self._stats[1])+" DEF")