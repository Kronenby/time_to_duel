# time_to_duel
This is a personal project for fun. The point of it is to code a kind of yu-gi-oh game and implement as many features as possible.

For now the cards name and text are in French because I can't be bothered to translate it.
The card database is inspired from the game Yu-Gi-Oh Duel Links.

Also if you don't get how to play the game, read a tuto or something, because right now it's clearly not that hard to understand. (I'll explain the rules here later)

current features (25/06/2020):
    - regular game for 2 players with 4000LP each.
    - turn per turn on one terminal.
    - phase system with options different for each system
    - display on terminal
    - normal summons in attack position only
    - only normal monsters
    - no spell&trap card
    - monster position switchable (not on the turn they're summoned, according to the rules) and counted
    - battle step, and damage step not implemented yet (gotta check what they do first because I have no clue)
    - effects not implemented.
    - cards only have a name, an attack stat and a defense stat 

    added on 25/06/2020 on second commit:
    - monster summonable in attack position and settable in face-down defense position
    - flip summon when switch from face-down to attack and when attacked in face-down position 

added on 30/06/2020:
    - architecture cleaner. The game has been separated from the display and the player, that could allow an eventual implementation of a graphic interface, or an IA for the player.