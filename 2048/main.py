import pygame
import sys
import random


pygame.init()

#Intitial setups
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 500
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption('2048 GAME')

ICON = pygame.image.load('gallery/logo-icon.jpeg')
pygame.display.set_icon(ICON)

timer = pygame.time.Clock()
FPS = 60

FONT = pygame.font.Font('freesansbold.ttf', 24)

# 2048 game color library
COLORS = {
    0:(204,192,179),
    2:(238,228,218),
    4:(237,224,200),
    8:(242,177,121),
    16:(245,149,99),
    32:(246,124,95),
    64:(246,94,59),
    128:(237,207,114),
    256:(237,204,97),
    512:(237,200,80),
    1024:(237,197,63),
    2048:(237,194,46),
    'light text':(249,246,242),
    'dark text':(119,110,101),
    'other':(0,0,0),
    'bg':(187,173,160)
}

#game variables initialization
BOARD_VALUES = [[0 for _ in range(4)] for _ in range(4)]
game_over = False
spawn_new = True
init_count = 0
direction = ''
score = 0
#high score
file = open('high_score', 'r')
init_high = int(file.readline())
file.close()
high_score = init_high


#game functions
def draw_board():
    pygame.draw.rect(SCREEN, COLORS['bg'], [0,0,400,400],0, 10)
    score_text = FONT.render(f'Score :{score}', True, 'black')
    high_score_text = FONT.render(f'High Score :{high_score}', True, 'black')
    SCREEN.blit(score_text, (10, 410))
    SCREEN.blit(high_score_text, (10, 450))



def draw_pieces(board):
    for i in range(4):
        for j in range(4):
            value = board[i][j]
            if value > 8:
                value_color = COLORS['light text']

            else:
                value_color = COLORS['dark text']

            if value <= 2048:
                color = COLORS[value]

            else:
                color = COLORS['other']

            pygame.draw.rect(SCREEN, color , [j * 95 + 20, i * 95 + 20, 75, 75], 0 ,5)

            if value > 0:
                value_len = len(str(value))
                FONT = pygame.font.Font('freesansbold.ttf', 48 - (5 * value_len))
                value_text = FONT.render(str(value), True, value_color)
                text_rect = value_text.get_rect(center = ( j * 95 + 57, i * 95 + 57))
                SCREEN.blit(value_text, text_rect)


def new_pieces(borad):

    count = 0
    full = False

    while any(0 in row for row in borad) and count < 1:
        row = random.randint(0,3)
        col = random.randint(0,3)

        if borad[row][col] == 0:
            count += 1
            if random.randint( 1,10) == 10:
                borad[row][col] = 4

            else:
                borad[row][col] = 2

    if count < 1:
        full = True

    return borad, full


def take_turn(direc, board):

    global score
    merged = [[False for _ in range(4)] for _ in range(4)]

    if direc == 'UP':
        for i in range(4):
            for j in range(4):
                shift = 0
                if i > 0 :
                    for q in range(i):
                        if board[q][j] == 0:
                            shift += 1

                    if shift > 0:
                        board[i - shift][j] = board[i][j]
                        board[i][j] = 0

                    if board[i - shift - 1][j] == board[i - shift][j] and not merged[i - shift - 1][j] and not merged[i - shift][j]:
                        board[i - shift - 1][j] *= 2
                        score += board[i - shift - 1][j]
                        board[i-shift][j] = 0
                        merged[i - shift - 1][j] = True




    elif direc == 'DOWN':
        for i in range(3):
            for j in range(3):
                shift = 0
                for q in range(i + 1):
                    if board[3-q][j] == 0:
                        shift += 1

                if shift > 0:
                    board[2 - i +shift][j] = board[2 - i][j]
                    board[2 - i][j] = 0

                if 3 - i + shift <= 3:
                    if board[2 - i + shift ][j] == board[3 -i + shift][j] and not merged[3 - i +shift ][j] and not merged[2 - i +shift][j]:
                        board[3 - i + shift][j] *= 2
                        score += board[3 - i + shift][j]
                        board[2-i+shift][j] = 0
                        merged[3 - i + shift ][j] = True






    elif direc == 'LEFT' :
        for i in range(4):
            for j in range(4):
                shift = 0
                for q in range(j):
                    if board[i][q] == 0:
                        shift += 1

                if shift > 0:
                    board[i][j - shift] = board[i][j]
                    board[i][j] = 0

                if board[i][j - shift] == board[i][j - shift - 1] and not merged[i][j - shift - 1] and not merged[i][j - shift]:
                    board[i][j - shift - 1] *= 2
                    score += board[i][j - shift - 1]
                    board[i][j - shift] = 0
                    merged[i][j - shift - 1] = True





    elif direc == 'RIGHT':
        for i in range(4):
            for j in range(4):
                shift = 0
                for q in range(j):
                    if board[i][3 - q] == 0:
                        shift += 1

                if shift > 0:
                    board[i][3 - j + shift] = board[i][3 - j]
                    board[i][3 - j] = 0

                if 4 - j + shift <= 3:
                    if board[i][4 - j +shift] == board[i][3 - j + shift] and not merged[i][4 - j + shift] and not merged[i][3 - j + shift] :
                        board[i][4 - j + shift] *= 2
                        score += board[i][4 - j + shift]
                        board[i][3 - j + shift] = 0
                        merged[i][4 - j + shift ] = True

    return board

def draw_over():
    pygame.draw.rect(SCREEN,'black',[50,50,300,100], 0 ,10)
    game_over_text1 = FONT.render('Game over!', True, 'white')
    game_over_text2 = FONT.render('Press Enter to Restart', True, 'white')
    SCREEN.blit(game_over_text1, (130, 65))
    SCREEN.blit(game_over_text2, (70, 105))


#Main Game Loop
Running = True

while Running:
    timer.tick(FPS)

    SCREEN.fill('gray')

    draw_board()
    draw_pieces(BOARD_VALUES)

    if spawn_new or init_count < 2:
        BOARD_VALUES, game_over = new_pieces(BOARD_VALUES)
        spawn_new = False
        init_count += 1

    if direction != ' ':
        BOARD_VALUES = take_turn(direction, BOARD_VALUES)
        direction = ' '
        spawn_new = True

    if game_over:
        draw_over()
        if high_score > init_high :
            file  = open('high_score', 'w')
            file.write(f'{high_score}')
            file.close()
            init_high = high_score

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                direction = 'UP'

            elif event.key == pygame.K_DOWN :
                direction = 'DOWN'

            elif event.key == pygame.K_RIGHT :
                direction = 'RIGHT'

            elif event.key == pygame.K_LEFT :
                direction = 'LEFT'

            if game_over:
                if event.key == pygame.K_RETURN:
                    BOARD_VALUES = [[0 for _ in range(4)] for _ in range(4)]
                    spawn_new = True
                    init_count = 0
                    score = 0
                    direction = ' '
                    game_over = False


        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()


    if score > high_score:
        high_score = score


    pygame.display.update()

