from random import *
import monster
import player

class Board:
    _blue = 0
    _red = 1

    def __init__(self,_b_player,_r_player):
        self._decks = [sample(_b_player._deck,len(_b_player._deck)) , sample(_r_player._deck,len(_r_player._deck))]
        self._players = [_b_player, _r_player]
        self._LPs = [4000, 4000]
        self._m_zones = [[None,None,None],[None,None,None]]
        self._n_monsters = [0,0]
        self._cemetaries = [[],[]]
        self._hands = [[],[]]

    def color(self,player):
        if player == 0:
            return "blue"
        else : 
            return "red"

    def combat_destruct(self, player, id):
        card = (self._m_zones[player].pop(id))._card
        self._m_zones[player].insert(id,None)
        self._n_monsters[player] -= 1
        self._cemetaries[player].append(card)

    def draw_card(self, player, n):
        if not self._decks[player]:
            return -1
        for i in range(n):
            card = self._decks[player].pop(0)
            self._hands[player].append(card)
        return 1

    def init_main(self,player):
        self._players[player].normal_summons +=1
        for monster in self._m_zones[player]:
            if monster is not None:
                monster._switchable = True

    def main_actions(self, player, n):
        actions = ["give up","battle phase","end phase", "display", "view"]
        if self._n_monsters[player] !=3 and n != 0 and len(self._hands[player]) > 0 :
            actions.append("normal summon")
            actions.append("set face-down")
        for monster in self._m_zones[player]:
            if monster is not None and monster._switchable:
                actions.append("change monster position")
                break
        return actions

    def nsummon(self,player,id):
        if id in range(len(self._hands[player])):
            mon = monster.Monster(self._hands[player].pop(id),0,0)
            for i in range(len(self._m_zones[player])):
                if self._m_zones[player][i] is None:
                    self._m_zones[player].pop(i)
                    self._m_zones[player].insert(i,mon)
                    self._players[player].normal_summons-=1
                    self._n_monsters[player] += 1 
                    break
            return 1
        print("invalid choice, number not in your hand")
        return 0

    def setdown(self,player,id):
        if id in range(len(self._hands[player])):
            mon = monster.Monster(self._hands[player].pop(id),0,2)
            for i in range(len(self._m_zones[player])):
                if self._m_zones[player][i] is None:
                    self._m_zones[player].pop(i)
                    self._m_zones[player].insert(i,mon)
                    self._players[player].normal_summons-=1
                    self._n_monsters[player] += 1
                    break
            return 1
        print("invalid choice, number not in your hand")
        return 0

    def switch(self, player, id):
        if id in range(len(self._m_zones[player])):
            monster = self._m_zones[player][id]
            if monster is not None and monster._switchable:
                if monster._position == 2:
                    monster._summon = 1
                monster._position = not monster._position
                monster._switchable = False
                return 0
        return 1

    def init_battle(self,player):
        for monster in self._m_zones[player]:
            if monster is not None:
                monster._nb_atk +=1
        
    def battle_actions(self,player):
        actions = ["give up", "end phase", "display", "view"]
        for monster in self._m_zones[player]:
            if monster is not None and monster._nb_atk > 0 and monster._position == 0:
                actions.append("attack")
                break
        return actions  
    
    def check_attacker(self,player,id_a):
        return self._m_zones[player][id_a] is not None and self._m_zones[player][id_a]._nb_atk > 0 and self._m_zones[player][id_a]._position == 0
        
    def check_target(self,player, id_t):
        cpt=0
        for monster in self._m_zones[not player]:
            if monster is not None:
                cpt+=1
        if id_t == 3:
            return cpt == 0
        return self._m_zones[not player][id_t] is not None

    def init_damage_step(self,player,id_t):
        if id_t == 3:
            return 0
        target = self._m_zones[not player][id_t]
        if target._position == 2:
            target._summon = 1
            target._position = 1
            return 1
        return 0


    def damage_calc(self, player, id_a, id_t):
        attacker = self._m_zones[player][id_a]
        atk = attacker.get_stat(attacker._position)
        res = 0
        attacker._nb_atk-=1
        if id_t == 3:
            self._LPs[not player] -= attacker.get_stat(0)
            if self._LPs[not player] <=0:
                res = 1
            return res
        target = self._m_zones[not player][id_t]
        target_stat= target.get_stat(target._position)
        if atk > target_stat:
            if target._position == 0:
                self._LPs[not player] -= (atk - target_stat)
            if self._LPs[not player] <=0:
                res = 1
            self.combat_destruct(not player, id_t)
        elif atk < target_stat:
            self._LPs[player] -= (target_stat - atk)
            if target._position == 0:
                self.combat_destruct(player, id_a)
            if self._LPs[player] <=0:
                res = -1
        else :
            if target._position == 0:
                self.combat_destruct(player, id_a)
                self.combat_destruct(not player, id_t)
        return res

    def end_battle(self,player):
        for monster in self._m_zones[player]:
            if monster is not None:
                monster._nb_atk = 0

    def end_turn(self,player):
        if len(self._hands[player]) > 6:
            return len(self._hands[player]) - 6
        return 0

    def discard(self,player,id):
        if id in range(len(self._hands[player])):
            card = self._hands[player].pop(id)
            self._cemetaries[player].append(card)
            return 1
        print("invalid choice, number not in your hand")
        return 0 

    def display_hand(self, player):
        i=0
        for card in self._hands[player]:
            i+=1
            print(str(i)+":", end='')
            card.print_details()
        return i

    def display_switchable(self,player):
        i=0
        for monster in self._m_zones[player]:
            i+=1
            if monster is not None and monster._switchable:
                print(str(i)+":",end= '')
                monster.print_details()

    def display_cemetary(self,player,which):
        pick = (player and which) or (not player and not which)
        i = 0
        for card in self._cemetaries[pick]:
            i+=1
            print(str(i)+":",end='')
            card.print_details()
        return i

    def display_field(self,player,which):
        pick = player and which or (not player and not which)
        print("spell and trap zone:\n1: Empty\n2:Empty\n3:Empty")
        print("monster zone:")
        i=0
        for monster in self._m_zones[pick]:
            i+=1
            print(str(i)+":",end='')
            if monster is not None:
                monster.print_details()
            else:
                print("Empty")

    def display_attackers(self,player):
        i = 0
        for monster in self._m_zones[player]:
            i+=1
            if monster is not None and monster._nb_atk > 0 and monster._position==0:
                print(str(i)+":",end='')
                monster.print_details()

    def display_targets(self, player):
        i = 0
        cpt = 0
        for monster in self._m_zones[not player]:
            i+=1
            if monster is not None:
                cpt+=1
                print(str(i)+":",end='')
                monster.print_details()
        if (cpt==0):
            print("4: direct attack")

    def print_deckline(self, player):
        print("deck:"+str(len(self._decks[player]))+"                  x        x        x")

    def print_cemline(self, player):
        names = []
        for i in range(len(self._m_zones[player])):
            monster = self._m_zones[player][i]
            if monster is None:
                names.append("x")
            else:
                if monster._position == 2:
                    names.append("[face-down monster]")
                else:
                    names.append(monster._card._name+"("+monster.get_position(monster._position)+")")
        print("cemetary:"+str(len(self._cemetaries[0]))+ "               "+names[0]+"        "+names[1]+"        "+names[2])

    def display(self, player):
        p2 = not player
        print(self.color(p2)+":   "+str(self._LPs[p2])+ "LP   "+str(len(self._hands[p2]))+" cards in hand")
        print(" ")
        self.print_deckline(p2)
        print(" ")
        self.print_cemline(p2)
        print(" ")
        print(" ")
        self.print_cemline(player)
        print(" ")
        self.print_deckline(player)
        print(" ")
        print(self.color(player)+":   "+str(self._LPs[player])+"LP")
        for card in self._hands[player]:
            print(card._name+"     ", end='')
        print(" ")

        

    def display_all(self):
        print("current game:")
        print("blue lp :" + str(self._LPs[0]) + "  red lp:" +str(self._LPs[1]))
        print(" ")
        for p in range(2):
            print(self.color(p)+" hand:")
            self.display_hand(p)
            print(" ")
            print(self.color(p)+" deck:")
            for card in self._decks[p]:
                print(card._name + ", " ,end='')
            print("\n")
            print(self.color(p)+" cemetary:")
            self.display_cemetary(p,1)
            print(" ")
            print(self.color(p)+" field:")
            self.display_field(p,1)
            print("\n")
        
        print("end of display.")

