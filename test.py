import random
from classes import *

#test classes
#Ressources
try:
    res = Ressources()
    res.set_all(69)
    print(res)
except:
    raise
#Players
try:
    player1 = Player("phil", 1)
    print(player1)
    print(player1.ressources)
except:
    raise
#RessourceStack
try:
    rs = RessourceStack(3)
    print(rs)
except:
    raise
    #BonusBoard + BonusCard
try:
    bb = BonusBoard()
    print(bb)
    bb.remove(0)
    print(bb)
except:
    raise
#Open_Board + cards
try:
    ob = OpenBoard()
    print(ob)
    card = ob.replace_card(7)
    print(card)
except:
    raise
#player methods
try:
    player1.take_res("green", rs)
    print(player1)
except:
    raise
