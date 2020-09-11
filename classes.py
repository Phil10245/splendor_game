import random

# first a cardcreator, creating cards with points, 1 o 4 colors, and ressouce need.
# all implemented in the Card object! It works fine. Many if statements and combinations are hard hardcoded
# <> Up next: write the Open_Board class: on init puts 12 cards in a list, 4 of each level,
# and a func to draw new card, if one is taken out -> done :)
# Next up: BonusCard class and func. logic similar to cardcreator stff done before!
# => also done.
# NEXT UP: RESSOURCE_STACK >done
# next: player class - there will be 2 funcs: 1 - pick ressources REFACTOR!; 2nd: pick card. DONE
# time for the game loop and py game. keep it text based till it's running ok.
# ressource stack just a list, instead of class?
#check func: compare ress need withn avaiolable ress ->returnn true if sufficient

class Card():
    ''' card object - points, colour, ressource need, coordinates '''

    x = 0
    y = 0

    def detPoints(self, level):
        ''' func to calculate point value of cards. '''

        if level == 0:
            if max(self.red, self.green, self.blck, self.blue) ==  4:
                return 1
            else:
                return 0
        elif level == 1:
            if max(self.red, self.green, self.blck, self.blue) ==  6:
                return 3
            elif max(self.red, self.green, self.blck, self.blue) == 3:
                return 1
            else:
                return 2
        else:
            if (max(self.red, self.green, self.blck, self.blue) == 7 and
            min(self.red, self.green, self.blck, self.blue) == 3):
                return 5
            if max(self.red, self.green, self.blck, self.blue) == 5:
                return 3
            else:
                return 4


    def res_need(self, level):
        '''func to make random ressource need distribution
        has a total res as a limit but it should itself vary a bit
        to be closer to the game, that has not all possible combinations,
        im working with hardcoded combinations, from which random.choice picks, according to difficult level'''
        if level == 0:
            r1st, r2nd, r3rd, r4th = (random.choice(((0,0,0,4),(1,1,1,2),(0,0,2,2),
            (1,1,1,1), (0,0,1,2),(0,0,0,3), (0,1,1,3))))
        elif level == 1:
            r1st, r2nd, r3rd, r4th = (random.choice(((0,2,3,2),(0,1,2,4), (0,0,0,5),
            (0,0,3,5), (0,0,0,6))))
        else:
            r1st, r2nd, r3rd, r4th = random.choice(((3,3,3,5), (0,0,0,7), (0,0,3,7)))
        lst = [r1st, r2nd, r3rd, r4th]
        random.shuffle(lst)
        return (lst)


    def __init__ (self, level,x: int, y: int):
            self.colour = random.randint(1, 4)
            self.level = level
            (self.green, self.blue, self.red, self.blck) = self.res_need(level)
            self.points = self.detPoints(level)


    def __str__(self):
        return ("Colour: {}, Points: {} \nRessources: Green: {}, Blue: {}, Red: {}, Black {}".format(self.colour,
        self.points, self.green, self.blue, self.red, self.blck))


class OpenBoard():
    '''made up of 12 card objects - list (4 of each level)
    with function to take out a card and refill the place wih a new one. '''
    deck = list()

    def __init__(self):
        for _ in range(3):
            y = 50 + _ * 100 # determining the y coordinate
            #that`s the 3 difficulties
            for __ in range(4):   #instance the 4 card
                x = 250 + __ * 70 # determining the x coordinate
                self.deck.append(Card(_, x, y)) # initializing the card with all params.

    def __str__(self):
        return str([el.__str__() for el in self.deck])
        #!maybe it will work better to call print on each el in the game loop...

    def replaceCard(self, el: int):
        #maybe to add: logic, to test if player has sufficint ressources to buy
        cardbought = self.deck.pop(el)
        level = cardbought.level
        self.deck.insert(el, Card(level))
        return cardbought


class BonusC():
    '''a bonuscard is worth 3P and is awarded when a player own the right pattern of cards'''
    points = 3

    def __init__(self):
        res = [3,3,3,0]
        random.shuffle(res)
        #print(res)
        self.green, self.blue, self.red, self.blck = res

    def __str__(self):
        return ("Points: {} \nRessources: Green: {}, Blue: {}, Red: {}, Black {}".format(
        self.points, self.green, self.blue, self.red, self.blck))


class BonusBoard():
    '''possible: merge into OpenBoard class to have all open cards together.
    but in the same time they follow a bit different game logic, therefore it might
    be better to keep them seperated'''
    def __init__(self):
        self.deck = []
        for _ in range(3):
            self.deck.append(BonusC())

    def __str__(self):
        return str([el.__str__() for el in self.deck])

    def remove(self, el: int):
        return self.deck.pop(el)


class RessourceStack():
    '''depending on nb players (n) the available ressources are determined.
    This needs to be implemented in __init__. First implementation in a list. Possible an optimization: dic
    '''

    def __init__(self, n:int):
        (self.green, self.blue, self.red, self.blck)  = [n + 2] * 4

    def __str__(self):
        return (f"GREEN: {self.green} \nBLUE: {self.blue} \nRED: {self.red} \nBLACK: {self.blck} ")


class Player():
    #human or pc,points counter, carddeck, res-dec, state (acti> not), take ressources,
    # take a card, receive bonuscard,
    (green, blue, red, blck) = (0,0,0,0)
    # active / it`s teh player´s turn:
    state = 0
    #id for knowing the order of players:
    id = 0
    #the accumulated points:
    points = 0
    #base coordinates:
    x = 0
    y = 0

    cardstack = list ()

    def __init__(self, name:str, human:int, id:int):
        self.name = name
        self.id = id
        if human == 1:
            self.state = "human"
        else:
            self.state = "computer"

    def __str__(self):
        return f'''{self.name}: \nGREEN: {self.green}, BLUE: {self.blue}, RED: {self.red}, BLACK: {self.blck}
Points: {self.points} \nOwned Cards: {self.cardstack}\n'''

    #take ressources.one a time repat the move acoordingly
    #add them to the player´s Ressourc
    #REFACTOR so taht it's not four  times same code! give color to pick as param!!
    def take_res(self, rs: RessourceStack, ressource: str):
        if rs.ressource >= 1:
            self.ressource += 1
            rs.ressource -= 1
        else:
            print ("invalid move")

    #add card to player´s stack, rempve card from board And deduct the ressources from player
    def pick_crd(self, ob:OpenBoard, el:int, stack:RessourceStack):
        '''param el: index of card that is to be taken from the OpenBoard
        param ob: the board
        param stack: Ressourcestack obj - to refill wit the paid res.'''
        if (self.green, self.blue, self.red, self.blck) >= (ob.deck[el].green, ob.deck[el].blue, ob.deck[el].red, ob.deck[el].blck):
            # updating player's stack
            self.green -= ob.deck[el].green
            self.blue -= ob.deck[el].blue
            self.red -= ob.deck[el].red
            self.blck -= ob.deck[el].blck
            #Updating resource stack:
            stack.lst_res[0] += ob.deck[el].green
            stack.lst_res[1] += ob.deck[el].blue
            stack.lst_res[2] += ob.deck[el].red
            stack.lst_res[3] += ob.deck[el].blck
            # moving the card  from board to player
            self.cardstack.append(ob.replaceCard(el))
        else:
            print("No sufficient funds. Please take another action")
