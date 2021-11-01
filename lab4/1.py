import pygame
from pygame.draw import *
from random import randint
import math
from Config import *
from Ball import *
from Interface import *
pygame.init()

FPS = 120
screen = pygame.display.set_mode((1080, 720))

screen.fill(White)


for i in range(0, Ball_number):
    new_ball()


pygame.display.update()
clock = pygame.time.Clock()
start = True
finished = False


while not finished:
    clock.tick(FPS)
    while start:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                start = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == 27):
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            Score += hit(event)
            if exit(event):
                finished = True
    screen.fill(White)
    movement()
    collision()
    exit_buttom()
    counter(event, Score)
    pygame.display.update()


pygame.quit()

