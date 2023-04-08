#MUHAMMAD HAMZA AAMIR

import random
import sys  # We will use sys.exit to exit the program


import pygame
from pygame.locals import *  # Basic pygame imports

pygame.init()
# Txt File
file = open("High_score.txt", "r")
high_score = file.readline()
# Screen
FPS = 60
SCREENWIDTH = 430
SCREENHEIGHT = 562  # 562
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))

# Images
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)
pygame.display.set_caption('Bouncy Ghost')
ghost = pygame.image.load("ghost.png").convert_alpha()
down_ghost = pygame.transform.rotate(pygame.image.load("ghost.png").convert_alpha(), 180)
dpipe = pygame.image.load("pipe.png").convert_alpha()
upipe = pygame.transform.rotate(pygame.image.load("pipe.png").convert_alpha(), 180)
BACKGROUND = pygame.image.load("spookybg.png").convert_alpha()
SPACE = pygame.image.load("SPACE.png").convert_alpha()
hit = pygame.mixer.Sound("sfx_hit.wav")
point = pygame.mixer.Sound("sfx_point.wav")

# Pipes
eu_image = []
ed_image = []
upper_pipe_x = []
upper_pipe_y = []
down_pipe_x = []
down_pipe_y = []
pipe_x_vel = 3


def opening():
    x = 0
    y = 180
    for i in range(2000):
        screen.fill((255, 255, 255))
        screen.blit(ghost, (x, 200))
        welcome = my_font2.render("Loading ..............................", True, black)
        screen.blit(welcome, (25, 400))
        x += 0.5
        pygame.display.update()


def fall():
    global px, py, upper_pipe_y, upper_pipe_x, down_pipe_y, down_pipe_x, high_score, file
    hit.play()
    screen.blit(down_ghost, (px, py))
    screen.fill((0, 0, 0))
    screen.blit(BACKGROUND, (0, 0))
    for i in range(10000):
        screen.blit(down_ghost, (px, py))
    for i in range(1000):
        py += 0.5
        screen.blit(BACKGROUND, (0, 0))
        for i in range(4):
            screen.blit(upipe, (upper_pipe_x[i], upper_pipe_y[i]))
            screen.blit(dpipe, (down_pipe_x[i], down_pipe_y[i]))
        screen.blit(down_ghost, (px, py))
        score_text = my_font.render(str(score), True, white)
        screen.blit(score_text, (190, 60))
        high_score_text = my_font2.render("High Score: " + str(high_score), True, white)
        screen.blit(high_score_text, (0, 0))
        screen.blit(SPACE, (0, 50))

        pygame.display.update()
    file.close()
    if score >= int(high_score):
        file2 = open("High_score.txt", "w")
        high_score = score
        file2.write(str(high_score))
        file2.close()


def reset():
    global eu_image, ed_image, upper_pipe_x, upper_pipe_y, down_pipe_x, down_pipe_y, pipe_x_vel, px, py, score, p_y_vel
    score = 0
    px = 80
    py = 250
    eu_image = []
    ed_image = []
    upper_pipe_x = []
    upper_pipe_y = []
    down_pipe_x = []
    down_pipe_y = []
    pipe_x_vel = 3
    p_y_vel = -10
    for i in range(4):
        eu_image.append(upipe)
        ed_image.append(dpipe)
        upper_pipe_x.append(430 + 280 * (i))
        upper_pipe_y.append(random.random() * -250)
        down_pipe_x.append(430 + 280 * (i))
        down_pipe_y.append(upper_pipe_y[i] + 500)


def pipe_move(i):
    global upper_pipe_y, upper_pipe_x, down_pipe_y, down_pipe_y
    upper_pipe_x[i] -= pipe_x_vel
    down_pipe_x[i] -= pipe_x_vel
    screen.blit(upipe, (upper_pipe_x[i], upper_pipe_y[i]))
    screen.blit(dpipe, (down_pipe_x[i], down_pipe_y[i]))


def respawn_pipe(i):
    global upper_pipe_x, down_pipe_x
    n = i - 1
    if n < 0:
        n = 3
    upper_pipe_x[i] = upper_pipe_x[n] + 280
    down_pipe_x[i] = down_pipe_x[n] + 280
    upper_pipe_y[i] = random.random() * - 250
    down_pipe_y[i] = upper_pipe_y[i] + 500


# Game Over
collided = False


def collide(i):
    global score, my_font
    global collided, score, upper_pipe_x, px, py

    player_rect = pygame.Rect(px, py, 64, 64)
    p_score_rect = pygame.Rect(px, py, 1, 1)
    upipe_rect = pygame.Rect(upper_pipe_x[i] + 8, upper_pipe_y[i], 45, 315)
    dpipe_rect = pygame.Rect(down_pipe_x[i] + 8, down_pipe_y[i] + 7, 45, 320)
    score_rect = pygame.Rect(upper_pipe_x[i] + 5, 0, 3, 570)
    if player_rect.colliderect(upipe_rect) or player_rect.colliderect(dpipe_rect):
        collided = True
    if p_score_rect.colliderect(score_rect):
        score += 1
        point.play()


# Score
score = 0
black = (0, 0, 0)
white = (255, 255, 255)
my_font = pygame.font.Font("LeagueSpartan-Bold.otf", 50)
my_font2 = pygame.font.Font("LeagueSpartan-Bold.otf", 25)

# Player
px = 80
py = 250
p_y_vel = -10


def flap():
    global py, p_y_vel
    p_y_vel += 1


def down():
    global py
    py += p_y_vel
    screen.blit(ghost, (px, py))


def home_screen():
    reset()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    return


def mainGame():
    global p_y_vel, collided, score, high_score

    while True:
        screen.blit(BACKGROUND, (0, 0))
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_SPACE:
                p_y_vel = -12

        flap()
        down()

        for i in range(4):
            pipe_move(i)
            if upper_pipe_x[i] <= -54:
                respawn_pipe(i)
            collide(i)
        score_text = my_font.render(str(score), True, white)
        screen.blit(score_text, (190, 60))
        high_score_text = my_font2.render("High Score: " + str(high_score), True, white)
        screen.blit(high_score_text, (0, 0))
        if score > int(high_score):
            high_score = score
        if py <= 0 or py >= 510:
            collided = True
        if collided:
            collided = False
            fall()
            return
        pygame.display.update()
        FPSCLOCK.tick(FPS)


if __name__ == "__main__":
    pygame.init()  # Initialize all pygame's modules
    FPSCLOCK = pygame.time.Clock()
    opening()
    screen.blit(BACKGROUND, (0, 0))
    screen.blit(ghost, (px, py))
    screen.blit(SPACE, (0, 0))
    pygame.display.update()

    reset()
    while True:
        home_screen()
        mainGame()
