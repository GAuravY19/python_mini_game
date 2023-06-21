import pygame
import random
import sys
from pygame.locals import *


#GAME CONSTANTS
FPS = 32
SCREEN_WIDTH = 289
SCREEN_HEIGHT = 511
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
GROUNDY = SCREEN_HEIGHT * 0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = 'gallery/sprites/bird.png'
BACKGROUND = 'gallery/sprites/background.png'
PIPE = 'gallery/sprites/pipe.png'



#GAME FUNCTIONS
def isCollide(playerx, playery, UpperPipes, LowerPipes):
    if playery > GROUNDY - 25 or playery < 0 :
        GAME_SOUNDS['hit'].play()
        return True

    for pipe in UpperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if (playery < pipeHeight + pipe['y'] and (abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width())):
            GAME_SOUNDS['hit'].play()
            return True

    for pipe in LowerPipes:
        if (playery + GAME_SPRITES['player'].get_height() > pipe['y'] ) and (abs(playerx - pipe['x'])
                                                                             < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True

    return False



def welcomeScreen():

    playerx = int(SCREEN_WIDTH/5)
    playery = int(SCREEN_HEIGHT - GAME_SPRITES['player'].get_height())/2

    messagex = int(SCREEN_WIDTH - GAME_SPRITES['message'].get_width())/2
    messagey = int(SCREEN_HEIGHT*0.13)

    basex = 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return

            else:
                SCREEN.blit(GAME_SPRITES['background'], (0,0)),
                SCREEN.blit(GAME_SPRITES['player'], (playerx, playery)),
                SCREEN.blit(GAME_SPRITES['message'], (messagex, messagey)),
                SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY)),
                pygame.display.update()
                FPSCLOCK.tick(FPS)


def getRandomPipe():

    pipeHeight = GAME_SPRITES['pipe'][0].get_height()

    offset = SCREEN_HEIGHT / 3

    y2 = offset + random.randrange(0, int(SCREEN_HEIGHT - GAME_SPRITES['base'].get_height() - 1.2*offset))

    pipeX = SCREEN_WIDTH + 10
    y1 = pipeHeight - y2 + offset

    pipe = [
        {'x':pipeX, 'y':-y1}, #upperpipe
        {'x':pipeX, 'y':y2 }  #lowerpipe
    ]

    return pipe


def mainGame():

    score = 0

    playerx = int(SCREEN_WIDTH/5)
    playery = int(SCREEN_WIDTH/2)

    basex = 0

    #2 random pipes creation
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    UpperPipes = [
        {'x':SCREEN_WIDTH + 200 ,'y':newPipe1[0]['y']},
        {'x':SCREEN_WIDTH + 200 + (SCREEN_WIDTH/2) ,'y':newPipe2[0]['y']}
    ]

    LowerPipes =  [
        {'x':SCREEN_WIDTH + 200 ,'y':newPipe1[1]['y']},
        {'x':SCREEN_WIDTH + 200 + (SCREEN_WIDTH/2) ,'y':newPipe2[1]['y']}
    ]

    pipevelx = -4

    playervely = -9
    playermaxvely = 10
    playeraccy = 1

    playerflapaccv = -8 #velocity while flapping
    playerflapped = False #True while the bird is flapping

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playervely = playerflapaccv
                    playerflapped = True
                    GAME_SOUNDS['wing'].play()

        #checking the crashtest
        CrashTest = isCollide(playerx, playery, UpperPipes, LowerPipes)
        if CrashTest:
            return


        #checking the score
        playerMid = playerx + (GAME_SPRITES['player'].get_width())/2
        for pipe in UpperPipes:
            pipeMidpos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidpos <= playerMid < pipeMidpos + 4:
                score += 1
                print(f"Your Score is {score}")
                GAME_SOUNDS['point'].play()

        if playervely < playermaxvely and not playerflapped:
            playervely += playeraccy

        if playerflapped:
            playerflapped = False
        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playervely, GROUNDY - playery - playerHeight)

        #moving pipe in left direction
        for upperpipe, lowerpipe in zip(UpperPipes, LowerPipes):
            upperpipe['x'] += pipevelx
            lowerpipe['x'] += pipevelx

        #adding the pipes in the screen
        if 0 < UpperPipes[0]['x'] < 5:
            newpipe = getRandomPipe()
            UpperPipes.append(newpipe[0])
            LowerPipes.append(newpipe[1])

        #removing the pipe if the pipe goes out of the screen
        if UpperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            UpperPipes.pop(0)
            LowerPipes.pop(0)

        SCREEN.blit(GAME_SPRITES['background'], (0,0))

        for upperpipe, lowerpipe in zip(UpperPipes, LowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperpipe['x'], upperpipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerpipe['x'], lowerpipe['y']))

        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))

        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()

        xoffset = (SCREEN_WIDTH - width)/2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (xoffset, SCREEN_HEIGHT*0.12))
            xoffset += GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)





if __name__ == "__main__":
    pygame.init()

    FPSCLOCK = pygame.time.Clock()

    pygame.display.set_caption('Flappy Bird')

    GAME_SPRITES['numbers'] = (
        pygame.image.load('gallery/sprites/0.png').convert_alpha(),
        pygame.image.load('gallery/sprites/1.png').convert_alpha(),
        pygame.image.load('gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('gallery/sprites/9.png').convert_alpha()
    )

    GAME_SPRITES['message'] = pygame.image.load('gallery/sprites/message.jpg').convert_alpha()

    GAME_SPRITES['base'] = pygame.image.load('gallery/sprites/base.png').convert_alpha()

    GAME_SPRITES['pipe'] = (
        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),
        pygame.image.load(PIPE).convert_alpha()
    )

    #GAME SOUNDS
    GAME_SOUNDS['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')

    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()

    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()

    while True:
        welcomeScreen()
        mainGame()




