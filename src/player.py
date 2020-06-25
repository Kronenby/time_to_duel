import card
import card_data
from random import *

def generate_base_deck(nb_cards):
    decklist = []
    checklist = []
    for i in range(card_data.data_length()-2):
        checklist.append(0)
    for i in range(nb_cards):
        id_card = randrange(0,card_data.data_length()-2)
        checklist[id_card]+=1
        if checklist[id_card] > 3:
            i-=1
        else:
            decklist.append(card.Card(id_card))
    return decklist

class Player:
    def __init__(self):
        self._deck = generate_base_deck(20)
        self.normal_summons = 0

    def draw(self):
        input("any input to draw:\n")
