from classes import Card, OpenBoard, BonusC, BonusBoard, RessourceStack, Player
import pygame as g

#defining all known funcs, needed for the game not implemented in classes:
#check func -> already implented in player class.

#check points -> if >=15 game ends,playyer wins

#check if a player fulfills the pattern to receive a bonus card:
#after each turn. check for all bonuscards

#count game_stats like nb of turns and print points of all players

#copying the code from hangman game - to be adapted but for a first intuition

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
    #draw active player's stack (cards, points, ress)
    #win.blit(images[hm_stat], (100, 150))
    g.display.update()

while run:

    clock.tick(FPS)

    #setup the game:
    #procedure to determine nb of players and crate the instances
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
    g.time.wait(10_000)

    for event in g.event.get():
        if event.type == g.QUIT:
            run = False
    '''    if event.type == g.MOUSEBUTTONDOWN:
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









def test():
    '''to test the functions. new tests added as functions are developed'''
    new_card = Card(2)
    print(new_card)
    new_card = Card(1)
    print(new_card)
    new_card = Card(0)
    print(new_card)
    new_game = OpenBoard()
    print(new_game)
    print(new_game.deck[-1])
    cb = new_game.replaceCard(-1)
    print(new_game.deck[-1])
    print(cb)
    #new_bonus = BonusC()
    bonus_set = BonusBoard()
    print(bonus_set.deck[0])
    crd = bonus_set.remove(0)
    print(crd)

def test2():
    ob = OpenBoard()
    print(ob)
    nstack = RessourceStack(2)
    print(nstack)
    np = Player("hans", 0, 1)
    print(np.name, np.state, np.green, np.cardstack)
    for _ in range(4):
        np.take_res(nstack, 2)
    np.pick_crd(ob, 11, nstack)
    #print(ob)
    print(np.cardstack[0])
    print(nstack)
    print(np.green, np.blue, np.red, np.blck)
#test2()
