from classes import *
from colours import *
import pygame as g
import math


g.init()

#font
LETTER_FONT = g.font.SysFont("comicsans", 30)
WORD_FONT = g.font.SysFont("comicsans", 60)
LOSE_FONT = g.font.SysFont("comicsans", 120)
TITLE_FONT = g.font.SysFont("comicsans", 50)
# colours


#setup drawings:
#1 Rect
BUTTON_WIDTH = 300
RECTWIDTH_CARDDECK = 90
RECTHEIGHT_CARDDECK = 120
RECT_P_RES = 70
PADDING_V = 10
PADDING_H = 10
RECTWIDTHBONI = 90
RECTHEIGHTBONI = 90
RADIUS_PLAYER_RS = 35
RS_RAD = 37
RS_X = 1040
RS_Y = 135

def draw_menu_page(screen):
    win.fill(DARKYELLOW)
    start_b.draw(screen)
    number_player_b.draw(screen)
    for box in input_name_boxes:
        if box.visible:
            box.draw(screen)
    exit_b.draw(screen)
    g.display.update()

def display_game_notification(message1, message2=""):
    text = WORD_FONT.render(message1, 1, BLUE)
    if len(message2) == 0:
        text2 = WORD_FONT.render(message2, 1, LIGHTBLUE)
        win.blit(text2, (WIDTH / 2 - text2.get_width() / 2 , HEIGHT / 2 - text.get_height() / 2))
    win.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 3))
    g.display.update()
    g.time.delay(1_500)

def display_message (message1, message2):
    g.time.delay(1_000)
    text = LOSE_FONT.render(message1, 1, BLUE)
    text2 = TITLE_FONT.render(message2, 1, LIGHTBLUE)
    win.fill(WHITE)
    win.blit(text, (300,275))
    win.blit(text2, (300,350))
    g.display.update()
    g.time.delay(10_000)

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
    for ress, col in ((card.ressources["green"], GREEN), (card.ressources["blue"], BLUE), (card.ressources["red"], RED), (card.ressources["blck"], BLACK)):
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

def draw_rs_stack(rs, x, ystart, r):
    ''' draw RessourceStack (rs) as 4 colored circles, starting at pos x,y with radius r
    RETURN: lst_res_xy containing the ressources and their coordinates - used in the event listener'''
    i = 0
    dict_res_xy = {}
    for ress, col in (("green", GREEN), ("blue", BLUE), ("red", RED), ("blck", BLACK)):
        y = ystart + i * (r * 2 + 2 * PADDING_V)
        g.draw.circle(win, col, (x, y), r , 0)
        a_res = LETTER_FONT.render(str(rs.ressources[ress]), 1, WHITE)
        win.blit(a_res,(x - 5 , y - 10 ))
        dict_res_xy[ress] = (x, y)
        i += 1
    return dict_res_xy

def draw_active_player(plyr):
    ''' Draw name and points of the active player in the lower part of display.
    Render underneath count of the cards he owns, and on the side 4 circles with
    the count of Ressources
    '''
    p_name = plyr.name
    drw_name = LETTER_FONT.render(p_name, 1, BLACK)
    win.blit(drw_name, (465,510))
    p_points = plyr.points
    drw_points = LETTER_FONT.render("Points: " + str(p_points), 1, BLACK)
    win.blit(drw_points, (665,510))
    #2 player stack (simple)
    y = 530
    for idx, key in enumerate(plyr.crds_count):
        x = 465 + idx * (RECT_P_RES + PADDING_H)
        if key == "green": col = GREEN
        if key == "blue": col = LIGHTBLUE
        if key == "red": col = RED
        if key == "blck": col = BLACK
        if key == "white": col == WHITE
        g.draw.rect(win, BLACK, g.Rect(x, y, RECT_P_RES, RECT_P_RES), 2)
        drw_nbcrds = LETTER_FONT.render(str(plyr.crds_count.get(key)), 1, col)
        win.blit(drw_nbcrds, (int(x + RECT_P_RES / 2 - 5) ,y + int(RECT_P_RES / 2)))
    #3 player's RessourceStack
    i = 0
    for ress, col in ((plyr.ressources["green"], GREEN), (plyr.ressources["blue"], BLUE), (plyr.ressources["red"], RED), (plyr.ressources["blck"], BLACK), (plyr.ressources["white"], WHITE)):
        y = 608 + RADIUS_PLAYER_RS + PADDING_V
        x = 465 + RADIUS_PLAYER_RS + (PADDING_H + RADIUS_PLAYER_RS * 2) * i
        g.draw.circle(win, col, (x, y), RADIUS_PLAYER_RS , 0)
        a_res = LETTER_FONT.render(str(ress), 1, WHITE)
        win.blit(a_res,(x - 5 , y - 5 ))
        i += 1

