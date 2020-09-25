import pygame as g
import random
from classes import *
from colours import *

g.init()
WIDTH, HEIGHT = 1330, 1000
win = g.display.set_mode((WIDTH, HEIGHT))

win.fill(WHITE)

lst_cards = []

res = Ressources(win)

g.display.update()

run = True

while run:

    for event in g.event.get():
        if event.type == g.QUIT:
            run = False

    g.event.wait()
