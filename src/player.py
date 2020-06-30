import card
import card_data
from random import *
from TermDisplay import *

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

class TermPlayer:
    def __init__(self,name):
        self._deck = generate_base_deck(20)
        self._normal_summons = 0
        self._name = name

    ### A VIRER?
    def get_id(self, board):
        for i in range(len(board._players)):
            if board._players[i]._name == self._name:
                return i
        print("player not in the game")
        return None
        
    def draw(self):
        input("any input to draw:\n")

    def accept_defeat(self, cause):
        input("any input to accept defeat :(\n")
    
    def get_input(self, board, player, actions):
        char = None
        str_actions = ["display", "view"]
        for string in actions:
            if char != string[0]:
                char = string[0]
                if char == 'g':
                    str_actions.append("give up")
                elif char == 'e':                 
                   str_actions.append("end turn")
                elif char == 'b':                    
                   str_actions.append("battle phase")
                elif char == 'n':                    
                   str_actions.append("normal summon")
                elif char == 's':                    
                   str_actions.append("set face-down")
                elif char == 'c':                    
                   str_actions.append("change position")
                elif char == 'a':                    
                   str_actions.append("attack")
        
        while True:
            print("['v', 'd'] + "+str(actions))
            print(str_actions)
            choice = input("what to do now? (enter first letter to chose)\n")
            if choice in actions:
                return choice
            elif choice == "d":
                display_all(board)
            elif choice == "v":
                while True:
                    pick = input("view a cemetary (C/c), your hand (h), or a field (F/f)?\n")
                    if pick == "r":
                        break
                    elif pick == "C":
                        len = display_cemetary(board, player,1)
                        if len == 0:
                            print("nothing to see here")
                        break
                    elif pick == "c":
                        len = display_cemetary(board, player,0)
                        if len == 0:
                            print("nothing to see here")
                        break
                    elif pick == "h":
                        display_hand(board, player)
                        break
                    elif pick == "F":
                        display_field(board, player,1)
                        break
                    elif pick == "f":
                        display_field(board, player,0)
                        break
                    else:
                        print("wrong input, try again")
            if choice == "n":
                while True:
                    display_hand(board, player)
                    pick = input("which card to summon? (enter a number or r to return to main phase)\n")
                    if pick=="r":
                        break
                    finalchoice = choice + " " + pick
                    if finalchoice not in actions:
                        print("invalid move, try again")
                    else:
                        return finalchoice
            if choice == "s":
                while True:
                    display_hand(board, player)
                    pick = input("which card to set face-down? (enter a number or r to return to main phase)\n")
                    if pick=="r":
                        break
                    finalchoice = choice + " " + pick
                    if finalchoice not in actions:
                        print("invalid move, try again")
                    else:
                        return finalchoice
            if choice == "c":
                while True:
                    display_switchable(board, player)
                    pick = input("which monster to switch position? (enter a number or r to return to main phase)\n")
                    if pick == "r":
                        break
                    finalchoice = choice + " " + pick
                    if finalchoice not in actions:
                        print("invalid move, try again")
                    else:
                        return finalchoice
            if choice == "a":
                while True:
                    display_attackers(board, player)
                    pick_a = input("which monster will attack? (enter a number or r to return to battle phase)\n")
                    if pick_a=="r":
                        break
                    choice_a = choice + " " + pick_a
                    if choice_a in actions:
                        return choice_a
                    if not pick_a.isnumeric():
                        print("don't enter letters beside r")
                        continue
                    attacker = int(pick_a)
                    if not board.check_attacker(player,attacker-1):
                        print("wrong number, try again")
                        continue
                    while True:
                        display_targets(board, player)
                        pick_t = input("what is the target? (enter a number or r to return to attacker picking)\n")
                        if pick_t=="r":
                            break
                        finalchoice = choice_a + " " + pick_t
                        if finalchoice not in actions:
                            print("wrong target, try again")
                            continue
                        else:
                            return finalchoice

    def choose_discard(self, board, player, nb):
        while True:
            display_hand(board, player)
            pick = input("you have "+str(nb)+" too many cards. Discard these to end turn.\n")
            if not pick.isnumeric():
                print("enter a number")
                continue
            if (int(pick)-1) in list(range(len(board._hand[player]))):
                return pick
            print("this id is not in your hand")
            