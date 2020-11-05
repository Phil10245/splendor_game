'''module that holds all classes and their associated methods of the game'''

import random
import pygame as g

from colours import (WHITE, BLACK, BLUE, RED, GREEN, ORANGE, LIGHTBLUE,
LIGHTBLACK, LIGHTRED, LIGHTGREEN, DARKWHITE)
from graphics import REDTOKEN, BLACKTOKEN, GREENTOKEN, BLUETOKEN, WHITETOKEN

g.init()

class Button():
    '''A clickable button. '''

    active_inactive_colours = ((g.Color('lightskyblue3')), (g.Color('dodgerblue2')))

    def __init__(self, font, x, y, w, h, text=""):
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
                return True
            self.active = False
            return False

    def draw(self, screen):
        screen.blit(self.text_surface, (self.rect.centerx - self.text_surface.get_width() / 2,
        self.rect.centery - self.text_surface.get_height() / 2))
        g.draw.rect(screen, self.colour, self.rect, 2)

    def increase_num(self, limit):
        ''' (Button obj, int) -> int

        Increases the number in self.text between 1 and limit.

        Catches if self.text is NOT an int.
        '''

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
    '''A input box class.

    inspired by
    https://stackoverflow.com/questions/46390231/how-to-create-a-text-input-box-with-pygame
    '''

    active_inactive_colours = ((g.Color('lightskyblue3')), (g.Color('dodgerblue2')))

    def __init__(self, x, y, w, h, font, text=''):
        self.rect = g.Rect(x, y, w, h)
        self.colour = self.active_inactive_colours[1]
        self.text = text
        self.font = font
        self.text_surface = self.font.render(text, True, self.colour)
        self.active = False
        self.visible = True

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
                self.text_surface = self.font.render(self.text, True, self.colour)

    def update(self):
        '''Resize the box if the text is too long.'''

        width = max(200, self.text_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        ''' Draw the box.'''
        # Blit the text.
        screen.blit(self.text_surface, (self.rect.centerx - self.text_surface.get_width() / 2,
        self.rect.centery - self.text_surface.get_height() / 2))
        # Blit the rect.
        g.draw.rect(screen, self.colour, self.rect, 2)

class Card():
    ''' card class has points, colour, ressource need, coordinates attributes
    and all mainly card related functions.'''

    def __init__ (self, level, x: int, y: int, w: int, h: int, font):
        self.colour = random.choice([LIGHTBLACK, LIGHTBLUE, LIGHTRED, LIGHTGREEN, DARKWHITE])
        self.clicked = LIGHTBLUE
        self.level = level
        self.rect = g.Rect(x, y, w, h)
        self.Resources = Resources()
        need = self.res_need(level)
        i = 0
        for k in self.Resources:
            self.Resources[k] = need[i]
            i += 1

        self.points = self.detPoints(level)
        self.font = font
        self.text_surface = self.font.render(str(self.points), 1, BLACK)

    def __str__(self):
        string = [f"Colour: {self.colour}, Points: {self.points} \n" , self.Resources.__str__()]
        return "".join(string)

    def max_need(self):
        '''Determine the highest amount of ressources needed of all ressources.'''
        max_lst = []
        for k in self.Resources:
            max_lst.append(self.Resources[k])
        max_value = max(max_lst)
        return max_value

    def min_need(self):
        '''Determine the minimum amount of ressources needed of all ressources.'''
        min_lst = []
        for k in self.Resources:
            min_lst.append(self.Resources[k])
        min_value = min(min_lst)
        return min_value

    def detPoints(self, level):
        ''' (self, int) -> int

        Calculate point value of cards. '''

        if level == 0:
            if self.max_need() ==  4:
                return 1
            return 0
        if level == 1:
            if self.max_need() ==  6:
                return 3
            if self.max_need() == 3:
                return 1
            return 2
        if self.max_need() == 7 and self.min_need() == 3:
            return 5
        if self.max_need() == 5:
            return 3
        return 4

    def res_need(self, level):
        '''(self, int) -> list of int

        Calculate random ressource need distribution.

        Has a "total res" as a limit but it should itself vary a bit
        to be closer to the game, that has not all possible combinations,
        im working with hardcoded combinations, from which random.choice picks,
        according to difficult level'''

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
        return lst

    def draw(self, screen):
        # Blit the text
        screen.blit(self.text_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect
        g.draw.rect(screen, self.colour, self.rect, 0)
        # Blit the text
        screen.blit(self.text_surface, (self.rect.x+5, self.rect.y+5))
        # Blit Resources
        rx , ry = int(self.rect.x + self.rect.w / 2 - 5) , int(self.rect.y + self.rect.h / 10)
        colours_text= (BLACK, BLUE, RED, GREEN, WHITE)
        order_res =("blck", "blue", "red", "green", "white")
        for ress, colour_text in zip(order_res, colours_text):
            text = self.font.render(str(self.Resources[ress]), 1, colour_text)
            screen.blit(text, (rx , ry))
            ry += int(self.rect.h / 6)

    def handle_event(self, event):
        if event.type == g.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
            return False

    def replace_card(self, el, cardlist):
        ''' (self, int, list of Card-Objs) -> None

        Removes self from cardlist and inserts a new Card at index el.

        Transfers level and coordinate values to the new Card'''
        replacement = Card(self.level, self.rect.x, self.rect.y,
        self.rect.w, self.rect.h, self.font)
        cardlist.pop(el)
        cardlist.insert(el,replacement)

class BonusC():
    '''Bonus Card class.

    A bonuscard is worth 3P and is awarded when a player own the right pattern of cards'''

    points = 3
    colour = ORANGE

    def __init__(self, x, y, w, h, font):
        self.rect = g.Rect(x, y, w, h)
        self.font = font
        self.text_surface = self.font.render(str(self.points), 1, BLACK)
        self.visible = True
        res =([3,3,3,0,0], [4,4,0,0,0])
        res = random.choice(res)
        random.shuffle(res)
        self.Resources = Resources()
        i = 0
        for k in self.Resources:
            self.Resources[k] = res[i]
            i += 1

    def __str__(self):
        return f"Points: {self.points} \n"  + self.Resources.__str__()

    def draw(self, screen):
        if self.visible:
            # Blit the rect
            g.draw.rect(screen, self.colour, self.rect, 0)
            # Blit the text
            screen.blit(self.text_surface, (self.rect.x+5, self.rect.y+5))
            # Blit Resources
            rx , ry = int(self.rect.x + self.rect.w / 2 - 5) , int(self.rect.y + self.rect.h / 10)
            colours_text= (BLACK, BLUE, RED, GREEN, WHITE)
            order_res =("blck", "blue", "red", "green", "white")
            for ress, colour_text in zip(order_res, colours_text):
                if self.Resources[ress] != 0:
                    text = self.font.render(str(self.Resources[ress]), 1, colour_text)
                    screen.blit(text, (rx , ry))
                    ry += int(self.rect.h / 6)

class Resources(dict):
    '''subclass to implement everywhere, where the 4 Resources are needed'''

    def __init__(self):
        super(Resources, self).__init__()
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
        part_a = f"Green: {self['green']}\nRed: {self['red']}\nBlue: {self['blue']}\n"
        part_b = f"Black: {self['blck']}"
        return part_a + part_b

class Resourcestack():
    '''depending on nb players (n) the available Resources are determined.'''

    def __init__(self, n:int):
        self.Resources = Resources()
        self.Resources.set_all(n+3)
        self.lst_rects =[]

    def __str__(self):
        return self.Resources.__str__()

    def draw(self, screen, font, x=0, y=0, r=0, padding=0):
        i = 0
        tokens = (BLACKTOKEN, BLUETOKEN, REDTOKEN, GREENTOKEN, WHITETOKEN)
        colours_bg = (LIGHTBLACK, LIGHTBLUE, LIGHTRED, LIGHTGREEN, DARKWHITE)
        order_res =("blck", "blue", "red", "green", "white")
        for ress, colour_bg, token in zip(order_res, colours_bg, tokens):
            ynext = y + i * (r * 2 + padding)
            res_rect = g.draw.circle(screen, colour_bg, (x, ynext), r, 1)
            print("DEBUG: ResourceStack.Rects", res_rect)
            # render the loaded token pictures
            token_small = g.transform.scale(token, (res_rect.width, res_rect.height))
            screen.blit(token_small, res_rect)
            #remove, when al is set up nicely
            g.draw.circle(screen, BLUE, (x, ynext), 5)

            # render the amount of resource available
            text = font.render(str(self.Resources[ress]), 1, WHITE)
            screen.blit(text, (x - text.get_width() / 2 , ynext - text.get_height() / 2))

            self.lst_rects.append((ress, res_rect))
            i += 1

class Player():
    '''Player class. Methods to interact with cards and resources'''

    points = 0

    def __init__(self, name:str, human:int):
        self.name = name
        if human == 1:
            self.state = "human"
        else:
            self.state = "computer"
        self.Resources = Resources()
        self.crds_count = Resources()

    def __str__(self):
        string = [f"{self.name}:", self.Resources.__str__(), f"Points: {self.points}"]
        return "\n".join(string)

    def take_res(self, key:str, rs:Resourcestack):
        '''take a ressource with the key from the rs,
        and add it to the player's ressource stack'''

        if rs.Resources[key] > 0:
            self.Resources[key] += 1
            rs.Resources[key] -= 1
            return True
        return False

    def get_and_accum_card_colour(self, c:Card):
        if c.colour == LIGHTGREEN:
            self.crds_count["green"] = self.crds_count.get("green", 0) + 1
        if c.colour == LIGHTBLUE:
            self.crds_count["blue"] = self.crds_count.get("blue", 0) + 1
        if c.colour == LIGHTRED:
            self.crds_count["red"] = self.crds_count.get("red", 0) + 1
        if c.colour == LIGHTBLACK:
            self.crds_count["blck"] = self.crds_count.get("blck", 0) + 1
        if c.colour == DARKWHITE:
            self.crds_count["white"] = self.crds_count.get("white", 0) + 1

    def combine_Resources_with_collected_cards(self):
        total_res = {k: self.Resources[k] + self.crds_count[k] for k in self.Resources}
        return total_res

    def check_if_card_affordable(self, c:Card):
        owned_res = self.combine_Resources_with_collected_cards()
        checker = 0
        for r in owned_res:
            if owned_res[r] >= c.Resources[r]:
                checker += 1
        if checker == 5:
            return True
        return False

    def add_and_deduct_real_costs(self, c:Card, stack:Resourcestack):
        for k in self.Resources:
            if self.crds_count[k] > c.Resources[k]:
                pass
            else:
                self.Resources[k] -= c.Resources[k] - self.crds_count[k]
                stack.Resources[k] += c.Resources[k] - self.crds_count[k]

    def pick_crd(self, c:Card, stack:Resourcestack):
        self.add_and_deduct_real_costs(c, stack)
        #adding points to player
        self.points += c.points
        # moving the card  from board to player
        self.get_and_accum_card_colour(c)

    def check_if_qualified_for_bonus(self, bc:BonusC):
        '''pattern bonus card: 3,3,3,0 or 4,4,0,0- pl must have the corresponding cards.
        if that is the case, checker will amount to 4, as for the 0 ressource, the
        condition is always True.'''

        checker = 0
        for res in bc.Resources:
            if bc.Resources[res] <= self.crds_count[res]:
                checker += 1
        if checker >= 4:
            return True
        return False

    def draw_name_points(self, screen, font, x=0, y=0, dist=0):
        ''' Draw name and points of the active player in the lower part of display.
        To render underneath: count of the cards he owns and 4 circles with
        the count of Resources
        '''
        p_name = self.name
        drw_name = font.render(p_name, 1, BLACK)
        screen.blit(drw_name, (x, y))
        p_points = self.points
        drw_points = font.render("Points: " + str(p_points), 1, BLACK)
        screen.blit(drw_points, (x + dist , y))

    def draw_crds_count(self, screen, font, x=0, y=0, w=0, padding=0):
        i = 0
        colours_bg = (LIGHTBLACK, LIGHTBLUE, LIGHTRED, LIGHTGREEN, DARKWHITE)
        colours_text= (BLACK, BLUE, RED, GREEN, WHITE)
        order_res =("blck", "blue", "red", "green", "white")
        for ress, colour_bg, colour_text in zip(order_res, colours_bg, colours_text):
            xnext = x + i * (w + padding)
            g.draw.rect(screen, colour_bg, g.Rect(xnext, y, w, w), 2)
            drw_nbcrds = font.render(str(self.crds_count.get(ress)), 1, colour_text)
            screen.blit(drw_nbcrds, (int(xnext + w / 2 - 5), y + int(w / 2)))
            i += 1

    def draw_resources_stack(self, screen, font, x=0, y=0, r=0, padding=0):
        i = 0
        colours_bg = (LIGHTBLACK, LIGHTBLUE, LIGHTRED, LIGHTGREEN, DARKWHITE)
        colours_text= (BLACK, BLUE, RED, GREEN, WHITE)
        order_res =("blck", "blue", "red", "green", "white")
        for ress, colour_bg, colour_text in zip(order_res, colours_bg, colours_text):
            xnext = x + i * (r * 2 + padding)
            g.draw.circle(screen, colour_bg, (xnext, y), r , 1)
            text = font.render(str(self.Resources[ress]), 1, colour_text)
            screen.blit(text, (xnext - text.get_width() / 2 , y - text.get_height() / 2))
            i += 1
