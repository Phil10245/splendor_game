from classes import *
import pygame as g
import math

g.init()

#font
LETTER_FONT = g.font.SysFont("comicsans", 30)
WORD_FONT = g.font.SysFont("comicsans", 60)
LOSE_FONT = g.font.SysFont("comicsans", 120)
TITLE_FONT = g.font.SysFont("comicsans", 50)
# colours
WHITE = (255, 255, 255)
BLACK = (0,0,0)
YELLOW = (255,255,0)
DARKYELLOW = (150,100,0)
BLUE = (0,0,200)
RED = (255,0,0)
GREEN = (0,200,0)
LIGHTBLUE = (0,200,252)

#setup drawings:
#1 Rect
BUTTON_WIDTH = 300
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

def change_number_of_players(number):
        if number < 4:
            return number + 1
        else:
            return 1

def draw_menu_page(screen):
    win.fill(DARKYELLOW)
    start_b.draw(screen)
    number_player_b.draw(screen)
    for player in input_name_boxes:
        if player.visible:
            player.draw(screen)
    exit_b.draw(screen)
    g.display.update()

def display_game_notification(message1, message2=""):
    g.time.delay(100)
    text = WORD_FONT.render(message1, 1, BLUE)
    if len(message2) == 0:
        text2 = WORD_FONT.render(message2, 1, LIGHTBLUE)
        win.blit(text2, (WIDTH / 2 - text2.get_width() / 2 , HEIGHT / 2 - text.get_height() / 3))
    win.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 3))
    g.display.update()
    g.time.delay(2_000)

def display_message (message1, message2):
    g.time.delay(2_000)
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
    win.blit(drw_name, (465,480))
    p_points = plyr.points
    drw_points = LETTER_FONT.render("Points: " + str(p_points), 1, BLACK)
    win.blit(drw_points, (665,480))
    #2 player stack (simple)
    y = 510
    for idx, key in enumerate(plyr.crds_count):
        x = 465 + idx * 100
        if key == "green": col = GREEN
        if key == "blue": col = LIGHTBLUE
        if key == "red": col = RED
        if key == "blck": col = BLACK
        g.draw.rect(win, BLACK, g.Rect(x, y, RECTWIDTHBONI, RECTHEIGHTBONI), 2)
        drw_nbcrds = LETTER_FONT.render(str(plyr.crds_count.get(key)), 1, col)
        win.blit(drw_nbcrds, (int(x + RECTWIDTHBONI / 2 - 5) ,y + int(RECTHEIGHTBONI / 2)))
    #3 player's RessourceStack
    i = 0
    for ress, col in ((plyr.ressources["green"], GREEN), (plyr.ressources["blue"], BLUE), (plyr.ressources["red"], RED), (plyr.ressources["blck"], BLACK)):
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
#The start menu should be here
#another while loop?
#Players and active_player / id:
ls_plyer = [Player("Catherine",1), Player("Philipp",1)]
active_player_id = 0


rs = RessourceStack(len(ls_plyer))
ob = OpenBoard()
boni = BonusBoard()

# game counter, to track actions done by active player
cntr_pck_crd = 0
cntr_pck_res_as_dict = Ressources()


in_menu = True
run = True
#menu and start_screen
while in_menu:
    clock.tick(FPS)
    win.fill(WHITE)
    draw_menu_page(win)

    for event in g.event.get():
        if event.type == g.QUIT:
            run = in_menu = False
        for box in input_name_boxes:
            box.handle_event(event)
        if start_b.handle_event(event):
            in_menu = False
        if exit_b.handle_event(event):
            run = in_menu = False
        if number_player_b.handle_event(event):
            number_player_b.increase_num(4, win)

#game_loop
while run:
    clock.tick(FPS)

    active_player = ls_plyer[active_player_id]

    dict_rs_coordinates = draw()

    for event in g.event.get():
        if event.type == g.QUIT:
            run = False
        if event.type == g.MOUSEBUTTONDOWN:
            m_x, m_y = g.mouse.get_pos()
            #player klicks on card
            for id_clicked_card, clicked_card in enumerate(ob.deck):
                if m_x > clicked_card.x and m_x < clicked_card.x + RECTWIDTH_CARDDECK and m_y > clicked_card.y and m_y < clicked_card.y + RECTHEIGHT_CARDDECK:
                    if 1 in cntr_pck_res_as_dict.values():
                        display_game_notification("That won't work!", "Insufficient Ressources")
                        continue
                    else:
                        g.draw.rect(win, LIGHTBLUE, g.Rect(clicked_card.x, clicked_card.y, RECTWIDTH_CARDDECK, RECTHEIGHT_CARDDECK), 2)
                        g.display.update()
                        g.time.wait(800)
                        # check if player can take card and if so replace it.
                        success = active_player.pick_crd(clicked_card, rs)
                        if success:
                            cntr_pck_crd += 1
                            ob.replace_card(id_clicked_card)
                            if clicked_card.points > 0:
                                display_game_notification(f"{clicked_card.points} points are added to your points!")
                    #check if player qualifies for any bonus
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
                    g.time.wait(800)
                    if cntr_pck_res_as_dict[k] == 0 or sum(cntr_pck_res_as_dict.values()) - cntr_pck_res_as_dict[k] == 0:
                        success = active_player.take_res(k, rs)
                        display_game_notification(f"1 of the {k} ressources added to your stack")
                    else:
                        display_game_notification("You can either take 2X the same, or 3 different ones!!! DUCKER!")
                        success = False
                    if success:
                        cntr_pck_res_as_dict[k] += 1
    draw()

    g.time.wait(1_000)

    if active_player_id == 0:
        for player in ls_plyer:
            if player.points >= 15:
                run = False
                display_message(f"Gratulations!!!\n {active_player.name}",
                "You won! Well done. Yo're amazing and sexy!!!")


    if cntr_pck_crd == 1 or 2 in cntr_pck_res_as_dict.values() or sum(cntr_pck_res_as_dict.values()) == 3:
        if active_player_id < len(ls_plyer) - 1 :
            active_player_id += 1
            cntr_pck_res_as_dict = Ressources()
            cntr_pck_crd = 0
        else:
            active_player_id = 0
            cntr_pck_res_as_dict = Ressources()
            cntr_pck_crd = 0
        display_game_notification(f"It's {ls_plyer[active_player_id].name}'s turn :)")




g.quit()
