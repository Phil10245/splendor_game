from classes import Card, OpenBoard, BonusC, BonusBoard, RessourceStack, Player
import pygame as g
import math

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
RECTWIDTH_CARDDECK = 90
RECTHEIGHT_CARDDECK = 110
PADDING_V = 10
PADDING_H = 10
RECTWIDTHBONI = 90
RECTHEIGHTBONI = 90
RADIUS_PLAYER_RS = 30
RS_RAD = 37
RS_X = 1040
RS_Y = 135
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

def draw_card(card, width, height, color):
    '''draw card obcject, with width and height setting the size of the rectangle
    if color == True: Draw "O"s coloured in the card's colour in the left corner
    if color == False, don't draw the "O"s'''

    g.draw.rect(win, BLACK, g.Rect(card.x, card.y, width, height), 2)
    #points in the right top corner
    points = LETTER_FONT.render(str(card.points) , 1, BLACK)
    win.blit(points,(card.x + 5, card.y + 5))
    # cost
    rx , ry = int(card.x + width/2 - 5) , int(card.y + height/8) # initial placing of the ressource numbers
    for ress, col in ((card.green, GREEN), (card.blue, BLUE), (card.red, RED), (card.blck, BLACK)):
        text = LETTER_FONT.render(str(ress), 1, col)
        win.blit(text, (rx , ry))
        ry += int(height/5)
    #color
    if color == True:
        if card.colour == 1: O = GREEN
        if card.colour == 2: O = LIGHTBLUE
        if card.colour == 3: O = RED
        if card.colour == 4: O = BLACK
        colour = LETTER_FONT.render("O", 1, O)
        win.blit(colour, (card.x + RECTWIDTH_CARDDECK - 20 , card.y + 5))

def draw_rs_stack(rs, x, y, r):
    ''' draw RessourceStack (rs) as 4 colored circles, starting at pos x,y with radius r
    RETURN: lst_res_xy containing the ressources and their coordinates - used in the event listener'''
    i = 0
    lst_res_xy = []
    for ress, col in ((rs.green, GREEN), (rs.blue, BLUE), (rs.red, RED), (rs.blck, BLACK)):
        y_real = y + i * (r * 2 + 2 * PADDING_V)
        g.draw.circle(win, col, (x, y_real), r , 0)
        a_res = LETTER_FONT.render(str(ress), 1, WHITE)
        win.blit(a_res,(x - 5 , y_real - 10 ))
        lst_res_xy.append((i, x, y_real))
        i += 1
    return lst_res_xy

