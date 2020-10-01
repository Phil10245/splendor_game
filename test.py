import random
from classes import *
from pygame import font


#test classes
print("#Ressources")
try:
    res = Ressources()
    res.set_all(69)
    print(res)
except:
    raise
print("#Players")
try:
    player1 = Player("phil", 1)
    print(player1)
    print(player1.ressources)
except:
    raise
print("#RessourceStack")
try:
    rs = RessourceStack(3)
    print(rs)
except:
    raise
print("#player methods")
try:
    player1.take_res("green", rs)
    print(player1)
    print(rs)
except:
    raise
print("#card")
try:
    c = Card(2,0,0,0,0, font.SysFont("comicsans", 30))
    print(c)
    c.replace_card(0, [c])
    print(c)
    pass
except:
    raise
try:
    player1.pick_crd(c, rs)
    player1.ressources.set_all(9)
    player1.pick_crd(c, rs)
    print(player1)
except:
    raise
print("#Bonusard")
try:
    for i in range(4):
        print("new Bonuscard:")
        bc = BonusC(0,0,0,0, font.SysFont("comicsans", 30))
        print(bc)
except:
    raise
print("#check_if_qualified_for_bonus")
try:
    player1.crds_count.set_all(3)
    print(player1.check_if_qualified_for_bonus(bc))
    player1.crds_count.set_all(2)
    print(player1.check_if_qualified_for_bonus(bc))
    player1.crds_count.set_all(4)
    print(player1.check_if_qualified_for_bonus(bc))
except:
    raise
