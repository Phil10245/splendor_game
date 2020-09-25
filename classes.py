import random
import pygame as g

from colours import *

g.init()

class Button():
    '''creates a clickable button'''

    active_inactive_colours = ((g.Color('lightskyblue3')), (g.Color('dodgerblue2')))

    def __init__(self, x, y, w, h, font, text=""):
        self.rect = g.Rect(x, y, w, h)
        self.colour = self.active_inactive_colours[1]
        self.active = False
        self.text = text
        self.font = font
        self.text_surface = self.font.render(self.text, 1, self.colour)

    def handle_event(self, event):
        if event.type == g.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
                self.colour = self.active_inactive_colours[0] if self.active else self.active_inactive_colours[1]
                return True
            else:
                self.active = False

    def draw(self, screen):
        screen.blit(self.text_surface, (self.rect.x+5, self.rect.y+5))
        g.draw.rect(screen, self.colour, self.rect, 2)

    def increase_num(self, limit, screen):
        try:
            start = int(self.text)
        except:
            return
        if start == limit:
            self.text = "1"
        else:
            self.text = str(start + 1)
        self.text_surface = self.font.render(self.text, True, self.colour)
        return int(self.text)

class InputBox():

    active_inactive_colours = ((g.Color('lightskyblue3')), (g.Color('dodgerblue2')))

    def __init__(self, x, y, w, h, font, text=''):
        self.rect = g.Rect(x, y, w, h)
        self.colour = self.active_inactive_colours[1]
        self.text = text
        self.font = font
        self.txt_surface = self.font.render(text, True, self.colour)
        self.active = False
        self.visible = False

    def handle_event(self, event):
        if event.type == g.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current colour of the input box.
            self.colour = self.active_inactive_colours[0] if self.active else self.active_inactive_colours[1]
        if event.type == g.KEYDOWN:
            if self.active:
                if event.key == g.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == g.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.font.render(self.text, True, self.colour)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        g.draw.rect(screen, self.colour, self.rect, 2)

