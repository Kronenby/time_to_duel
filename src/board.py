from random import *
import monster
import player

class Board:
    _blue = 0
    _red = 1
    _DRAW = "DRAW"
    _STANBY = "STANDBY"
    _MAIN = "MAIN"
    _BATTLE = "BATTLE"
    _END = "END"

    def __init__(self,_b_player,_r_player):
        self._decks = [sample(_b_player._deck,len(_b_player._deck)) , sample(_r_player._deck,len(_r_player._deck))]
        self._players = [_b_player, _r_player]
        self._LPs = [4000, 4000]
        self._m_zones = [[None,None,None],[None,None,None]]
        self._n_monsters = [0,0]
        self._cemetaries = [[],[]]
        self._hands = [[],[]]
        self._current_phase = self._DRAW
        self.draw_card(self._blue,4)
        self.draw_card(self._red,4)
        self._nextphase = self._STANBY
        self._turn_nb = 0

    def color(self,player):
        if player == self._blue:
            return self._players[0]._name
        else : 
            return self._players[1]._name

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
        self._players[player]._normal_summons +=1
        for monster in self._m_zones[player]:
            if monster is not None:
                monster._switchable = True

    def get_actions(self,player):
        actions = ["g" , "e"]
        if self._current_phase == self._MAIN:
            if self._turn_nb != 1:
                actions.append("b")
            if self._n_monsters[player] !=3 and self._players[player]._normal_summons != 0 and len(self._hands[player]) > 0 :
                n = []
                s = []
                for i in range(len(self._hands[player])):
                    n.append("n "+str(i+1))
                    s.append("s "+str(i+1))
                actions = actions + n + s
            for i in range(len(self._m_zones[player])):
                if self._m_zones[player][i] is not None and self._m_zones[player][i]._switchable:
                    actions.append("c "+str(i+1))   
        if self._current_phase == self._BATTLE:
            for i in range(len(self._m_zones[player])):
                monsteri = self._m_zones[player][i]
                if monsteri is not None and monsteri._nb_atk > 0 and monsteri._position == 0:
                    cpt = 0
                    for j in range(len(self._m_zones[not player])):
                        if self._m_zones[not player][j] is not None:
                            actions.append("a "+ str(i+1) + " " + str(j+1))
                            cpt+=1
                    if cpt == 0:
                        actions.append("a "+ str(i+1) + " " +str(len(self._m_zones[not player])))
        return actions

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
                    self._players[player]._normal_summons-=1
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
                    self._players[player]._normal_summons-=1
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

