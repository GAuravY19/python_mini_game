import pygame
import sys
import random
import time

pygame.init()

#game constants
SCREEN_WIDTH = 400
SCREEN_HEIGTH = 700
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGTH))
pygame.display.set_caption("Road Rush Game")
ICON = pygame.image.load('gallery/icon/motorbike.png')
pygame.display.set_icon(ICON)

ROAD = pygame.image.load('gallery/road/road.jpg')

GAME_FONT = pygame.font.Font('freesansbold.ttf', 25)

clock = pygame.time.Clock()

FPS = 60

class Main:

    def __init__(self):
        self.rides = Rider()
        self.cars = EnemyCars()

        self.start_screen = pygame.image.load('gallery/icon/logo.jpg')
        self.gameOver_screen = pygame.image.load('gallery/icon/game-over.png')

        self.score = 0
        self.high_score = 0

    def update(self):
        self.cars.movecars()

    def draw_elements(self):
        self.rides.Riderrect()
        self.cars.CarsRect()

    def gameOver(self):
        #show game over screen
        if self.score > self.high_score:
            self.high_score = self.score
            fileopen = open('highscore.txt', 'w')
            fileopen.write(f'{self.high_score}')
            fileopen.close
        pygame.quit()
        sys.exit()

    def collision(self, dist):
        if dist == self.rides.Riderx:
            self.gameOver()

    def movecars(self, move):
        if move == "left":
            self.rides.Riderx -= 130

        elif move == 'right':
            self.rides.Riderx += 130

    def Score(self,position):
        if int(position) - self.rides.Riderx <= -20:
            self.score += 1

        return self.score

    def show_score(self):
        score_surface = GAME_FONT.render("Score :- " + str(self.score), True, (255,255,255))
        score_rect = score_surface.get_rect(topleft = (20,10))
        SCREEN.blit(score_surface, score_rect)

    def High_score(self):
        fileopen = open('highscore.txt', 'r')
        int_high = (fileopen.readlines())
        fileopen.close()
        self.high_score = int_high

        return self.high_score

    def show_high_score(self):
        high_score_surface = GAME_FONT.render("High Score : " + str(self.high_score), True, (255,255,240))
        high_score_surface_rect = high_score_surface.get_rect(bottomright = (390,690))
        SCREEN.blit(high_score_surface, high_score_surface_rect)

class Rider:

    def __init__(self):
        self.rider = pygame.image.load('gallery/cars/rider.png')
        self.Riderx = 270
        self.Ridery = 40

    def Riderrect(self):
        riderrect = self.rider.get_rect(topleft = (self.Riderx, self.Ridery))
        SCREEN.blit(self.rider, riderrect )


class EnemyCars:

    def __init__(self):
        self.car1 = pygame.image.load('gallery/cars/car1.png')
        self.car2 = pygame.image.load('gallery/cars/car2.png')
        self.car3 = pygame.image.load('gallery/cars/car3.png')

        self.x1 = 300
        self.y1 = 800

        self.x2 = 220
        self.y2 = 800

        self.x3 = 50
        self.y3 = 800

    def movecars(self):
        self.y1 = self.y1 - 0.25
        self.y2 = self.y2 - 0.2
        self.y3 = self.y3 - 0.4
        main.collision(self.y1)
        main.collision(self.y2)
        main.collision(self.y3)
        main.Score(self.y1)
        main.Score(self.y2)
        main.Score(self.y3)
        return self.y1,self.y2,self.y3

    def CarsRect(self):
        #getting the rectangles of the cars
        self.movecars()

        if self.y1 <= 0:
            self.y1 = 800

        if self.y2 <= 0:
            self.y2 = 800

        if self.y3 <= 0:
            self.y3 = 800

        carRect1 = self.car1.get_rect(bottomleft = (self.x1, self.y1))
        carRect2 = self.car1.get_rect(bottomright = (self.x2, self.y2))
        carRect3 = self.car1.get_rect(midbottom = (self.x3, self.y3))

        #bliting of the cars
        SCREEN.blit(self.car1, carRect1)
        SCREEN.blit(self.car2, carRect2)
        SCREEN.blit(self.car3, carRect3)

main = Main()


#game loop
running = True

while running:

    main.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()

            elif event.key == pygame.K_LEFT:
                main.movecars('left')

            elif event.key == pygame.K_RIGHT:
                main.movecars('right')


    #screen drawing
    SCREEN.fill((130, 168, 160))
    SCREEN.blit(ROAD,(0,0))
    main.show_score()
    main.show_high_score()
    main.draw_elements()
    pygame.display.update()
