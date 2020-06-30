from random import *
import board
import player
from TermDisplay import *

def handle_input(choice, actions, board, current_player):
    if choice not in actions:
        print("wrong input, try again.")
        return 1
    if choice == "g":
        print_defeat(board.color(current_player),1)
        board._players[current_player].accept_defeat(1)
        quit()
    if choice == "b":
        board._nextphase = board._BATTLE
        return 0
    if choice == "e":
        board._nextphase = board._END
        return 0
    s_choice = choice.split()
    if s_choice[0] == "n":
        board.nsummon(current_player,int(s_choice[1])-1)
        return 1
    if s_choice[0] == "s":
        board.setdown(current_player,int(s_choice[1])-1)
        return 1
    if s_choice[0] == "c":
        board.switch(board, current_player,int(s_choice[1])-1)
        return 1
    if s_choice[0] == "a":
        ### ATTACK DECLARATION

        ### BATTLE STEP

        ### DAMAGE STEP
        if board.init_damage_step(current_player,int(s_choice[2])-1):
            display_board(board, current_player)
            input("face-down monster got flipped! press any input to continue")

        ### DAMAGE CALCULATION
        lethal = board.damage_calc(current_player, int(s_choice[1])-1, int(s_choice[2])-1)
        if lethal != 0:
            defeated_player = ( current_player != (lethal>0) )
            print_defeat(board.color(defeated_player),2)
            board._players[defeated_player].accept_defeat(2)
            quit()
        return 1


seed(None,2)

player1 = player.TermPlayer("blue")
player2 = player.TermPlayer("red")
board = board.Board(player1,player2)
current_player = randint(0,1)

while True:
    board._turn_nb +=1
    print_turn(board.color(current_player),board._turn_nb)
    
    ### DRAW PHASE
    if board._nextphase== board._DRAW:
        board._current_phase = board._nextphase
        print_phase(board._current_phase)
        display_board(board, current_player)
        board._players[current_player].draw()
        if board.draw_card(current_player,1) == -1:
            print_defeat(board.color(current_player),0)
            board._players[current_player].accept_defeat()
        board._nextphase = board._STANBY
        
    ### STANDBY PHASE
    if board._nextphase == board._STANBY:
        board._current_phase = board._nextphase
        print_phase(board._current_phase)
        board._nextphase = board._MAIN

    ### MAIN PHASE
    if board._nextphase == board._MAIN:
        board._current_phase = board._nextphase
        print_phase(board._current_phase)
        board.init_main(current_player)
        while True:
            display_board(board, current_player)
            legal_actions = board.get_actions(current_player)
            choice = board._players[current_player].get_input(board, current_player, legal_actions)
            if not handle_input(choice, legal_actions, board, current_player):
                break

    ### BATTLE PHASE
    if board._nextphase == board._BATTLE:
        board._current_phase = board._nextphase
        print_phase(board._current_phase)
        board.init_battle(current_player)
        while True:
            display_board(board, current_player)
            legal_actions = board.get_actions(current_player)
            choice = board._players[current_player].get_input(board, current_player, legal_actions)
            if not handle_input(choice, legal_actions, board, current_player):
                break
        
    ### END PHASE
    if board._nextphase == board._END:
        board._current_phase = board._nextphase
        print_phase(board._current_phase)
        nb_discard = board.end_turn(current_player)
        while nb_discard != 0:
            pick = board._players[current_player].choose_discard(board, current_player, nb_discard)
            if board.discard(current_player,int(pick)-1):
                nb_discard-=1
        current_player = not current_player
        board._nextphase = board._DRAW