def draw():

    win.fill(DARKYELLOW)

    #draw Title
    text = TITLE_FONT.render("Splendor", 1, BLUE)
    win.blit(text, (int(WIDTH/2 - text.get_width()/2), 20))

    #Draw board
    #-------------------------------
    #draw carddeck
    for card in lst_cards:
        card.draw(win)

    # draw bonus cards (available)
    for card in boni.deck:
        draw_card(card, RECTWIDTHBONI, RECTHEIGHTBONI, False)
    # draw ressource stack
    dict_rs_coordinates = draw_rs_stack(rs, RS_X, RS_Y, RS_RAD)

    #draw active player's stack (cards, points, ress)
    draw_active_player(active_player)

    g.display.update()

    return dict_rs_coordinates


#setup display

WIDTH, HEIGHT = 1330, 1000
win = g.display.set_mode((WIDTH, HEIGHT))
g.display.set_caption("Splendor 0.9")

#setup game loop
FPS = 60
clock = g.time.Clock()

#setting up start menu:
start_b = Button(WIDTH / 2, HEIGHT / 2 - 300, BUTTON_WIDTH, 50, LETTER_FONT, "START")
exit_b = Button(WIDTH / 2, HEIGHT / 2 + 200, BUTTON_WIDTH, 50, LETTER_FONT, text="END")
number_player_b = Button(WIDTH / 2 - 70, HEIGHT / 2 - 200, 50, 50, LETTER_FONT, "2")
name_player1 = InputBox(WIDTH / 2 , 0, BUTTON_WIDTH, 50, LETTER_FONT, "Player1")
name_player2 = InputBox(WIDTH / 2 , 0, BUTTON_WIDTH, 50, LETTER_FONT, text="Player2")
name_player3 = InputBox(WIDTH / 2 , 0, BUTTON_WIDTH, 50, LETTER_FONT, text="Player3")
name_player4 = InputBox(WIDTH / 2 , 0, BUTTON_WIDTH, 50, LETTER_FONT, text="Player4")
input_name_boxes = [name_player1, name_player2, name_player3, name_player4]
y = -200
for input_box in input_name_boxes:
    input_box.rect.move_ip(0, HEIGHT / 2 + y)
    y += 100

#initiate the 12 cards of the carddeck
lst_cards = []
for difficulty_level in range(3):
    y = 100 + difficulty_level * (PADDING_V + RECTHEIGHT_CARDDECK) # determining the y coordinate
    for __ in range(4):   #instance the 4 card
        x = 465 + __ * ( PADDING_H + RECTWIDTH_CARDDECK)# determining the x coordinate
        c = Card(difficulty_level, x, y, RECTWIDTH_CARDDECK, RECTHEIGHT_CARDDECK, LETTER_FONT)
        lst_cards.append(c)

# game counter, to track actions done by active player
cntr_pck_crd = 0
cntr_pck_res_as_dict = Ressources()


