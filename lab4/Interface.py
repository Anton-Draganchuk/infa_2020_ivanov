import pygame
from pygame.draw import *
from random import randint
import math
from Config import *
pygame.init()

FPS = 60
screen = pygame.display.set_mode((1080, 720))


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
    if 1050 >= mouse_x >= 870 and 75 >= mouse_y >= 45:
        return True


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

