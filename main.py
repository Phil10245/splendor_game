from classes import Card, OpenBoard, BonusC, BonusBoard, RessourceStack, Player
import pygame as g

#defining all known funcs, needed for the game not implemented in classes:
#check func -> already implented in player class.

#check points -> if >=15 game ends,playyer wins

#check if a player fulfills the pattern to receive a bonus card:
#after each turn. check for all bonuscards

#count game_stats like nb of turns and print points of all players

#copying the code from hangman game - to be adapted but for a first intuition

#to determine active player: Use ls_plyer : [0] is active player -> goes in last positon after his turn.
# OR iterate over the list

#make a draw_points() as it is repeated for boni and card deck
# same for cost.

#setup display
g.init()
WIDTH, HEIGHT = 1330, 1000
win = g.display.set_mode((WIDTH, HEIGHT))
g.display.set_caption("Splendor 0.9")

#font
LETTER_FONT = g.font.SysFont("comicsans", 30)
WORD_FONT = g.font.SysFont("comicsans", 60)
LOSE_FONT = g.font.SysFont("comicsans", 120)
TITLE_FONT = g.font.SysFont("comicsans", 50)
# colours
WHITE = (255, 255, 255)
BLACK = (0,0,0)
YELLOW = (255,255,0)
BLUE = (0,0,200)
RED = (255,0,0)
GREEN = (0,200,0)
LIGHTBLUE = (0,200,252)

#setup drawings:
#1 Rect
RECTWIDTH = 90
RECTHEIGHT = 110
PADDING_V = 10
PADDING_H = 10
RECTWIDTHB = 90
RECTHEIGHTB = 90
RADIUSP = 30

#setup game loop
FPS = 60
clock = g.time.Clock()
run = True


def display_message (message1, message2):
    g.time.delay(2000)
    text = LOSE_FONT.render(message1, 1, RED)
    text2 = TITLE_FONT.render(message2, 1, BLUE)
    win.fill(WHITE)
    win.blit(text, (300,275))
    win.blit(text2, (300,350))
    g.display.update()
    g.time.delay(3000)


