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
            self.x = x
            self.y = y

    def __str__(self):
        return ("Colour: {}, Points: {} \nRessources: Green: {}, Blue: {}, Red: {}, Black {}".format(self.colour,
        self.points, self.green, self.blue, self.red, self.blck))


class OpenBoard():
    '''list of 12 card objects (4 of each level),
    with methods to replace a card. '''

    deck = list()

    def __init__(self):
        for _ in range(3):
            y = 100 + _ * 120 # determining the y coordinate
            #that`s the 3 difficulties
            for __ in range(4):   #instance the 4 card
                x = 465 + __ * 100 # determining the x coordinate
                self.deck.append(Card(_, x, y)) # initializing the card with all params.

    def __str__(self):
        return str([el.__str__() for el in self.deck])
        #!maybe it will work better to call print on each el in the game loop...

    def replace_card(self, el: int):
        #maybe to add: logic, to test if player has sufficint ressources to buy
        cardbought = self.deck.pop(el)
        level = cardbought.level
        self.deck.insert(el, Card(level,cardbought.x, cardbought.y))
        return cardbought


class BonusC():
    '''a bonuscard is worth 3P and is awarded when a player own the right pattern of cards'''

    points = 3

    def __init__(self, x, y):
        self.x = x
        self.y = y
        res = [3,3,3,0]
        random.shuffle(res)
        #print(res)
        self.green, self.blue, self.red, self.blck = res

    def __str__(self):
        return ("Points: {} \nRessources: Green: {}, Blue: {}, Red: {}, Black {}".format(
        self.points, self.green, self.blue, self.red, self.blck))


class BonusBoard():
    '''list of 3 BonusC objects. With method remove to pop one'''

    def __init__(self):
        self.deck = []
        for _ in range(3):
            y = 100 + _ * 100     #design : 90*90, 10px padding, starting at 885,75
            x = 885
            self.deck.append(BonusC(x,y))

    def __str__(self):
        return str([el.__str__() for el in self.deck])

    def remove(self, el: int):
        return self.deck.pop(el)

class Ressources(dict):
    '''subclass to implement everywhere, where the 4 ressources are needed'''

    def __init__(self):
        super(Ressources, self).__init__()
        self["green"]=0
        self["blue"]=0
        self["red"]=0
        self["blck"]=0

    def set_all(self, value):
        for key in self:
            self[key] = value




class RessourceStack():
    '''depending on nb players (n) the available ressources are determined.
    This needs to be implemented in __init__. First implementation in a list. Possible an optimization: dic
    '''

    def __init__(self, n:int):
        (self.green, self.blue, self.red, self.blck)  = [n + 3] * 4


    def __str__(self):
        return (f"GREEN: {self.green} \nBLUE: {self.blue} \nRED: {self.red} \nBLACK: {self.blck} ")


