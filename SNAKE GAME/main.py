import pygame
import sys
from pygame.math import Vector2
import random

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

#game constants
CELL_SIZE = 40
CELL_NUMBER = 20
SCREEN = pygame.display.set_mode((CELL_SIZE*CELL_NUMBER, CELL_NUMBER*CELL_SIZE))
CLOCK = pygame.time.Clock()
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)
APPLE = pygame.image.load('gallery/apple.png').convert_alpha()
GAME_FONT = pygame.font.Font('freesansbold.ttf', 25)


class Main:

    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()


    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()


    def draw_elements(self):
        self.draw_grass()
        self.draw_score()
        self.fruit.draw_fruit()
        self.snake.draw_snake()


    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.snake.play_crunch_sound()
            self.fruit.randomize()
            self.snake.add_block()

        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()


    def check_fail(self):
        if not 0 <= self.snake.body[0].x < CELL_NUMBER:
            self.gameOver()

        elif not 0 <= self.snake.body[0].y < CELL_NUMBER:
            self.gameOver()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.gameOver()


    def gameOver(self):
        self.snake.reset()


    def draw_grass(self):
        grass_color = (108, 245, 98)
        for row in range(CELL_NUMBER):
            if row%2 == 0:
                for col in range(CELL_NUMBER):
                    if col%2 == 0:
                        grass_rect = pygame.Rect(col * CELL_SIZE,row * CELL_SIZE,CELL_SIZE, CELL_SIZE)
                        pygame.draw.rect(SCREEN,grass_color, grass_rect)

            else:
                for col in range(CELL_NUMBER):
                    if col%2 != 0:
                        grass_rect = pygame.Rect(col * CELL_SIZE,row * CELL_SIZE,CELL_SIZE, CELL_SIZE)
                        pygame.draw.rect(SCREEN,grass_color, grass_rect)


    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = GAME_FONT.render(score_text, True, (0,0,0))
        score_X = int(CELL_SIZE * CELL_NUMBER - 60)
        score_Y = int(CELL_SIZE * CELL_NUMBER - 40)
        score_rect = score_surface.get_rect(center = (score_X,score_Y))
        apple_rect = APPLE.get_rect(midright = (score_rect.left, score_rect.centery))
        br_rect = pygame.Rect(apple_rect.left, apple_rect.top, apple_rect.width + score_rect.width + 8,apple_rect.height)

        pygame.draw.rect(SCREEN, (167, 209, 61), br_rect)

        SCREEN.blit(score_surface,score_rect)
        SCREEN.blit(APPLE, apple_rect)



class SNAKE:

    def __init__(self):
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)] #starting position of the player
        self.direction = Vector2(1,0)
        self.new_block = False

        #loading the snake images
        self.head_up = pygame.image.load('gallery/snake/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('gallery/snake/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('gallery/snake/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('gallery/snake/head_left.png').convert_alpha()

        self.tail_up = pygame.image.load('gallery/snake/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('gallery/snake/tail_down.png').convert_alpha()
        self.tail_left = pygame.image.load('gallery/snake/tail_left.png').convert_alpha()
        self.tail_right = pygame.image.load('gallery/snake/tail_right.png').convert_alpha()

        self.body_vertical = pygame.image.load('gallery/snake/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('gallery/snake/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('gallery/snake/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('gallery/snake/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('gallery/snake/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('gallery/snake/body_bl.png').convert_alpha()

        self.crunch_sound = pygame.mixer.Sound('gallery/sounds/crunch.wav')
        self.crash_sound = pygame.mixer.Sound('gallery/sounds/crash.mp3')


    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index,block in enumerate(self.body):
            x_pos = int(block.x * CELL_SIZE)
            y_pos = int(block.y * CELL_SIZE)
            block_rect = pygame.Rect(x_pos, y_pos, CELL_SIZE, CELL_SIZE)

            if index == 0:
                SCREEN.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                SCREEN.blit(self.tail, block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    SCREEN.blit(self.body_vertical, block_rect)

                elif previous_block.y == next_block.y:
                    SCREEN.blit(self.body_horizontal, block_rect)

                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        SCREEN.blit(self.body_tl, block_rect)

                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1 :
                        SCREEN.blit(self.body_bl, block_rect)

                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1 :
                        SCREEN.blit(self.body_tr, block_rect)

                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1 :
                        SCREEN.blit(self.body_br, block_rect)


    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]

        if head_relation == Vector2(1,0):
            self.head = self.head_left

        elif head_relation == Vector2(-1,0):
            self.head = self.head_right

        elif head_relation == Vector2(0,1):
            self.head = self.head_up

        elif head_relation == Vector2(0,-1):
            self.head = self.head_down


    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]

        if tail_relation == Vector2(1,0):
            self.tail = self.tail_left

        elif tail_relation == Vector2(-1,0):
            self.tail = self.tail_right

        elif tail_relation == Vector2(0,1):
            self.tail = self.tail_up

        elif tail_relation == Vector2(0,-1):
            self.tail = self.tail_down


    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]


    def add_block(self):
        self.new_block = True


    def play_crunch_sound(self):
        self.crunch_sound.play()


    def play_crash_sound(self):
        self.crash_sound.play()


    def reset(self):
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]
        self.direction = Vector2(0,0)


class FRUIT:

    def __init__(self):
        #creating x and y position by drawing a square
        self.randomize()


    def draw_fruit(self):
        #creating a rectangle to place the fruit
        FruitXPos = int(CELL_SIZE*self.pos.x)
        FruitYPos = int(CELL_SIZE*self.pos.y)
        Fruit_rect = pygame.Rect(FruitXPos,FruitYPos, CELL_SIZE, CELL_SIZE)
        SCREEN.blit(APPLE,Fruit_rect)


    def randomize(self):
        self.x = random.randint(0, CELL_NUMBER - 1)
        self.y = random.randint(0, CELL_NUMBER - 1)
        self.pos = Vector2(self.x, self.y)


main_game = Main()

#game loop
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

        elif event.type == SCREEN_UPDATE:
            main_game.update()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0,-1)

            elif event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0,1)

            elif event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1,0)

            elif event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1,0)


    SCREEN.fill((108, 250, 0))
    main_game.draw_elements()
    pygame.display.update()
    CLOCK.tick(60)


