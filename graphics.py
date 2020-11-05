'''module to load graphics, convert them to pygame-surface and use them in the main.py.'''

import pygame as g
import os

g.init()

#Set up Display
DISPLAY = g.display.set_mode((0, 0), g.FULLSCREEN)

#gaming board
path = "Graphics/Board/"
name = "background_board.jpg"
BACKGROUND = g.image.load(os.path.join(path, name))
BACKGROUND.convert()

#Tokens
path = "Graphics/Tokens/"
name = "Redtoken.png"
REDTOKEN = g.image.load(os.path.join(path, name))
REDTOKEN.convert()
red_token_rect = REDTOKEN.get_rect()
g.draw.rect(DISPLAY, 255, red_token_rect)
name = "Greentoken.png"
GREENTOKEN = g.image.load(os.path.join(path, name))
GREENTOKEN.convert()
name = "Bluetoken.png"
BLUETOKEN = g.image.load(os.path.join(path, name))
BLUETOKEN.convert()
name = "Blacktoken.png"
BLACKTOKEN = g.image.load(os.path.join(path, name))
BLACKTOKEN.convert()
name = "Whitetoken.png"
WHITETOKEN = g.image.load(os.path.join(path, name))
WHITETOKEN.convert()
