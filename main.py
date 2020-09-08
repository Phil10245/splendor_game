from classes import Card, OpenBoard, BonusC, BonusBoard, RessourceStack, Player
#import pygame

#defining all known funcs, needed for the game not implemented in classes:
#check func -> already implented in player class.
#check points -> if >=15 game ends,playyer wins
#








def test():
    '''to test the functions. new tests added as functions are developed'''
    new_card = Card(2)
    print(new_card)
    new_card = Card(1)
    print(new_card)
    new_card = Card(0)
    print(new_card)
    new_game = OpenBoard()
    print(new_game)
    print(new_game.deck[-1])
    cb = new_game.replaceCard(-1)
    print(new_game.deck[-1])
    print(cb)
    #new_bonus = BonusC()
    bonus_set = BonusBoard()
    print(bonus_set.deck[0])
    crd = bonus_set.remove(0)
    print(crd)

def test2():
    ob = OpenBoard()
    print(ob)
    nstack = RessourceStack(2)
    print(nstack)
    np = Player("hans", 0, 1)
    print(np.name, np.state, np.green, np.cardstack)
    for _ in range(4):
        np.take_res(nstack, 2)
    np.pick_crd(ob, 11, nstack)
    #print(ob)
    print(np.cardstack[0])
    print(nstack)
    print(np.green, np.blue, np.red, np.blck)
test2()
