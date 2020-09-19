import random
from classes import *

try:
    P = Player("Test", 1, 0)
    print("test 1 ok")
    print(P)
except:
    print("Player instantiaten doesn't work")
    raise
try:
    cards_count = {"green": 0, "blue":0, "red": 0, "blck": 0}
    P.combine_ressources_with_collected_cards(cards_count)
    print("no error when calling combine-func")
except:
    print("combine is not working")
    raise

try:
    ob = OpenBoard()
    P.pick_crd(ob, 1, RessourceStack(2))
    print("pick_crd works")
except:
    print("pick_crd doesnt work")
    raise
