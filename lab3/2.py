import pygame
from pygame.draw import *

pygame.init()

FPS = 30
screen = pygame.display.set_mode((400, 400))

# Colors
Sand = [218, 165, 32]
Sea = [0, 139, 139]
Deck = [139, 69, 19]
Sail = [255, 255, 255]
Mast = [0, 0, 0]
Clouds = [245, 245, 245]
Sun = [255, 165, 0]
Sky = [224, 255, 255]
Umbrella = [255, 105, 180]
Stick = [160, 82, 45]
Circuit = [0, 0, 0]
Window = [255, 255, 255]


def picture():
    """
    Рисует картину с морем и караблем
    :return: Картина
    """
    Sky_size = 150
    Sea_size = 150
    Sand_size = 100
    # sum of Sky_size, Sea_size, Sand_size should be equal Screen_size
    landscape(Sky_size, Sea_size, Sand_size)

    Sun_pos = [340, 60]
    Sun_radius = 30
    sun(Sun_pos, Sun_radius)

    Cloud_pos = [100, 50]
    cloud(Cloud_pos)

    Ship_pos = [250, Sky_size + 50]
    Ship_size = [150, 150]
    ship(Ship_pos, Ship_size)

    Umbrella_pos = [100, 250]
    Umbrella_size = [100, 150]
    umbrella(Umbrella_pos, Umbrella_size)


def landscape(Sky_size, Sea_size, Sand_size):
    """
    Рисует задний фон, небо, море, песок
    :param Sky_size: Ширина неба
    :param Sea_size: Ширина Моря
    :param Sand_size: Ширина Песка
    :return: Рисунок заднего фона
    """
    rect(screen, Sky, (0, 0, 400, Sky_size))
    rect(screen, Sea, (0, Sky_size, 400, Sea_size))
    rect(screen, Sand, (0, Sky_size + Sea_size, 400, Sand_size))


def sun(Sun_pos, Sun_radius):
    """
    Рисует солнце
    :param Sun_pos: Координаты солнца
    :param Sun_radius: Радиус солнца
    :return: Рисунок солнца
    """
    circle(screen, Sun, Sun_pos, Sun_radius)


def cloud(Cloud_pos):
    """
    Рисует облака
    :param Cloud_pos: координата центра облака
    :return: Рисунок облак
    """
    circle(screen, Clouds, (Cloud_pos[0] - 20, Cloud_pos[1]), 20)
    circle(screen, Circuit, (Cloud_pos[0] - 20, Cloud_pos[1]), 20, 1)
    circle(screen, Clouds, Cloud_pos, 20)
    circle(screen, Circuit, Cloud_pos, 20, 1)
    circle(screen, Clouds, (Cloud_pos[0] + 20, Cloud_pos[1]), 20)
    circle(screen, Circuit, (Cloud_pos[0] + 20, Cloud_pos[1]), 20, 1)
    circle(screen, Clouds, (Cloud_pos[0] + 30, Cloud_pos[1] + 20), 20)
    circle(screen, Circuit, (Cloud_pos[0] + 30, Cloud_pos[1] + 20), 20, 1)
    circle(screen, Clouds, (Cloud_pos[0] + 10, Cloud_pos[1] + 20), 20)
    circle(screen, Circuit, (Cloud_pos[0] + 10, Cloud_pos[1] + 20), 20, 1)
    circle(screen, Clouds, (Cloud_pos[0] - 10, Cloud_pos[1] + 20), 20)
    circle(screen, Circuit, (Cloud_pos[0] - 10, Cloud_pos[1] + 20), 20, 1)
    circle(screen, Clouds, (Cloud_pos[0] - 30, Cloud_pos[1] + 20), 20)
    circle(screen, Circuit, (Cloud_pos[0] - 30, Cloud_pos[1] + 20), 20, 1)


