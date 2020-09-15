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
PADDING_V = 100
PADDING_H = 100
RECTWIDTHB = 90
RECTHEIGHTB = 90

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
        rx , ry = x + 45 , y + 20 # initial placing of the ressource numbers
        # cost
        for ress, col in ((card.green, GREEN), (card.blue, BLUE), (card.red, RED), (card.blck, BLACK)):
            text = LETTER_FONT.render(str(ress),1,col)
            win.blit(text, (rx , ry))
            ry += 20
        #color
        if card.colour == 1: O = GREEN
        if card.colour == 2: O = LIGHTBLUE
        if card.colour == 3: O = RED
        if card.colour == 4: O = BLACK
        colour = LETTER_FONT.render("O", 1, O)
        win.blit(colour, (x + 70, y + 5))

    #draw bonus cards (available)
    for card in boni.deck:
        x, y = card.x, card.y
        g.draw.rect(win, BLACK, g.Rect(x, y, RECTWIDTHB, RECTHEIGHTB), 2)
        #points
        points = LETTER_FONT.render(str(card.points) ,1,BLACK)
        win.blit(points,(x + 5, y + 5))
        # cost
        rx , ry = x + 35 , y + 10 # initial placing of the ressource numbers
        for ress, col in ((card.green, GREEN), (card.blue, BLUE), (card.red, RED), (card.blck, BLACK)):
            text = LETTER_FONT.render(str(ress),1,col)
            win.blit(text, (rx , ry))
            ry += 20
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
        x = 465 + idx * 75
        if key == "green": col = GREEN
        if key == "blue": col = LIGHTBLUE
        if key == "red": col = RED
        if key == "blck": col = BLACK
        g.draw.rect(win, BLACK, g.Rect(x, y, RECTWIDTHB // 3 * 2, RECTHEIGHTB //3 * 2), 2)
        drw_nbcrds = LETTER_FONT.render(str(crds_count.get(key, 0)), 1, col)
        win.blit(drw_nbcrds,(x+20,y+20))
    #3 player's RessourceStack
    # analog to draw rs
    #circle(surface, color, center, radius, width=0)
    i = 0
    for ress, col in ((ls_plyer[0].green, GREEN), (ls_plyer[0].blue, BLUE), (ls_plyer[0].red, RED), (ls_plyer[0].blck, BLACK)):
        print( ress, col, i)
        if i < 2:
            x = 850
            y = 510 + i * 80
        else:
            x = 930
            y = 510 + (i - 2) * 80
        print( x, y)
        g.draw.circle(win, col, (x, y), 30 , 0)
        a_res = LETTER_FONT.render(str(ress), 1, WHITE)
        win.blit(a_res,(x - 5 , y - 10 ))
        i += 1


    g.display.update()

while run:

    clock.tick(FPS)

    #setup the game:
    #procedure to determine nb of players and crate the instances
    # To be replaed by a menu!
    ls_plyer = list()
    number_of_players = input("Please enter the number of players: ")
    try:
        number_of_players = int(number_of_players)
        if number_of_players < 5 and number_of_players > 0:
            for _ in range(1, number_of_players + 1):
                player_ = Player("player" + str(_), 1, _)
                ls_plyer.append(player_)
                print(player_)
        elif number_of_players == 69:
            break
        else:
            print("Maximum players allowed are 4!")
            continue
    except:
        print("Bad input. Enter a Number between  and 4!!!")
        continue

    rs = RessourceStack(number_of_players)
    ob = OpenBoard()
    boni = BonusBoard()

    print(boni)
    print(ob)
    print(rs)
    #turn of active player -> performs his actions, at the end next.
    #Should be an inner loop !

    draw()
    g.time.wait(15_000)
    run = False

    '''for event in g.event.get():
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
    draw()'''
