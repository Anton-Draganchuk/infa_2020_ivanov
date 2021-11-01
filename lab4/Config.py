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
Ball_number = 10
