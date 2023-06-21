import pygame
import sys
import random
import math
from pygame import mixer

#Initializing the pygame
pygame.init()

#game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BACKGROUND = pygame.image.load('gallery/background.png')
SCORE = 0
FONT = pygame.font.Font('freesansbold.ttf', 32)
SCORE_X = 10
SCORE_Y = 10
BULLET_SOUND = mixer.Sound('sounds/laser.wav')
GAME_OVER_FONT = pygame.font.Font('freesansbold.ttf', 64)


#screen creation
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


#screen title and icon
pygame.display.set_caption('Space Invaders')
Icon = pygame.image.load('gallery/spaceship/spaceship.png')
pygame.display.set_icon(Icon)

#playerImage
playerImage = pygame.image.load('gallery/spaceship/invaders.png')
playerImgx = 370
playerImgy = 420
playerImgx_Change = 0


#Enemy Image
enemy_Img = []
enemyImgx = []
enemyImgy = []
enemyImgx_Change = []
enemyImgy_Change = []
num_of_enemy = 5
for i in range(num_of_enemy):
    enemy_Img.append( pygame.image.load(f'gallery/Enemy/enemy{i}.png'))
    enemyImgx.append( random.randint(0,736))
    enemyImgy.append( random.randint(20,200))
    enemyImgx_Change.append(2)
    enemyImgy_Change.append(20)

# background sounds
mixer.music.load('sounds/background.wav')
mixer.music.play(-1)

#bullets Image
BULLETS = pygame.image.load('gallery/bullet.png')
bulletx = 0
bullety = 420
bullety_Change = 5
bullet_state = 'ready' #in ready state the bullet can't be seen


#game functions
def PlayerImg(x,y):
    SCREEN.blit(playerImage, (x,y))

def EnemyImg(x , y, i):
    SCREEN.blit(enemy_Img[i], (x,y))

def FireBullet(x,y):
    global bullet_state
    bullet_state = 'fire' #in fire state the bullet is been fired
    SCREEN.blit(BULLETS, ( x+16, y+10 ))

def isCollide(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX-bulletX,2)) + (math.pow(enemyY-bulletY,2) )
    if distance < 27:
        return True
    else:
        return False

def show_score(x,y):
    score = FONT.render('Score : '+ str(SCORE), False, (255,255,255))
    SCREEN.blit(score, (x, y))


def gameOverText():
    over_text = GAME_OVER_FONT.render('GAME OVER', True, (255,255,255))
    SCREEN.blit(over_text, (200, 250))

#game loop
running = True

while running:
    SCREEN.fill((0,0,0))
    SCREEN.blit(BACKGROUND,(0,0))

    for event in pygame.event.get():
        # player movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerImgx_Change = -4

            elif event.key == pygame.K_RIGHT:
                playerImgx_Change = 4

            elif event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    bulletx = playerImgx
                    FireBullet(bulletx, bullety)


            elif event.key == pygame.K_ESCAPE:
                running == False
                pygame.quit()
                sys.exit()

        if event.type == pygame.QUIT:
            running = False


    # bullet movement
    if bullety <= 0:
        bullety = 420
        bullet_state = 'ready'

    if bullet_state == 'fire':
        FireBullet(bulletx, bullety)
        bullety -= bullety_Change
        BULLET_SOUND.play()



    #setting boundary for the spaceship
    playerImgx += playerImgx_Change
    if playerImgx <= 0:
        playerImgx = 0

    elif playerImgx >= 736:
        playerImgx = 736


    #setting boundary for the enemy
    for j in range(num_of_enemy):

        #game over
        if enemyImgy[j] > 360:
            for k in range(num_of_enemy):
                enemyImgy[j] = 2000

            gameOverText()
            break

        enemyImgx[j] += enemyImgx_Change[j]
        if enemyImgx[j] <= 0 :
            enemyImgx_Change[j] = 2
            enemyImgy[j] += enemyImgy_Change[j]

        elif enemyImgx[j] >= 736:
            enemyImgx_Change[j] = -2
            enemyImgy[j] += enemyImgy_Change[j]

        #setting collision conditions
        collision = isCollide(enemyImgx[j], enemyImgy[j], bulletx, bullety)
        if collision == True:
            COLLISION_SOUND = mixer.Sound('sounds/explosion.wav')
            COLLISION_SOUND.play()
            bullety = 420
            bullet_state = 'ready'
            SCORE += 1
            enemyImgx[j] = random.randint(0,736)
            enemyImgy[j] = random.randint(20,200)

        EnemyImg(enemyImgx[j], enemyImgy[j], j)


    PlayerImg(playerImgx, playerImgy)
    show_score(SCORE_X, SCORE_Y)
    pygame.display.update()


