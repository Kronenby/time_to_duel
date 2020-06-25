from random import *
import board
import player

nextphase = None

def print_phase(phase):
    print("----"+phase+" PHASE----")

def handle_input(choice, actions, board, current_player):
    global nextphase
    if choice not in actions:
        print("wrong input, try again.")
        return 1
    if choice == "g":
        print("player "+board.color(current_player)+" gave up")
        quit()
    if choice == "b":
        nextphase = _BATTLE
        return 0
    if choice == "e":
        nextphase = _END
        return 0
    if choice == "d":
        board.display_all()
        return 1
    if choice == "v":
        while True:
            pick = input("view a cemetary (C/c), your hand (h), or a field (F/f)?\n")
            if pick == "r":
                break
            elif pick == "C":
                len = board.display_cemetary(current_player,1)
                if len == 0:
                    print("nothing to see here")
                break
            elif pick == "c":
                len = board.display_cemetary(current_player,0)
                if len == 0:
                    print("nothing to see here")
                break
            elif pick == "h":
                board.display_hand(current_player)
                break
            elif pick == "F":
                board.display_field(current_player,1)
                break
            elif pick == "f":
                board.display_field(current_player,0)
                break
            else:
                print("wrong input, try again")
        return 1
    if choice == "n":
        while True:
            board.display_hand(current_player)
            pick = input("which card to summon? (enter a number or r to return to main phase)\n")
            if pick=="r":
                break
            if not pick.isnumeric():
                print("don't enter letters beside r")
                continue
            if board.nsummon(current_player,int(pick)-1):
                break
        return 1
    if choice == "c":
        while True:
            board.display_switchable(current_player)
            pick = input("which monster to switch position? (enter a number or r to return to main phase)\n")
            if pick == "r":
                break
            if not pick.isnumeric():
                print("don't enter letters beside r")
                continue
            if board.switch(current_player,int(pick)-1):
                print("wrong number, pick again")
                continue
            break
        return 1
    if choice == "a":
        done = False
        while True:
            board.display_attackers(current_player)
            pick_a = input("which monster will attack? (enter a number or r to return to battle phase)\n")
            if pick_a=="r":
                break
            if not pick_a.isnumeric():
                print("don't enter letters beside r")
                continue
            attacker = int(pick_a)
            if not board.check_attacker(current_player,attacker-1):
                print("wrong number, try again")
                continue
            while True:
                board.display_targets(current_player)
                pick_t = input("what is the target? (enter a number or r to return to attacker picking)\n")
                if pick_t=="r":
                    break
                if not pick_t.isnumeric():
                    print("don't enter letters beside r")
                    continue
                target = int(pick_t)
                if not board.check_target(current_player,target-1):
                    print("wrong number, try again")
                    continue

                ### ATTACK DECLARATION

                ### BATTLE STEP

                ### DAMAGE STEP
                done = True

                ### DAMAGE CALCULATION
                lethal = board.damage_calc(current_player, attacker-1, target-1)
                if lethal == 1:
                    print("player "+board.color(not current_player)+" had his LP reduced to 0 and lost the game")
                    quit()
                if lethal == -1:
                    print("player "+board.color(current_player)+" had his LP reduced to 0 and lost the game")
                    quit()
                break
            if done:
                break
        return 1


seed(None,2)

_DRAW = "DRAW"
_STANBY = "STANDBY"
_MAIN = "MAIN"
_BATTLE = "BATTLE"
_END = "END"


player1 = player.Player()
player2 = player.Player()
board = board.Board(player1,player2)
turn_nb = 0
current_player = randint(0,1)
nextphase = _STANBY
board.draw_card(0,4)
board.draw_card(1,4)


while True:
    turn_nb +=1
    print("player "+board.color(current_player)+ " turn ! (turn n°"+str(turn_nb)+")")
    
    ### DRAW PHASE
    if nextphase== _DRAW:
        print_phase(nextphase)
        board.display(current_player)
        board._players[current_player].draw()
        if board.draw_card(current_player,1) == -1:
            print("player "+board.color(current_player)+" lost the game because of his inability to draw")
            quit()
        nextphase = _STANBY
        
    ### STANDBY PHASE
    if nextphase == _STANBY:
        print_phase(nextphase)
        nextphase = _MAIN

    ### MAIN PHASE
    if nextphase == _MAIN:
        print_phase(nextphase)
        board.init_main(current_player)
        while True:
            board.display(current_player)
            actions = board.main_actions(current_player, board._players[current_player].normal_summons)
            if turn_nb == 1:
                actions.remove("battle phase")
            print(actions)
            choice = input("what to do now? (enter first letter to chose)\n")
            for i in range(len(actions)):
                actions[i] = actions[i][0]
            if not handle_input(choice, actions, board, current_player):
                break

    ### BATTLE PHASE
    if nextphase == _BATTLE:
        print_phase(nextphase)
        board.init_battle(current_player)
        while True:
            board.display(current_player)
            actions = board.battle_actions(current_player)
            print(actions)
            choice = input("what to do now? (enter first letter to chose)\n")
            for i in range(len(actions)):
                actions[i] = actions[i][0]
            if not handle_input(choice, actions, board, current_player):
                break
        
    ### END PHASE
    if nextphase == _END:
        print_phase(nextphase)
        current_player = not current_player
        nextphase = _DRAW
