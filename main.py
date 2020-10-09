'''
The main module of the splendor game. The GUI is set up here.
The module contains four parts: Constants and function definitions,
the pre-game-menu-loop and the game loop
'''

import sys
import pygame as g
from pygame.locals import *
from classes import Button, InputBox, Card, BonusC, Resources, Resourcestack, Player
from colours import WHITE, BLACK, BLUE, LIGHTBLUE, DARKYELLOW, HIGHLIGHTORANGE

g.init()

#font
LETTER_FONT = g.font.SysFont("comicsans", 30)
WORD_FONT = g.font.SysFont("comicsans", 60)
LOSE_FONT = g.font.SysFont("comicsans", 120)
TITLE_FONT = g.font.SysFont("comicsans", 50)

#setup display
WIDTH, HEIGHT = 1300, 1000
win = g.display.set_mode((WIDTH, HEIGHT))
g.display.set_caption("Splendor 0.9")

#setup gui
SIDEBAR_WIDTH = int(WIDTH / 4)
REDUCED_WIDTH = WIDTH - SIDEBAR_WIDTH
BUTTON_WIDTH = int(REDUCED_WIDTH / 3)
INGAME_BUTTON = int(REDUCED_WIDTH / 12)
RECTWIDTH_CARDDECK = int(REDUCED_WIDTH / 10)
RECTHEIGHT_CARDDECK = int(HEIGHT / 8)
RECTSQUARE_PLAYER_CARDS = int(REDUCED_WIDTH / 10)
PADDING_V = int(WIDTH / 100)
PADDING_H = int(REDUCED_WIDTH / 100)
RECTWIDTHBONI = int(REDUCED_WIDTH / 10)
RECTHEIGHTBONI = int(HEIGHT / 8)
RADIUS_PLAYER_RS = int(REDUCED_WIDTH / 25)
RADIUS_RESOURCES = int(REDUCED_WIDTH / 24)

START_X_CARDS = SIDEBAR_WIDTH + int(WIDTH / 2.5) - (RECTWIDTH_CARDDECK + PADDING_H)*2
START_Y_CARDS = TITLE_FONT.get_height() + 2*PADDING_V
START_X_PLAYER = START_X_CARDS
START_Y_PLAYER = START_Y_CARDS + 7*PADDING_V + 10*RADIUS_RESOURCES
START_Y_PLAYER_CARDS = START_Y_PLAYER + PADDING_V + LETTER_FONT.get_height()
START_X_PLAYER_RS = START_X_CARDS + int(RECTSQUARE_PLAYER_CARDS/ 2)
START_Y_PLAYER_RS = START_Y_PLAYER_CARDS + RECTSQUARE_PLAYER_CARDS + PADDING_V*2 + RADIUS_PLAYER_RS
START_X_BONI = START_X_CARDS + (RECTWIDTH_CARDDECK + PADDING_H)*4 + PADDING_H*2
START_Y_BONI = START_Y_CARDS
START_X_RS = START_X_BONI + RECTWIDTHBONI + 4*PADDING_H + int(RADIUS_RESOURCES/2)
START_Y_RS = START_Y_CARDS + 2*RADIUS_RESOURCES


def draw_menu_page(screen):
    win.fill(DARKYELLOW)
    start_b.draw(screen)
    number_player_b.draw(screen)
    for b in input_name_boxes:
        if b.visible:
            b.draw(screen)
    exit_b.draw(screen)
    g.display.update()

