import card

###summons : 0 = normal, 1 = flip


class Monster:
    _n_summoned = 0
    def __init__(self, card, summon, position):
        self._card = card
        self._summon = summon
        self._stats_change = [0,0]
        self._nb_atk = 0
        self._position = position
        self._switchable = False

    def get_stat(self,position):
        return self._card._stats[position] + self._stats_change[position]

    def print_details(self):
        name = None
        if self._position == 2:
            print("[face-down monster]")
        else:
            print(self._card._name+ ": "+str(self.get_stat(0))+" ATK, "+str(self.get_stat(1))+" DEF, currently in "+self.get_position(self._position)+" position")

    def get_position(self,position):
        if position == 0:
            return "attack"
        elif position == 1:
            return "defense"
        else:
            return "face-down defense"
