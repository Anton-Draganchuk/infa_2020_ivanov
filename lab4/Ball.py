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
    r = randint(15, 50)
    x = randint(r, 1080 - r)
    y = randint(r, 720 - r)
    vx = randint(-10, 10)
    vy = randint(-10, 10)
    color = COLORS[randint(0, 5)]
    coordinate.append([x, y, r, vx, vy, color])
    circle(screen, color, (x, y), r)


def hit(event):
    """
    Проверяет попали ли мы по шарику или нет
    :param event: Событие которое мы сделали
    :return: колличество очков за попадание
    """
    mouse_x = event.pos[0]
    mouse_y = event.pos[1]
    for i in coordinate:
        dx = mouse_x - i[0]
        dy = mouse_y - i[1]
        dist = (dx**2 + dy**2)**(1 / 2)
        if dist <= i[2]:
            coordinate.remove(i)
            new_ball()
            return int(10**5 * (math.sqrt(i[3]**2 + i[4]**2) / i[2]**2))
    return 0


def movement():
    """
    Создает двигающиеся и отрожающиеся шарики
    :return:
    """
    for i in coordinate:
        if math.fabs(i[0] - 1080) <= i[2] or i[0] <= i[2]:
            i[3] = -i[3]
        if math.fabs(i[1] - 720) <= i[2] or i[1] <= i[2]:
            i[4] = -i[4]
        i[0] += i[3]*0.3
        i[1] += i[4]*0.3
        circle(screen, i[5], (i[0], i[1]), i[2])


def collision():
    c = []
    for i in coordinate:
        for k in coordinate:
            if i != k and c.count(k) != 1:
                dist_between = math.sqrt((i[0] - k[0])**2 + (i[1] - k[1])**2)
                if dist_between <= (i[2] + k[2]):
                    v_i = math.sqrt(i[3]**2 + i[4]**2)
                    if math.sqrt((i[0] + i[3]*0.3 - k[0] + k[3]*0.3)**2 + (i[1] + i[4]*0.3 - k[1] + k[4]*0.3)**2) <= (i[2] + k[2]):
                        if i[3] == 0:
                            betta_i = math.pi / 2
                        else:
                            betta_i = math.atan(i[4] / i[3])
                        if i[0] == k[0]:
                            phi = math.pi / 2
                        else:
                            phi = math.atan((i[1] - k[1]) / (i[0] - k[0]))
                        i[3], i[4] = -1*v_i*math.cos(betta_i - phi*2), v_i*math.sin(betta_i - phi*2)
                        v_k = math.sqrt(k[3]**2 + k[4]**2)
                        if k[3] == 0:
                            betta_k = math.pi / 2
                        else:
                            betta_k = math.atan(k[4] / k[3])
                        k[3], k[4] = -1*v_k*math.cos(betta_k - phi*2), v_k*math.sin(betta_k - phi*2)
                        c.append(i)

