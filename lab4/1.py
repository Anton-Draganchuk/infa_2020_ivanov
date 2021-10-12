import pygame
from pygame.draw import *
from random import randint
import math
pygame.init()

FPS = 1
screen = pygame.display.set_mode((1200, 800))

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]


def new_ball():
    """
    Создает новый шарик в случайном месте
    :return: Шарик случайного размера и цвета
    """
    global x, y, r
    x = randint(100, 1100)
    y = randint(100, 800)
    r = randint(10, 100)
    color = COLORS[randint(0, 5)]
    circle(screen, color, (x, y), r)


def hit(event):
    """
    Проверяет попали ли мы по шарику или нет
    :param event: Событие которое мы сделали
    :return: true or folse
    """
    dx = event.pos[0] - x
    dy = event.pos[1] - y
    dist = (dx**2 + dy**2)**(1 / 2)
    if dist <= r:
        return True
    else:
        return False


pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if hit(event):
                print('Hit')
            else:
                print('Click!')
    new_ball()
    pygame.display.update()
    screen.fill(BLACK)


pygame.quit()

