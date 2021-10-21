import pygame
from pygame.draw import *
from random import randint
import math
from Config import *
pygame.init()

FPS = 60
screen = pygame.display.set_mode((1080, 720))

# i[0] координата x
# i[1] координата y
# i[2] радиус
# i[3] скорость x
# i[4] скорость y
# i[5] цвет


def new_ball():
    """
    Создает новый шарик в случайном месте
    :return: Шарик случайного размера и цвета
    """
    global coordinate
    r = randint(10, 100)
    x = randint(r, 1080 - r)
    y = randint(r, 720 - r)
    vx = randint(-5, 5)
    vy = randint(-5, 5)
    color = COLORS[randint(0, 5)]
    coordinate.append([x, y, r, vx, vy, color])
    circle(screen, color, (x, y), r)


def hit(event):
    """
    Проверяет попали ли мы по шарику или нет
    :param event: Событие которое мы сделали
    :return: true or false
    """
    mouse_x = event.pos[0]
    mouse_y = event.pos[1]
    for i in coordinate:
        dx = mouse_x - i[0]
        dy = mouse_y - i[1]
        dist = (dx**2 + dy**2)**(1 / 2)
        if dist <= i[2]:
            return True
    return False


def movement():
    """
    Создает двигающиеся и отрожающиеся шарики
    :return:
    """
    for i in coordinate:
        if math.fabs(i[0] - 1080) <= i[2] or i[0] <= i[2]:
            i[3] = -i[3]
        elif math.fabs(i[1] - 720) <= i[2] or i[1] <= i[2]:
            i[4] = -i[4]
        i[0] += i[3]
        i[1] += i[4]
        circle(screen, i[5], (i[0], i[1]), i[2])

