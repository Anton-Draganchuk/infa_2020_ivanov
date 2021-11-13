import math
import random
import pygame

FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600


class Ball:
    def __init__(self, screen: pygame.Surface):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = tank.x + 25*math.sin(tank.an)
        self.y = tank.y - 25*math.cos(tank.an)
        self.r = 5
        self.vx = 0
        self.vy = 0
        self.a = 2
        self.color = random.choice(GAME_COLORS)
        self.live = 60

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        self.x += self.vx
        if math.fabs(HEIGHT - 100 - self.y) <= self.r - self.vy and self.vy < 0:
            self.y = HEIGHT - 100 - self.r
            balls.remove(self)
        else:
            self.y -= self.vy
        self.vy -= self.a
        if self.live == 0:
            balls.remove(self)
        else:
            self.live -= 1

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )
        pygame.draw.circle(
            self.screen,
            BLACK,
            (self.x, self.y),
            self.r,
            1
        )


class Tank:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 45
        self.an = 0
        self.x = 400
        self.y = 500
        self.reload = 0
        self.movement = 0
        self.flag_a = 0
        self.flag_d = 0
        self.v = 10

    def move(self, event):
        if event.type == pygame.KEYUP and event.key == pygame.K_a:
            tank.movement = 0
            self.flag_a = 0
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_a) or self.flag_a:
            tank.movement = 1
            tank.x -= self.v
            self.flag_a = 1
        if event.type == pygame.KEYUP and event.key == pygame.K_d:
            tank.movement = 0
            self.flag_d = 0
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_d) or self.flag_d:
            tank.movement = 1
            tank.x += self.v
            self.flag_d = 1
        if self.flag_a:
            self.an = - math.pi / 2
        elif self.flag_d:
            self.an = math.pi / 2

    def fire2_start(self):
        global balls
        if not self.movement:
            if self.reload == 0:
                new_ball = Ball(self.screen)
                new_ball.vx = self.f2_power * math.sin(self.an)
                new_ball.vy = self.f2_power * math.cos(self.an)
                balls.append(new_ball)
                self.f2_power = 45
                self.reload = 0

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if self.y - event.pos[1] != 0:
            self.an = math.atan((event.pos[0] - self.x) / (self.y - event.pos[1]))
        elif event.pos[0] > self.x:
            self.an = math.pi / 2
        elif event.pos[0] < self.x:
            self.an = -math.pi / 2

    def draw(self):
        if self.an > 0:
            screen.blit(pygame.transform.rotate(image_tank, - self.an / math.pi * 180),
                        (self.x - (69*math.sin(self.an) + 62*math.cos(self.an)) / 2,
                         self.y - (69*math.cos(self.an) + 62*math.sin(self.an)) / 2))
        else:
            screen.blit(pygame.transform.rotate(image_tank, - self.an / math.pi * 180),
                        (self.x - (-69*math.sin(self.an) + 62*math.cos(self.an)) / 2,
                         self.y - (69*math.cos(self.an) - 62*math.sin(self.an)) / 2))
        if self.reload != 0:
            self.reload -= 1


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

image_background = pygame.transform.scale(pygame.image.load('background.jpg'), (800, 600))
image_tank = pygame.transform.scale(pygame.image.load('tank.png').convert_alpha(), (62, 69))

balls = []
tank = Tank(screen)

finished = False

while not finished:
    clock.tick(FPS)

    screen.blit(image_background, (0, 0))
    tank.draw()
    for b in balls:
        b.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == 27):
            finished = True
        elif event.type == pygame.MOUSEMOTION:
            tank.targetting(event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            tank.fire2_start()
        tank.move(event)

    for b in balls:
        b.move()

    pygame.display.update()

pygame.quit()

