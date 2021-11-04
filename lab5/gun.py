import math
import random as choice

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
        if gun.an <= 0:
            self.x = gun.x+120*math.cos(gun.an)-(63 / 2)*math.sin(gun.an)
            self.y = gun.y+(63 / 2)*math.cos(gun.an)
        else:
            self.x = 20+120*math.cos(gun.an)+(63 / 2)*math.sin(gun.an)
            self.y = 410+120*math.sin(gun.an)+(63 / 2)*math.cos(gun.an)
        self.r = 5
        self.vx = 0
        self.vy = 0
        self.a = 2
        self.color = choice.choice(GAME_COLORS)
        self.live = 60

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        if math.fabs(WIDTH - self.x) <= self.r + self.vx and self.vx > 0:
            self.x = WIDTH - self.r
            self.vx *= -1
        else:
            self.x += self.vx
        if math.fabs(HEIGHT - self.y) <= self.r - self.vy and self.vy < 0:
            self.y = HEIGHT - self.r
            self.vy *= -0.7
            self.vx *= 0.6
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

    def hittest(self):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        for obj in target:
            if math.sqrt((self.x - obj.x)**2 + (self.y - obj.y)**2) <= self.r + obj.r:
                obj.hit()
                target.remove(obj)
                new_target = Target(self.screen)
                target.append(new_target)
                return True
        return False


class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.thickness = 7
        self.length = 15
        self.color = BLACK
        self.x = 20
        self.y = 410

    def fire2_start(self, event):
        self.f2_on = 1
        sound_reload.play()

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen)
        new_ball.r += 5
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10
        sound_shot.play()

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            if event.pos[0]-self.x == 0:
                self.an = math.pi / 2
            else:
                self.an = math.atan((event.pos[1]-self.y) / (event.pos[0]-self.x))

    def draw(self):
        screen.blit(pygame.transform.rotate(image_gun, - self.an / math.pi * 180), (self.x, self.y))

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 50:
                self.f2_power += 1


class Target:
    def __init__(self, screen):
        self.screen = screen
        self.r = choice.randint(10, 50)
        self.x = choice.randint(300, 780 - self.r)
        self.y = choice.randint(30 + self.r, 480 - self.r)
        self.vx = choice.randint(2, 5)
        self.vy = choice.randint(2, 5)
        self.color = RED

    def move(self):
        """ Инициализация новой цели. """
        if math.fabs(WIDTH - self.x) <= self.r + self.vx and self.vx > 0:
            self.x = WIDTH - self.r
            self.vx *= -1
        elif math.fabs(300 - self.x) <= self.r + self.vx and self.vx < 0:
            self.x = 300 + self.r
            self.vx *= -1
        else:
            self.x += self.vx
        if math.fabs(500 - self.y) <= self.r - self.vy and self.vy < 0:
            self.y = 500 - self.r
            self.vy *= -1
        elif self.y <= self.r - self.vy and self.vy > 0:
            self.y = self.r
            self.vy *= -1
        else:
            self.y -= self.vy

    def hit(self):
        """Попадание шарика в цель."""
        global points
        points += 1

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)
        pygame.draw.circle(self.screen, BLACK, (self.x, self.y), self.r, 1)


class Interface:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 30)

    def blit_points(self):
        self.screen.blit(self.font.render(str(points), False, BLACK), (20, 30))

    def blit_hit(self):
        pygame.draw.rect(self.screen, WHITE, [240, 290, 390, 40])
        if bullet == 1:
            self.text = 'Вы уничтожили цель за ' + str(bullet) + ' выстрел'
        elif bullet <= 4:
            self.text = 'Вы уничтожили цель за ' + str(bullet) + ' выстрела'
        else:
            self.text = 'Вы уничтожили цель за ' + str(bullet) + ' выстрелов'
        self.screen.blit(self.font.render(self.text, False, BLACK), (250, 300))

    def power(self):
        self.color = GREEN
        if gun.f2_power >= 40:
            self.color = RED
        elif gun.f2_power >= 30:
            self.color = YELLOW
        pygame.draw.rect(self.screen, self.color, [50, 30, 2*gun.f2_power, 10])
        pygame.draw.rect(self.screen, BLACK, [50, 30, 100, 10], 2)


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
points = 0
balls = []
pause = 0
target = []

pygame.mixer.init()
pygame.mixer.music.load('Gp.mp3')
pygame.mixer.music.play(-1)
sound_shot = pygame.mixer.Sound('Shot.wav')
sound_reload = pygame.mixer.Sound('Reload.wav')
sound_win1 = pygame.mixer.Sound('Sound1.wav')
sound_win2 = pygame.mixer.Sound('Sound2.wav')
sound_win3 = pygame.mixer.Sound('Sound3.wav')
sound_win4 = pygame.mixer.Sound('Sound4.wav')
sound_win5 = pygame.mixer.Sound('Sound5.wav')
sound_win6 = pygame.mixer.Sound('Sound6.wav')
sound_win7 = pygame.mixer.Sound('Sound7.wav')
sound_win8 = pygame.mixer.Sound('Sound8.wav')
sound_win9 = pygame.mixer.Sound('Sound9.wav')
playlist = [sound_win1, sound_win2, sound_win3, sound_win4, sound_win5, sound_win6, sound_win7, sound_win8, sound_win9]

image = pygame.image.load('Gelik.png').convert_alpha()
new_image = pygame.transform.scale(image, (WIDTH, HEIGHT))

image_gun = pygame.transform.scale(pygame.image.load('Gun.png').convert_alpha(), (120, 63))


clock = pygame.time.Clock()
gun = Gun(screen)
for i in range(2):
    new_target = Target(screen)
    target.append(new_target)
interface = Interface(screen)
finished = False
shot = False

while not finished:
    screen.fill(WHITE)
    screen.blit(new_image, (0, 0))
    gun.draw()
    interface.blit_points()
    interface.power()
    if pause == 0:
        pygame.mixer.music.set_volume(1)
        for obj in target:
            obj.draw()
        for b in balls:
            b.draw()
        pygame.display.update()

        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                finished = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                gun.fire2_start(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                gun.fire2_end(event)
            elif event.type == pygame.MOUSEMOTION:
                gun.targetting(event)
            elif (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or shot:
                gun.f2_power = 50
                gun.fire2_end(event)
                shot = True
            elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                shot = False

        for obj in target:
            obj.move()
        for b in balls:
            b.move()
            if b.hittest():
                pause = 100
                pygame.mixer.music.set_volume(0.5)
                choice.choice(playlist).play()

        gun.power_up()
    else:
        interface.blit_hit()
        for b in balls:
            b.draw()
        pygame.display.update()

        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == 27):
                finished = True
            elif event.type == pygame.MOUSEMOTION:
                gun.targetting(event)

        for b in balls:
            b.move()

        pause -= 1
        if pause == 0:
            bullet = 0


pygame.quit()