def display_game_notification(message1, message2=""):
    text = WORD_FONT.render(message1, 1, BLUE)
    if len(message2) != 0:
        text2 = WORD_FONT.render(message2, 1, LIGHTBLUE)
        win.blit(text2, (int(win.get_width() / 2) - text2.get_width() // 2, int(win.get_height() / 2 )))
    win.blit(text, (int(win.get_width() / 2) - text.get_width() // 2, int(win.get_height() / 2) - text.get_height()))
    g.display.update()
    g.time.delay(1_500)

def display_message (message1, message2):
    g.time.delay(1_000)
    text = LOSE_FONT.render(message1, 1, BLUE)
    text2 = TITLE_FONT.render(message2, 1, LIGHTBLUE)
    win.fill(WHITE)
    win.blit(text, (win.get_width() / 2, win.get_height() / 4))
    win.blit(text2, (win.get_width() / 2, win.get_height() / 2 ))
    g.display.update()
    g.time.delay(10_000)

def highlight_rect(rect:Rect):
    g.draw.rect(win, HIGHLIGHTORANGE, rect, 5)
    g.display.update()

def highlight_circle(rect:Rect):
    g.draw.circle(win, HIGHLIGHTORANGE, rect.center, RADIUS_RESOURCES, 5)
    g.display.update()

def draw():

    win.fill(DARKYELLOW)

    #draw Title
    text = TITLE_FONT.render("Splendor", 1, BLUE)
    win.blit(text, (int(WIDTH/2 - text.get_width()/2), 20))

    #draw Buttons
    help_button.draw(win)
    exit_button.draw(win)

    #Draw board
    #-------------------------------
    #draw carddeck
    for card_ind in lst_cards:
        card_ind.draw(win)

    # draw bonus cards (available)
    for bc in lst_bcards:
        bc.draw(win)

    # draw ressource stack
    ressource_stack.draw(win, LETTER_FONT, x=START_X_RS , y=START_Y_RS, r=RADIUS_RESOURCES, padding=PADDING_H)

    #draw active player
    active_player.draw_name_points(win, LETTER_FONT, START_X_PLAYER, START_Y_PLAYER, (RECTWIDTH_CARDDECK + PADDING_H)*4)
    active_player.draw_crds_count(win, LETTER_FONT, START_X_PLAYER, START_Y_PLAYER_CARDS, RECTSQUARE_PLAYER_CARDS, PADDING_H)
    active_player.draw_Resources_stack(win, LETTER_FONT, START_X_PLAYER_RS, START_Y_PLAYER_RS, int(RECTSQUARE_PLAYER_CARDS/2), PADDING_H)

    g.display.update()

#setup game loop
FPS = 60
clock = g.time.Clock()

#setting up start menu:
start_b = Button(LETTER_FONT, WIDTH / 2, HEIGHT / 2 - 300, BUTTON_WIDTH, 50, "START")
exit_b = Button(LETTER_FONT, WIDTH / 2, HEIGHT / 2 + 200, BUTTON_WIDTH, 50, text="END")
number_player_b = Button(LETTER_FONT, WIDTH / 2 - 70, HEIGHT / 2 - 200, 50, 50, "4")
name_player1 = InputBox(WIDTH / 2 , 0, BUTTON_WIDTH, 50, LETTER_FONT, "Player1")
name_player2 = InputBox(WIDTH / 2 , 0, BUTTON_WIDTH, 50, LETTER_FONT, text="Player2")
name_player3 = InputBox(WIDTH / 2 , 0, BUTTON_WIDTH, 50, LETTER_FONT, text="Player3")
name_player4 = InputBox(WIDTH / 2 , 0, BUTTON_WIDTH, 50, LETTER_FONT, text="Player4")
input_name_boxes = [name_player1, name_player2, name_player3, name_player4]
y = -200
for input_box in input_name_boxes:
    input_box.rect.move_ip(0, int(HEIGHT/2)+ y)
    y += 100

#initiate the 12 cards of the carddeck.
lst_cards = []
for difficulty_level in range(3):
    y = 100 + difficulty_level*(PADDING_V + RECTHEIGHT_CARDDECK) # determining the y coordinate
    for __ in range(4):   #instance the 4 card
        x = START_X_CARDS + __*(PADDING_H + RECTWIDTH_CARDDECK)# determining the x coordinate
        c = Card(difficulty_level, x, y, RECTWIDTH_CARDDECK, RECTHEIGHT_CARDDECK, LETTER_FONT)
        lst_cards.append(c)

#initiate the 3 bonus cards.
lst_bcards = []
for _ in range(3):
    y = 100 + _ * (RECTHEIGHTBONI + PADDING_V)
    x = START_X_BONI
    bonus = BonusC(x, y, RECTWIDTHBONI, RECTHEIGHTBONI, LETTER_FONT)
    lst_bcards.append(bonus)

#game counter, to track actions done by active player.
cntr_pck_crd = 0
cntr_pck_res_as_dict = Resources()

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
        if event.type == QUIT:
            run = in_menu = False
        for box in input_name_boxes:
            box.handle_event(event)
            number_player_b.active = False
        if start_b.handle_event(event):
            number_player_b.active = False
            for box in input_name_boxes:
                if box.visible:
                    lst_player_names.append(box.text)
            if len(lst_player_names) >= 1:
                in_menu = False
        if exit_b.handle_event(event):
            run = in_menu = False
            number_player_b.active = False
        if number_player_b.handle_event(event):
            i = number_player_b.increase_num(4)
            for box in input_name_boxes[:i]:
                box.visible = True
            for box in input_name_boxes[i:]:
                box.visible = False
#in-gamebuttons
help_button = Button(LETTER_FONT, WIDTH - 2*INGAME_BUTTON, 20, INGAME_BUTTON, LETTER_FONT.get_height() + 15, "Help")
help_button.colour = BLACK

exit_button = Button(LETTER_FONT, WIDTH - 4*INGAME_BUTTON + PADDING_H, 20, INGAME_BUTTON, LETTER_FONT.get_height() + 15  , "Exit")
exit_button.colour = BLACK

#Players and active_player / id:
lst_player = []
for player in lst_player_names:
    lst_player.append(Player(str(player), 1))
active_player_id = 0

ressource_stack = Resourcestack(len(lst_player))

#game_loop
while run:
    clock.tick(FPS)

    active_player = lst_player[active_player_id]

    draw()

    for event in g.event.get():
        if event.type == QUIT:
            run = False
        if event.type == MOUSEBUTTONDOWN:
            #TODO player clicks help button:
            if help_button.handle_event(event):
                pass
            #player clicks exit button:
            if exit_button.handle_event(event):
                run = False
            #player clicks on card
            for card_id, card in enumerate(lst_cards):
                if card.handle_event(event):
                    highlight_rect(card.rect)
                    if 1 in cntr_pck_res_as_dict.values():
                        display_game_notification("That won't work!", "You took already a ressource.")
                        continue #without this continue, the algorithm doesn't work as expected.
                    else:
                        if active_player.check_if_card_affordable(card):
                            active_player.pick_crd(card, ressource_stack)
                            cntr_pck_crd += 1
                            if card.points > 0:
                                display_game_notification(f"{card.points} points are added to your points!")
                            card.replace_card(card_id, lst_cards)
                        else:
                            display_game_notification("Not enough Resources")
                    for bcard in lst_bcards:
                        if active_player.check_if_qualified_for_bonus(bcard):
                            active_player.points += 3
                            bcard.visible = False
                            lst_bcards.remove(bcard)
                            display_game_notification("Awesome!!! You just earned a bonus", f"{bonus.points} are added to your points.")
                            break
            #player klicks on Resources
            for ress, ressource_rect in ressource_stack.lst_rects:
                if event.type == MOUSEBUTTONDOWN:
                    if ressource_rect.collidepoint(event.pos):
                        highlight_circle(ressource_rect)
                        if cntr_pck_res_as_dict[ress] == 0 or sum(cntr_pck_res_as_dict.values()) - cntr_pck_res_as_dict[ress] == 0:
                            success = active_player.take_res(ress, ressource_stack)
                            if success:
                                display_game_notification(f"1 of the {ress} Resources added to your stack")
                                cntr_pck_res_as_dict[ress] += 1
                                break
                            else:
                                display_game_notification("You can't take this, sweetie.")
                                break
                        else:
                            display_game_notification("You can either take 2x the same, or 3 different ones!!! DUCKER!")
                            break

    draw()

    g.time.wait(200)

    if active_player_id == 0:
        for player in lst_player:
            if player.points >= 15:
                run = False
                display_message(f"Gratulations!!!\n {active_player.name}",
                "You won! Well done. You're amazing and sexy!!!")
                g.quit()

    if cntr_pck_crd == 1 or 2 in cntr_pck_res_as_dict.values() or sum(cntr_pck_res_as_dict.values()) >= 3:
        if active_player_id < len(lst_player) - 1 :
            active_player_id += 1
            cntr_pck_res_as_dict = Resources()
            cntr_pck_crd = 0
        else:
            active_player_id = 0
            cntr_pck_res_as_dict = Resources()
            cntr_pck_crd = 0
        display_game_notification(f"It's {lst_player[active_player_id].name}'s turn :)")

g.display.quit()
g.quit()
sys.exit()
