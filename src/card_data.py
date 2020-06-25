from collections import OrderedDict

cards_data = OrderedDict()
cards_data[-1] = ["test_monster",1000,1000]
cards_data[-2] = ["strong_test_monster",2000,2000]
cards_data[0]  = ["Axe Raider",1700,1150]
cards_data[1]  = ["Boeuf de Combat",1700,1000]
cards_data[2]  = ["Attaquant au Sol Bugroth",1500,1000]
cards_data[3]  = ["Cavalier Mystique",1300,1550]
cards_data[4]  = ["Dragon Rampant N°2",1600,1200]
cards_data[5]  = ["Dragon des Ténèbres",1500,800]
cards_data[6]  = ["Gazelle, Roi des Bêtes Mythiques",1500,1200]
cards_data[7]  = ["Glaive de l'Alligator",1500,1200]
cards_data[8]  = ["Grand Blanc",1600,800]
cards_data[9]  = ["Guerrier de Zera",1600,1600]
cards_data[10] = ["Kamakiri Volant N°2",1500,800]
cards_data[11] = ["Le Squelette des Mers",1600,900]
cards_data[12] = ["Oiseau au Crâne Rouge",1550,1200]
cards_data[13] = ["Overdrive",1600,1500]
cards_data[14] = ["Puce Géante",1500,1200]
cards_data[15] = ["Roi Rex à Deux Têtes",1600,1200]
cards_data[16] = ["Ryu-Kishin le Puissant",1600,1200]
cards_data[17] = ["Dragon Zombie",1600,0]
cards_data[18] = ["Amitié Scintillante",1300,1100]
cards_data[19] = ["Ancien Guerrier Lézard",1400,1100]

def get_data(id):
    return cards_data[id]

def data_length():
    return len(cards_data)