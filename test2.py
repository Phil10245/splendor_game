import pygame as g
import random
from classes import *
from colours import *

g.init()
WIDTH, HEIGHT = 1330, 1000
win = g.display.set_mode((WIDTH, HEIGHT))

win.fill(WHITE)

lst_cards = []

for difficulty_level in range(3):
    y = 100 + difficulty_level * 160 # determining the y coordinate
    for __ in range(4):   #instance the 4 card
        x = 465 + __ * 130 # determining the x coordinate
        c = Card(difficulty_level, x, y, 120, 150, g.font.SysFont("comicsans", 30))
        c.draw(win)
        lst_cards.append(c)

g.display.update()

run = True

while run:

    for event in g.event.get():
        if event.type == g.QUIT:
            run = False

    g.event.wait()