def draw_active_player(plyr):
    ''' Draw name and points of the active player in the lower part of display.
    Render underneath count of the cards he owns, and on the side 4 circles with
    the count of Ressources
    '''
    p_name = plyr.name
    drw_name = LETTER_FONT.render(p_name, 1, BLACK)
    win.blit(drw_name, (465,480))
    p_points = plyr.points
    drw_points = LETTER_FONT.render("Points: " + str(p_points), 1, BLACK)
    win.blit(drw_points, (665,480))
    #2 player stack (simple)
    crds_count = plyr.card_counter()
    y = 510
    for idx, key in enumerate(crds_count):
        x = 465 + idx * 100
        if key == "green": col = GREEN
        if key == "blue": col = LIGHTBLUE
        if key == "red": col = RED
        if key == "blck": col = BLACK
        g.draw.rect(win, BLACK, g.Rect(x, y, RECTWIDTHBONI, RECTHEIGHTBONI), 2)
        drw_nbcrds = LETTER_FONT.render(str(crds_count.get(key, 0)), 1, col)
        win.blit(drw_nbcrds, (int(x + RECTWIDTHBONI / 2 - 5) ,y + int(RECTHEIGHTBONI / 2)))
    #3 player's RessourceStack
    i = 0
    for ress, col in ((plyr.green, GREEN), (plyr.blue, BLUE), (plyr.red, RED), (plyr.blck, BLACK)):
        x = 900 + ((RADIUS_PLAYER_RS * 2 + PADDING_H) * (i % 2))
        '< für i = 0 und i = 2 wird der 2. Teil der Summe 0!'
        y = 540 + ((i // 2) * (PADDING_V + RADIUS_PLAYER_RS *2))
        ' "//" ist der Integerdivisioner > der Ausdruck ist somit 0 solange i < 2, dann 1, bis i = 4'
        g.draw.circle(win, col, (x, y), RADIUS_PLAYER_RS , 0)
        a_res = LETTER_FONT.render(str(ress), 1, WHITE)
        win.blit(a_res,(x - 5 , y - 10 ))
        i += 1

def draw():

    win.fill(WHITE)

    #draw Title
    text = TITLE_FONT.render("Splendor", 1, BLUE)
    win.blit(text, (int(WIDTH/2 - text.get_width()/2), 20))

    #Draw board
    #-------------------------------
    #draw carddeck (openboard)
    for card in ob.deck:
        draw_card(card, RECTWIDTH_CARDDECK, RECTHEIGHT_CARDDECK, True)

    # draw bonus cards (available)
    for card in boni.deck:
        draw_card(card, RECTWIDTHBONI, RECTHEIGHTBONI, False)
    # draw ressource stack
    rs_coordinates = draw_rs_stack(rs, RS_X, RS_Y, RS_RAD)

    #draw active player's stack (cards, points, ress)
    draw_active_player(ls_plyer[active_player_id])

    g.display.update()

    return rs_coordinates

#Players and active_player_id:
ls_plyer = [Player("Catherine",1,1), Player("Philipp",1,1)]
active_player_id = 0

rs = RessourceStack(len(ls_plyer))
ob = OpenBoard()
boni = BonusBoard()

print(boni)
print(ob)
print(rs)
print("length player_list:", len(ls_plyer))
# game counter, to track actions done by active player
cntr_pck_crd = 0
cntr_pck_res_as_lst = [0, 0, 0, 0]

while run:
    clock.tick(FPS)

    #turn of active player -> performs his actions, at the end next.
    #Should be an inner loop !

    rs_coordinates = draw()

    for event in g.event.get():
        if event.type == g.QUIT:
            run = False
        if event.type == g.MOUSEBUTTONDOWN:
            m_x, m_y = g.mouse.get_pos()
            print(m_x, m_y)
            #player klicks on card
            for id_clicked_card, clicked_card in enumerate(ob.deck):
                if m_x > clicked_card.x and m_x < clicked_card.x + RECTWIDTH_CARDDECK and m_y > clicked_card.y and m_y < clicked_card.y + RECTHEIGHT_CARDDECK:
                    if 1 in cntr_pck_res_as_lst:
                        #TO DO: render some messagetext
                        print("invalid move")
                        continue
                    else:
                        g.draw.rect(win, LIGHTBLUE, g.Rect(clicked_card.x, clicked_card.y, RECTWIDTH_CARDDECK, RECTHEIGHT_CARDDECK), 2)
                        g.display.update()
                        # implement the replaceCard calL!
                        success = ls_plyer[active_player_id].pick_crd(ob, id_clicked_card, rs)
                        if success:
                            cntr_pck_crd += 1
                            print("Player:", ls_plyer[active_player_id].name)
                            print("Deck:", ls_plyer[active_player_id].cardstack)
                            #g.display.update()
            #player klicks on ressources
            for id_clicked_ress, x, y in rs_coordinates:
                #Calculating distance between mouse and letters = collision_detection
                dis = math.sqrt((x-m_x)**2 + (y - m_y)**2)
                if dis < RS_RAD:
                    g.draw.circle(win, LIGHTBLUE, (x, y), RS_RAD , 2)
                    g.display.update()
                    success = ls_plyer[active_player_id].take_res(id_clicked_ress, rs)
                    print("DEBUG: suucess picking res:", success,  id_clicked_ress)
                    if success:
                        if id_clicked_ress == 0:
                            cntr_pck_res_as_lst[0] += 1
                    if id_clicked_ress == 1:
                        cntr_pck_res_as_lst[1] += 1
                    if id_clicked_ress == 2:
                        cntr_pck_res_as_lst[2] += 1
                    if id_clicked_ress == 3:
                        cntr_pck_res_as_lst[3] += 1
    draw()

    g.time.wait(3_000)



    if cntr_pck_crd == 1 or 2 in cntr_pck_res_as_lst or sum(cntr_pck_res_as_lst) == 3:
        if active_player_id < len(ls_plyer) - 1 :
            active_player_id += 1
            cntr_pck_res_as_lst = [0, 0, 0, 0]
            cntr_pck_crd = 0
        else:
            active_player_id = 0
            cntr_pck_res_as_lst = [0, 0, 0, 0]
            cntr_pck_crd = 0



g.quit()
