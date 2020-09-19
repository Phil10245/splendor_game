import random
from classes import *

#test class RessourceStack
print("\nTEST 1\n")
try:
    res = Ressources()
    print(f"{res}")
    res.set((1,1,1,1))
    print(f"{res}")
    res2 = Ressources([69,69,69,69])
    res3 = res2.get()
    print(f"{res2}\n{res3}")
except:
    print("Problem with Ressources")
    raise
#test RessourceStack
print("\nTEST 2\n")
try:
    n = 2
    ressource_stack = RessourceStack(n)
    print("{}-Player Ressource_stack {}".format(n, ressource_stack))
except:
    print("problem with RessourceStack")
# test Player
print("\nTEST 3a\n")
try:
    P = Player("TestPlyer", 1, 0)
    print("player object:")
    print(P)
except:
    print("Player instantiaten doesn't work")
    raise
print("\nTEST 3b\n")
try:
    P.ressources.green = 100
    print("P.ressources", P.ressources)
    P.ressources.set([99,88,77,66])
    print(P.ressources)
except:
    print("issue in manipulating players ressource")
    raise
print("\nTEST 4\n")
try:
    P.cardstack = {"green": 1, "blue":2, "red": 3, "blck": 4}
    P.ressources = {"green": 4, "blue":3, "red": 2, "blck": 65}
    print(P.cardstack)
    print(P.ressources)
    total_res = P.combine_ressources_with_collected_cards()
    print("Sum", total_res)
    print("no error when calling combine-func")
except:
    print("combine is not working")
    raise
#tests pick card
print("TEST 5\n")
try:
    ob = OpenBoard()
    P.pick_crd(ob, 1, RessourceStack(2))
    print("pick_crd works")
    for key in P.ressources:
        P.ressources[key] += 5
    P.pick_crd(ob, 4, RessourceStack(2))
except:
    print("pick_crd doesnt work")
    raise