def draw():

    win.fill(WHITE)

    #draw Title
    text = TITLE_FONT.render("Splendor", 1, BLUE)
    win.blit(text, (int(WIDTH/2 - text.get_width()/2), 20))

    #draw board
    #draw carddeck (openboard)
    for card in ob.deck:
        x, y = card.x, card.y
        g.draw.rect(win, BLACK, g.Rect(x, y, RECTWIDTH, RECTHEIGHT), 2)
        #points
        points = LETTER_FONT.render(str(card.points) ,1,BLACK)
        win.blit(points,(x + 5, y + 5))
        # cost
        rx , ry = int(x + RECTWIDTH/2 - 5) , int(y + RECTHEIGHT/8) # initial placing of the ressource numbers
        for ress, col in ((card.green, GREEN), (card.blue, BLUE), (card.red, RED), (card.blck, BLACK)):
            text = LETTER_FONT.render(str(ress), 1, col)
            win.blit(text, (rx , ry))
            ry += int(RECTHEIGHT/5)
        #color
        if card.colour == 1: O = GREEN
        if card.colour == 2: O = LIGHTBLUE
        if card.colour == 3: O = RED
        if card.colour == 4: O = BLACK
        colour = LETTER_FONT.render("O", 1, O)
        win.blit(colour, (x + RECTWIDTH - 20 , y + 5))

    #draw bonus cards (available)
    for card in boni.deck:
        x, y = card.x, card.y
        g.draw.rect(win, BLACK, g.Rect(x, y, RECTWIDTHB, RECTHEIGHTB), 2)
        #points
        points = LETTER_FONT.render(str(card.points) ,1,BLACK)
        win.blit(points,(x + 5, y + 5))
        # cost
        rx , ry = x + 35 , int(y + RECTHEIGHTB/8) # initial placing of the ressource numbers
        for ress, col in ((card.green, GREEN), (card.blue, BLUE), (card.red, RED), (card.blck, BLACK)):
            text = LETTER_FONT.render(str(ress),1,col)
            win.blit(text, (rx , ry))
            ry += int(RECTHEIGHTB/5)
    # draw ressource stack  (variable name: rs)
    #circle(surface, color, center, radius, width=0)
    x = 1040
    i = 0
    for ress, col in ((rs.green, GREEN), (rs.blue, BLUE), (rs.red, RED), (rs.blck, BLACK)):
        print( ress, col, i)
        y = 135 + i * 90
        print( x, y)
        g.draw.circle(win, col, (x, y), 37 , 0)
        a_res = LETTER_FONT.render(str(ress), 1, WHITE)
        win.blit(a_res,(x - 5 , y - 10 ))
        i += 1


    #draw active player's stack (cards, points, ress)
    #1 player_name & points
    p_name = ls_plyer[0].name
    drw_name = LETTER_FONT.render(p_name, 1, BLACK)
    win.blit(drw_name, (465,480))
    p_points = ls_plyer[0].points
    drw_points = LETTER_FONT.render("Points: " + str(p_points), 1, BLACK)
    win.blit(drw_points, (665,480))
    #2 player stack (simple)
    crds_count = {"green": 0, "blue": 0, "red": 0, "blck": 0}
    for card in ls_plyer[0].cardstack:
        if card.colour == 1:
            crds_count[green] = crds_count.get(green, 0) + 1
        if card.colour == 2:
            crds_count[blue] = crds_count.get(blue, 0) + 1
        if card.colour == 3:
            crds_count[red] = crds_count.get(red, 0) + 1
        if card.colour == 4:
            crds_count[blck] = crds_count.get(blck, 0) + 1
    print(crds_count)
    y = 510
    for idx, key in enumerate(crds_count):
        x = 465 + idx * 100
        if key == "green": col = GREEN
        if key == "blue": col = LIGHTBLUE
        if key == "red": col = RED
        if key == "blck": col = BLACK
        g.draw.rect(win, BLACK, g.Rect(x, y, RECTWIDTHB, RECTHEIGHTB), 2)
        drw_nbcrds = LETTER_FONT.render(str(crds_count.get(key, 0)), 1, col)
        win.blit(drw_nbcrds, (int(x + RECTWIDTHB / 2 - 5) ,y + int(RECTHEIGHTB / 2)))
    #3 player's RessourceStack
    i = 0
    for ress, col in ((ls_plyer[0].green, GREEN), (ls_plyer[0].blue, BLUE), (ls_plyer[0].red, RED), (ls_plyer[0].blck, BLACK)):
        print( ress, col, i)
        x = 900 + ((RADIUSP * 2 + PADDING_H) * (i % 2))
        '< für i = 0 und i = 2 wird der 2. Teil der Summe 0!'
        y = 540 + ((i // 2) * (PADDING_V + RADIUSP *2))
        ' "//" ist der Integerdivisioner > der Ausdruck ist somit 0 solange i < 2, dann 1, bis i = 4'
        print( x, y)
        g.draw.circle(win, col, (x, y), RADIUSP , 0)
        a_res = LETTER_FONT.render(str(ress), 1, WHITE)
        win.blit(a_res,(x - 5 , y - 10 ))
        i += 1


    g.display.update()

ls_plyer = [Player("Catherine",1,1),Player("Philipp",1,1)]
rs = RessourceStack(len(ls_plyer))
ob = OpenBoard()
boni = BonusBoard()

while run:

    clock.tick(FPS)

    #setup the game:
    #procedure to determine nb of players and crate the instances
    # To be replaed by a menu!


    print(boni)
    print(ob)
    print(rs)
    #turn of active player -> performs his actions, at the end next.
    #Should be an inner loop !

    draw()

    for event in g.event.get():
        if event.type == g.QUIT:
            run = False
        if event.type == g.MOUSEBUTTONDOWN:
            m_x, m_y = g.mouse.get_pos()
            for letter in letters:
                x, y, ltr, visible = letter
                if visible:
                    'Calculating distance between mouse and letters = collision_detection:'
                    dis = math.sqrt((x-m_x)**2 + (y - m_y)**2)
                    if dis < RADIUS:
                         letter[3] = False
                         guessed.append(letter[2])
                         print(guessed)
                         if letter[2] not in word:
                            hm_stat += 1
                            print(hm_stat)
    draw()
