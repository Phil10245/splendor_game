import pygame as g
import random
from classes import *
from colours import *

g.init()
WIDTH, HEIGHT = 1330, 1000
win = g.display.set_mode((WIDTH, HEIGHT))

win.fill(WHITE)
newC = Card(1, 600, 400, 210, 190, g.font.SysFont("comicsans", 30))
print(newC.colour)
newC.draw(win)
g.display.update()

g.time.wait(10000)