class Card():
    ''' card object - points, colour, ressource need, coordinates '''

    def __init__ (self, level, x: int, y: int, w: int, h: int, font):
        self.colour = random.choice([LIGHTBLACK, LIGHTBLUE, LIGHTRED, LIGHTGREEN, DARKWHITE])
        self.clicked = LIGHTBLUE
        self.level = level
        self.rect = g.Rect(x, y, w, h)
        self.ressources = Ressources()
        need = self.res_need(level)
        i = 0
        for k in self.ressources:
            self.ressources[k] = need[i]
            i += 1

        self.points = self.detPoints(level)
        self.font = font
        self.text_surface = self.font.render(str(self.points), 1, self.colour)

    def __str__(self):
        string = [f"Colour: {self.colour}, Points: {self.points} \n" , self.ressources.__str__()]
        return "".join(string)

    def max_need(self):
        max_lst = []
        for k in self.ressources:
            max_lst.append(self.ressources[k])
        max_value = max(max_lst)
        return max_value

    def min_need(self):
        min_lst = []
        for k in self.ressources:
            min_lst.append(self.ressources[k])
        min_value = min(min_lst)
        return min_value

    def detPoints(self, level):
        ''' func to calculate point value of cards. '''

        if level == 0:
            if self.max_need() ==  4:
                return 1
            else:
                return 0
        elif level == 1:
            if self.max_need() ==  6:
                return 3
            elif self.max_need() == 3:
                return 1
            else:
                return 2
        else:
            if self.max_need() == 7 and self.min_need() == 3:
                return 5
            if self.max_need() == 5:
                return 3
            else:
                return 4

    def res_need(self, level):
        '''func to make random ressource need distribution
        has a total res as a limit but it should itself vary a bit
        to be closer to the game, that has not all possible combinations,
        im working with hardcoded combinations, from which random.choice picks, according to difficult level'''

        if level == 0:
            r1st, r2nd, r3rd, r4th, r5th = (random.choice(((0,0,0,0,4),(0,1,1,1,2),(0,0,0,2,2),
            (1,1,1,1,0), (0,0,0,1,2),(0,0,0,0,3), (0,0,1,1,3))))
        elif level == 1:
            r1st, r2nd, r3rd, r4th, r5th = (random.choice(((0,0,2,3,2),(0,0,1,2,4), (0,0,0,0,5),
            (0,0,0,3,5), (0,0,0,0,6))))
        else:
            r1st, r2nd, r3rd, r4th, r5th = random.choice(((3,3,3,5,0), (0,0,0,0,7), (0,0,0,3,7)))
        lst = [r1st, r2nd, r3rd, r4th, r5th]
        random.shuffle(lst)
        return (lst)

    def draw(self, screen):
        # Blit the text
        screen.blit(self.text_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect
        g.draw.rect(screen, self.colour, self.rect, 0)
        # Blit Ressources
        rx , ry = int(self.rect.x + self.rect.w / 2 - 5) , int(self.rect.y + self.rect.h / 10)
        for ress, col in ((self.ressources["green"], GREEN), (self.ressources["blue"], BLUE),
        (self.ressources["red"], RED), (self.ressources["blck"], BLACK), (self.ressources["white"], WHITE)):
            text = self.font.render(str(ress), 1, col)
            screen.blit(text, (rx , ry))
            ry += int(self.rect.h / 6)

    def handle_event(self, event):
        if event.type == g.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True

    def replace_card(self):
        taken_card = self.deck.pop(el)
        level = taken_card.level
        self.deck.insert(el, Card(level,card_bought.x, card_bought.y))
        return cardbought

class BonusC():
    '''a bonuscard is worth 3P and is awarded when a player own the right pattern of cards'''

    points = 3

    def __init__(self, x, y):
        self.x = x
        self.y = y
        res = [3,3,3,0,0]
        random.shuffle(res)
        self.ressources = Ressources()
        i = 0
        for k in self.ressources:
            self.ressources[k] = res[i]
            i += 1

    def __str__(self):
        return (f"Points: {self.points} \n" ,self.ressources.__str__())

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

    def remove(self, el:int):
        return self.deck.pop(el)

class Ressources(dict):
    '''subclass to implement everywhere, where the 4 ressources are needed'''

    def __init__(self):
        super(Ressources, self).__init__()
        self["green"] = 0
        self["blue"] = 0
        self["red"] = 0
        self["blck"] = 0
        self["white"] = 0

    def set_all(self, value):
        for key in self:
            self[key] = value

    def set_green(self, value):
        self["green"] = value

    def set_red(self, value):
        self["red"] = value

    def set_blue(self, value):
        self["blue"] = value

    def set_blck(self, value):
        self["blck"] = value

    def set_white(self, value):
        self["white"] = value

    def __str__(self):
        return f"Green: {self['green']}\nRed: {self['red']}\nBlue: {self['blue']}\nBlack: {self['blck']}\nWhite: {self['white']}"

class RessourceStack():
    '''depending on nb players (n) the available ressources are determined.'''

    def __init__(self, n:int):
        self.ressources = Ressources()
        self.ressources.set_all(n+3)

    def __str__(self):
        return self.ressources.__str__()

class Player():
    #human or pc,points counter, carddeck, res-dec, state (acti> not), take ressources,
    # take a card, receive bonuscard,

    #the accumulated points:
    points = 0
    #base coordinates:
    x = 0
    y = 0



    def __init__(self, name:str, human:int):
        self.name = name
        if human == 1:
            self.state = "human"
        else:
            self.state = "computer"
        self.ressources = Ressources()
        self.crds_count = Ressources()

    def __str__(self):
        string = [f"{self.name}:", self.ressources.__str__(), f"Points: {self.points}"]
        return "\n".join(string)

    def take_res(self, key:str, rs:RessourceStack):
        '''take a ressource with the key from the rs,
        and add it to the player's ressource stack'''

        if rs.ressources[key] > 0:
            self.ressources[key] += 1
            rs.ressources[key] -= 1
            return True
        else:
            return False

    def get_and_accum_card_colour(self, c:Card):
            if c.colour == 1:
                self.crds_count["green"] = self.crds_count.get("green", 0) + 1
            if c.colour == 2:
                self.crds_count["blue"] = self.crds_count.get("blue", 0) + 1
            if c.colour == 3:
                self.crds_count["red"] = self.crds_count.get("red", 0) + 1
            if c.colour == 4:
                self.crds_count["blck"] = self.crds_count.get("blck", 0) + 1

    def combine_ressources_with_collected_cards(self):
        total_res = {k: self.ressources[k] + self.crds_count[k] for k in self.ressources}
        return total_res

    def check_if_card_affordable(self, c:Card):
        owned_res = self.combine_ressources_with_collected_cards()
        for r in owned_res:
            if owned_res[r] < c.ressources[r]:
                return False
        else:
            return True

    def add_and_deduct_real_costs(self, c:Card, stack:RessourceStack):

        for k in self.ressources:
            if self.crds_count[k] > c.ressources[k]:
                pass
            else:
                self.ressources[k] -= c.ressources[k] - self.crds_count[k]
                stack.ressources[k] += c.ressources[k] - self.crds_count[k]


    #add card to player´s stack, rempve card from board And deduct the ressources from player
    def pick_crd(self, c:Card, stack:RessourceStack):
        '''param el: index of card that is to be taken from the OpenBoard
        param ob: the board
        param stack: Ressourcestack obj - to refill wit the paid res.'''
        sufficient_res = self.check_if_card_affordable(c)
        if sufficient_res:
            self.add_and_deduct_real_costs(c, stack)
            #adding points to player
            self.points += c.points
            # moving the card  from board to player
            self.get_and_accum_card_colour(c)
            return True
        else:
            return False

    def check_if_qualified_for_bonus(self, bb:BonusBoard):
        '''pattern bonus card: 3,3,3,0 - pl must have the corresponding cards.
        if that is the case, checker will amount to 4, as for the 0 ressource, the
        condition is always True.'''

        for card in bb.deck:
            checker = 0
            for res in card.ressources:
                if card.ressources[res] <= self.crds_count[res]:
                    checker += 1
            if checker == 4:
                return True
        return False