class Player():
    #human or pc,points counter, carddeck, res-dec, state (acti> not), take ressources,
    # take a card, receive bonuscard,
    ressources = {"green": 0, "blue":0, "red": 0, "blck": 0}
    #id for knowing the order of players:
    id = 0
    #the accumulated points:
    points = 0
    #base coordinates:
    x = 0
    y = 0

    crds_count = {"green": 0, "blue": 0, "red": 0, "blck": 0}

    def __init__(self, name:str, human:int, id:int):
        self.name = name
        self.id = id
        self.cardstack = []
        if human == 1:
            self.state = "human"
        else:
            self.state = "computer"

    def __str__(self):
        return (f'''{self.name}: \nGREEN: {self.ressources["green"]}, BLUE: {self.ressources["blue"]}, RED: {self.ressources["red"]}, BLACK: {self.ressources["blck"]}
        Points: {self.points} \nOwned Cards: {self.cardstack}\n''')

    #take ressources.one a time repat the move acoordingly
    #add them to the player´s Ressource
    #REFACTOR so taht it's not four  times same code! give color to pick as param!!
    def take_res(self, id_res:int, rs:RessourceStack):
        '''take a ressource with the id_res from the rs,
        and add it to the player's ressource stack'''
        if id_res == 0:
            if rs.green >= 1:
                self.green += 1
                rs.green -= 1
                return True
            else:
                print ("invalid move")
                return False
        if id_res == 1:
            if rs.blue >= 1:
                self.blue += 1
                rs.blue -= 1
                return True
            else:
                print ("invalid move")
                return False
        if id_res == 2:
            if rs.red >= 1:
                self.red += 1
                rs.red -= 1
                return True
            else:
                print ("invalid move")
                return False
        if id_res == 3:
            if rs.blck >= 1:
                self.blck += 1
                rs.blck -= 1
                return True
            else:
                print ("invalid move")
                return False

    def card_counter(self):
        for id, card in enumerate(self.cardstack):
            if card.colour == 1:
                self.crds_count["green"] = self.crds_count.get("green", 0) + 1
            if card.colour == 2:
                self.crds_count["blue"] = self.crds_count.get("blue", 0) + 1
            if card.colour == 3:
                self.crds_count["red"] = self.crds_count.get("red", 0) + 1
            if card.colour == 4:
                self.crds_count["blck"] = self.crds_count.get("blck", 0) + 1
        self.cardstack.pop(id)

    def combine_ressources_with_collected_cards(self):
        total_res = {"green": 0, "blue":0, "red": 0, "blck": 0}
        total_res["green"] = self.ressources["green"] + self.crds_count["green"]
        total_res["red"] = self.ressources["red"] + self.crds_count["red"]
        total_res["blue"] = self.ressources["blue"] + self.crds_count["blue"]
        total_res["blck"] = self.ressources["blck"] + self.crds_count["blck"]
        return total_res

    def check_if_card_affordable(self, C:Card):
        owned_res = self.combine_ressources_with_collected_cards()
        if owned_res["green"] < C.green:
            return False
        if owned_res["blue"] < C.blue:
            return False
        if owned_res["red"] < C.red:
            return False
        if owned_res["blck"] < C.blck:
            return False
        else:
            return True

    def add_and_deduct_real_costs(self, ob:OpenBoard, el:int, stack:RessourceStack):

        if self.crds_count["green"] > ob.deck[el].green:
            pass
        else:
            self.ressources["green"] -= ob.deck[el].green - self.crds_count["green"]
            stack.green += ob.deck[el].green - self.crds_count["green"]
        if self.crds_count["blue"] > ob.deck[el].blue:
            pass
        else:
            self.ressources["blue"] -= ob.deck[el].blue - self.crds_count["blue"]
            stack.blue += ob.deck[el].blue - self.crds_count["blue"]
        if self.crds_count["red"] > ob.deck[el].red:
            pass
        else:
            self.ressources["red"] -= ob.deck[el].red - self.crds_count["red"]
            stack.red += ob.deck[el].red - self.crds_count["red"]
        if self.crds_count["blck"] > ob.deck[el].blck:
            pass
        else:
            self.ressources["blck"] -= ob.deck[el].blck - self.crds_count["blck"]
            stack.blck += ob.deck[el].blck - self.crds_count["blck"]

    #add card to player´s stack, rempve card from board And deduct the ressources from player
    def pick_crd(self, ob:OpenBoard, el:int, stack:RessourceStack):
        '''param el: index of card that is to be taken from the OpenBoard
        param ob: the board
        param stack: Ressourcestack obj - to refill wit the paid res.'''
        sufficient_res = self.check_if_card_affordable(ob.deck[el])
        if sufficient_res:
            self.add_and_deduct_real_costs(ob, el, stack)
            #adding points to player
            self.points += ob.deck[el].points
            # moving the card  from board to player
            self.cardstack.append(ob.replace_card(el))
            return True
        else:
            print("No sufficient funds. Please take another action")
            return False
