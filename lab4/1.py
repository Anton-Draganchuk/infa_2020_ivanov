import pygame
from pygame.draw import *
from random import randint
import math
pygame.init()

FPS = 60
screen = pygame.display.set_mode((1080, 720))

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
GAY = (102, 178, 255)
White = (255, 255, 255)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]
Score = 0
coordinate = []
Ball_number = 6


def new_ball():
    """
    Создает новый шарик в случайном месте
    :return: Шарик случайного размера и цвета
    """
    global coordinate
    r = randint(10, 100)
    x = randint(r, 1080 - r)
    y = randint(r, 720 - r)
    vx = randint(2, 5)
    vy = randint(2, 5)
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


def exit_buttom():
    """
    Кнопка выхода
    :return: ВЫход из игры
    """
    pygame.draw.rect(screen, GAY, (870, 45, 180, 30))
    font = pygame.font.SysFont(None, 30)
    img = font.render('Press to exit', True, BLACK)
    screen.blit(img, (900, 50))


def exit(event):
    """
    Реализует выход из игры
    :param event: Событие которое мы сделали
    :return: Выход из игры
    """
    mouse_x = event.pos[0]
    mouse_y = event.pos[1]
    if mouse_x <= 1050 and mouse_x >= 870 and mouse_y <= 75 and mouse_y >= 45:
        return True
    else:
        return False


def counter(event, Score):
    """
    Счетчик очков
    :param event: Событие которое произошло
    :return: Очки
    """
    text = 'Score: ' + str(Score)
    font = pygame.font.SysFont(None, 20)
    img = font.render(text, True, BLACK)
    screen.blit(img, (50, 50))


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


screen.fill(White)


for i in range(0, Ball_number):
    new_ball()


pygame.display.update()
clock = pygame.time.Clock()
start = True


while start:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            finished = False
            start = False


while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == 27):
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if hit(event):
                Score += 1
            elif exit(event):
                finished = True
    screen.fill(White)
    movement()
    exit_buttom()
    counter(event, Score)
    pygame.display.update()


pygame.quit()