def ship(Ship_pos, Ship_size):
    """
    Рисует Корабль
    :param Ship_pos: Координата корабля
    :param Ship_size: Размеры прямоугольника, в который будет вписан корабль
    :return: Рисунок корабля
    """
    rect(screen, Deck, (int(Ship_pos[0] - Ship_size[0] / 4), int(Ship_pos[1] + Ship_size[1] / 4),
                        int(Ship_size[0] / 2), int(Ship_size[1] / 4)))
    polygon(screen, Deck, [(int(Ship_pos[0] + Ship_size[0] / 4), int(Ship_pos[1] + Ship_size[1] / 4)),
                           (int(Ship_pos[0] + Ship_size[0] / 2), int(Ship_pos[1] + Ship_size[1] / 4)),
                           (int(Ship_pos[0] + Ship_size[0] / 4), int(Ship_pos[1] + Ship_size[1] / 2)),
                           (int(Ship_pos[0] + Ship_size[0] / 4), int(Ship_pos[1] + Ship_size[1] / 4))])
    circle(screen, Deck, (int(Ship_pos[0] - Ship_size[0] / 4), int(Ship_pos[1] + Ship_size[1] / 4)),
           int(Ship_size[1] / 4), draw_bottom_left=True)
    rect(screen, Mast, (int(Ship_pos[0] - Ship_size[0] / 5), int(Ship_pos[1] - Ship_size[1] / 2),
                        int(Ship_size[0] / 15), int(Ship_size[1]*(3 / 4))))
    polygon(screen, Sail, [(int(Ship_pos[0] - Ship_size[0] / 5 + Ship_size[0] / 15), int(Ship_pos[1] - Ship_size[1] / 2)),
                     (int(Ship_pos[0] + Ship_size[0] / 4), int(Ship_pos[1] - Ship_size[1] / 8)),
                     (int(Ship_pos[0] - Ship_size[0] / 5 + Ship_size[0] / 15), int(Ship_pos[1] + Ship_size[1] / 4)),
                     (int(Ship_pos[0]), int(Ship_pos[1] - Ship_size[1] / 8)),
                     (int(Ship_pos[0] - Ship_size[0] / 5 + Ship_size[0] / 15), int(Ship_pos[1] - Ship_size[1] / 2))])
    polygon(screen, Circuit, [(int(Ship_pos[0] - Ship_size[0] / 5 + Ship_size[0] / 15), int(Ship_pos[1] - Ship_size[1] / 2)),
                     (int(Ship_pos[0] + Ship_size[0] / 4), int(Ship_pos[1] - Ship_size[1] / 8)),
                     (int(Ship_pos[0] - Ship_size[0] / 5 + Ship_size[0] / 15), int(Ship_pos[1] + Ship_size[1] / 4)),
                     (int(Ship_pos[0]), int(Ship_pos[1] - Ship_size[1] / 8)),
                     (int(Ship_pos[0] - Ship_size[0] / 5 + Ship_size[0] / 15), int(Ship_pos[1] - Ship_size[1] / 2))], 1)
    line(screen, Circuit, (int(Ship_pos[0] + Ship_size[0] / 4), int(Ship_pos[1] - Ship_size[1] / 8)),
         (int(Ship_pos[0]), int(Ship_pos[1] - Ship_size[1] / 8)), 1)
    circle(screen, Window, (int(Ship_pos[0] + Ship_size[0] / 3), int(Ship_pos[1] + Ship_size[1] / 3)),
           int(Ship_size[0] / 20))
    circle(screen, Circuit, (int(Ship_pos[0] + Ship_size[0] / 3), int(Ship_pos[1] + Ship_size[1] / 3)),
           int(Ship_size[0] / 20), 1)


def umbrella(Umbrella_pos, Umbrella_size):
    """
    Рисует зонтик
    :param Umbrella_pos: координата зонтика
    :param Umbrella_size: Размеры прямоугольника, в который будет вписан зонтик
    :return: Рисунок зонтика
    """
    rect(screen, Stick, (int(Umbrella_pos[0] - Umbrella_size[0] / 22), int(Umbrella_pos[1] - Umbrella_size[1] / 2),
                         int(Umbrella_size[0] / 11), int(Umbrella_size[1])))
    polygon(screen, Umbrella, [(int(Umbrella_pos[0] - Umbrella_size[0] / 22),
                                int(Umbrella_pos[1] - Umbrella_size[1] / 2)),
                               (int(Umbrella_pos[0] + Umbrella_size[0] / 22),
                                int(Umbrella_pos[1] - Umbrella_size[1] / 2)),
                               (int(Umbrella_pos[0] + Umbrella_size[0] / 2), int(Umbrella_pos[1] - Umbrella_size[1] / 4)),
                               (int(Umbrella_pos[0] - Umbrella_size[0] / 2), int(Umbrella_pos[1] - Umbrella_size[1] / 4)),
                               (int(Umbrella_pos[0] - Umbrella_size[0] / 22),
                                int(Umbrella_pos[1] - Umbrella_size[1] / 2))])
    N = 3
    x_1 = int(Umbrella_pos[0] - Umbrella_size[0] / 22)
    y_1 = int(Umbrella_pos[1] - Umbrella_size[1] / 2)
    dx = int(Umbrella_size[0] / (2*N + 1))
    y_2 = int(Umbrella_pos[1] - Umbrella_size[1] / 4)
    x_2 = int(Umbrella_pos[0] - Umbrella_size[0] / 2)
    # Number of stick
    for i in range(0, N):
        x_2 += dx
        line(screen, Circuit, (x_1, y_1), (x_2, y_2), 1)
    x_1 = int(Umbrella_pos[0] + Umbrella_size[0] / 22)
    for i in range(0, N):
        x_2 += dx
        line(screen, Circuit, (x_1, y_1), (x_2, y_2), 1)


picture()

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