in_menu = True
run = True
i = 0
#menu and start_screen
lst_player_names = []
while in_menu:
    clock.tick(FPS)
    win.fill(WHITE)
    draw_menu_page(win)


    for event in g.event.get():
        if event.type == g.QUIT:
            run = in_menu = False
        for box in input_name_boxes:
            box.handle_event(event)
            number_player_b.active = False
        if start_b.handle_event(event):
            in_menu = False
            number_player_b.active = False
            for box in input_name_boxes:
                if box.visible:
                    lst_player_names.append(box.text)
        if exit_b.handle_event(event):
            run = in_menu = False
            number_player_b.active = False
        if number_player_b.handle_event(event):
            i = number_player_b.increase_num(4, win)
            for box in input_name_boxes[:i]:
                box.visible = True
            for box in input_name_boxes[i:]:
                box.visible = False

#Players and active_player / id:
lst_player = []
for player in lst_player_names:
    lst_player.append(Player(str(player), 1))
active_player_id = 0


rs = RessourceStack(len(lst_player))
boni = BonusBoard()

#game_loop
while run:
    clock.tick(FPS)

    active_player = lst_player[active_player_id]

    dict_rs_coordinates = draw()

    for event in g.event.get():
        if event.type == g.QUIT:
            run = False
        if event.type == g.MOUSEBUTTONDOWN:
            m_x, m_y = g.mouse.get_pos()
            for card_id, card in enumerate(lst_cards):
                if card.handle_event(event):
                    g.draw.rect(win, LIGHTBLUE, card.rect, 5)
                    g.display.update()
                    if 1 in cntr_pck_res_as_dict.values():
                        display_game_notification("That won't work!", "You took already a ressource.")
                        continue
                    else:
                        # check if player can take card and if so replace it. refactor i one function - one task
                        success = active_player.pick_crd(card, rs)
                        if success:
                            cntr_pck_crd += 1
                            if card.points > 0:
                                display_game_notification(f"{card.points} points are added to your points!")
                            card.replace_card(card_id, lst_cards)
                        else:
                            display_game_notification("Not enough Ressources")
                    #TODO: Seems incomplete. Should be a for loop over the three cards?
                    if active_player.check_if_qualified_for_bonus(boni):
                        active_player.points += 3
                        boni.remove(id)
                        display_game_notification("Awesome!!! You just earned a bonus", f"{bonus.points} are added to your points.")
            #player klicks on ressources
            for k in dict_rs_coordinates:
                #Calculating distance between mouse and ressources = collision_detection
                x = dict_rs_coordinates[k][0]
                y = dict_rs_coordinates[k][1]
                dis = math.sqrt((x-m_x)**2 + (y - m_y)**2)
                if dis < RS_RAD / 2:
                    g.draw.circle(win, LIGHTBLUE, (x, y), RS_RAD , 2)
                    g.display.update()
                    if cntr_pck_res_as_dict[k] == 0 or sum(cntr_pck_res_as_dict.values()) - cntr_pck_res_as_dict[k] == 0:
                        success = active_player.take_res(k, rs)
                        display_game_notification(f"1 of the {k} ressources added to your stack")
                    else:
                        display_game_notification("You can either take 2X the same, or 3 different ones!!! DUCKER!")
                        success = False
                    if success:
                        cntr_pck_res_as_dict[k] += 1
            g.time.wait(800)

    draw()

    g.time.wait(1_000)

    if active_player_id == 0:
        for player in lst_player:
            if player.points >= 15:
                run = False
                display_message(f"Gratulations!!!\n {active_player.name}",
                "You won! Well done. Yo're amazing and sexy!!!")


    if cntr_pck_crd == 1 or 2 in cntr_pck_res_as_dict.values() or sum(cntr_pck_res_as_dict.values()) == 3:
        if active_player_id < len(lst_player) - 1 :
            active_player_id += 1
            cntr_pck_res_as_dict = Ressources()
            cntr_pck_crd = 0
        else:
            active_player_id = 0
            cntr_pck_res_as_dict = Ressources()
            cntr_pck_crd = 0
        display_game_notification(f"It's {lst_player[active_player_id].name}'s turn :)")




g.quit()
