import math
import random
import pygame

FPS = 30

RED = (255, 0, 0)
BLUE = 0x0000FF
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
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
        self.x = tank.x + 25 * math.sin(tank.an)
        self.y = tank.y - 25 * math.cos(tank.an)
        self.r = 5
        self.vx = 0
        self.vy = 0
        self.color = random.choice(GAME_COLORS)
        self.live = 10

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        self.x += self.vx
        self.y -= self.vy
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

    def hit(self):
        for t in trucks:
            if (t.x <= self.x <= t.x + 100) and t.y <= self.y <= t.y + 53:
                t.HP -= 1
                balls.remove(self)

        for r in interface.rocks:
            if (r[0] <= self.x <= r[0] + 72) and r[1] <= self.y <= r[1] + 50:
                balls.remove(self)

        for t in tanks:
            if t.stop:
                if t.an != 0:
                    b11 = (56 * math.cos(t.an) + t.y) - math.tan(t.an) * (t.x - 56 * math.sin(t.an))
                    b10 = self.y - math.tan(t.an) * self.x
                    b12 = (t.y - 56 * math.cos(t.an)) - math.tan(t.an) * (t.x + 56 * math.sin(t.an))
                    b21 = (t.y - 20 * math.sin(t.an)) + (1 / math.tan(t.an)) * (t.x - 20 * math.cos(t.an))
                    b20 = self.y + (1 / math.tan(t.an) * self.x)
                    b22 = (t.y + 20 * math.sin(t.an)) + (1 / math.tan(t.an)) * (t.x + 20 * math.cos(t.an))
                    if t.an < 0:
                        if b11 > b10 > b12 and b21 > b20 > b22:
                            t.HP -= 1
                            balls.remove(self)
                    else:
                        if b11 > b10 > b12 and b21 < b20 < b22:
                            t.HP -= 1
                            balls.remove(self)
                else:
                    b11 = (56 * math.cos(t.an) + t.y) - math.tan(t.an) * (t.x - 56 * math.sin(t.an))
                    b10 = self.y - math.tan(t.an) * self.x
                    b12 = (t.y - 56 * math.cos(t.an)) - math.tan(t.an) * (t.x + 56 * math.sin(t.an))
                    if b11 > b10 > b12 and t.x > self.x > t.x + 39:
                        t.HP -= 1
                        balls.remove(self)
            else:
                if -56 < self.x - t.x < 56 and -20 < self.y - t.y < 20:
                    t.HP -= 1
                    balls.remove(self)

        if math.fabs(self.x - tank.x) <= 31 and math.fabs(self.y - tank.y) <= 31:
            tank.HP -= 1
            balls.remove(self)


class Tank:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 45
        self.f2_power_bullet = 10
        self.an = 0
        self.x = 400
        self.y = 500
        self.reload = 30
        self.movement = 0
        self.flag_a = 0
        self.flag_d = 0
        self.v = 10
        self.flag_a = 0
        self.flag_d = 0
        self.HP = 5
        self.bullet = 0
        self.font = pygame.font.Font(None, 25)

    def move(self):
        if self.flag_a:
            self.movement = 1
            if tank.x >= 50:
                self.x -= self.v
        if self.flag_d:
            self.movement = 1
            if tank.x <= 750:
                self.x += self.v
        if self.flag_a:
            self.an = - math.pi / 2
        elif self.flag_d:
            self.an = math.pi / 2
        if not self.flag_a and not self.flag_d:
            self.movement = 0

    def fire2_start(self):
        if not self.movement:
            if self.reload == 0:
                if not self.bullet:
                    new_ball = Ball(self.screen)
                    new_ball.vx = self.f2_power * math.sin(self.an)
                    new_ball.vy = self.f2_power * math.cos(self.an)
                    balls.append(new_ball)
                else:
                    new_bullet = Bullet(self.screen)
                    new_bullet.vx = self.f2_power_bullet * math.sin(self.an)
                    new_bullet.vy = self.f2_power_bullet * math.cos(self.an)
                    bullets.append(new_bullet)
                self.reload = 30

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
            self.screen.blit(pygame.transform.rotate(image_tank, - self.an / math.pi * 180),
                             (self.x - (69 * math.sin(self.an) + 62 * math.cos(self.an)) / 2,
                              self.y - (69 * math.cos(self.an) + 62 * math.sin(self.an)) / 2))
        else:
            self.screen.blit(pygame.transform.rotate(image_tank, - self.an / math.pi * 180),
                             (self.x - (-69 * math.sin(self.an) + 62 * math.cos(self.an)) / 2,
                              self.y - (69 * math.cos(self.an) - 62 * math.sin(self.an)) / 2))

        screen.blit(self.font.render(str(self.HP), False, RED), (self.x - 5, self.y + 70))

        if self.reload != 0:
            self.reload -= 1


class Interface:
    def __init__(self, screen):
        self.screen = screen
        self.town_hall_x = 30
        self.town_hall_y = 50
        self.town_hall_HP = 100
        self.reload_color = GREEN
        self.road_y = 70
        self.road_x = 100
        self.rocks = [[200, 400], [400, 250], [650, 300]]
        self.font = pygame.font.Font(None, 35)
        self.color_font = GREEN

    def draw_town_hall(self):
        self.screen.blit(image_town_hall, (self.town_hall_x, self.town_hall_y))
        if self.town_hall_HP <= 30:
            self.color_font = RED
        self.screen.blit(self.font.render(str(self.town_hall_HP), False, self.color_font),
                         (self.town_hall_x + 61, self.town_hall_y + 180))

    def draw_reload(self):
        self.reload_color = GREEN
        if tank.reload * 2 >= 40:
            self.reload_color = RED
        elif tank.reload * 2 >= 30:
            self.reload_color = YELLOW
        pygame.draw.rect(self.screen, self.reload_color, [tank.x - 30, tank.y + 50, 2 * tank.reload, 10])
        pygame.draw.rect(self.screen, BLACK, [tank.x - 30, tank.y + 50, 60, 10], 2)

    def draw_road(self):
        while self.road_x < 800:
            self.screen.blit(image_road, (self.road_x, self.road_y))
            self.road_x += 100
        self.road_x = 100
        self.road_y += 70
        while self.road_x < 800:
            self.screen.blit(image_road, (self.road_x, self.road_y))
            self.road_x += 100
        self.road_x = 100
        self.road_y = 70

    def draw_rock(self):
        for r in self.rocks:
            self.screen.blit(image_rock, (r[0], r[1]))

    def game_over(self):
        if self.town_hall_HP <= 0 or tank.HP <= 0:
            screen.fill(BLACK)
            self.screen.blit(self.font.render('Press ESC to exit', False, random.choice(GAME_COLORS)), (150, 400))
            self.font = pygame.font.Font(None, 80)
            self.screen.blit(self.font.render('GAME OVER', False, WHITE), (200, 250))

    def hit(self):
        global trucks
        for t in trucks:
            if t.x <= 150:
                trucks.remove(t)
                self.town_hall_HP -= 10


class Truck:
    def __init__(self, screen):
        self.screen = screen
        self.x = 800
        self.y = 80
        self.HP = 3
        self.font = pygame.font.Font(None, 25)

    def draw(self):
        screen.blit(image_truck, (self.x, self.y))
        screen.blit(self.font.render(str(self.HP), False, YELLOW), (self.x + 50, self.y - 5))
        self.x -= 1


class Hostile:
    def __init__(self, screen):
        self.screen = screen
        self.x = 800
        self.y = 200
        self.v = 1
        self.HP = 10
        self.power = 20
        self.reload = 50
        self.path = random.randint(300, 600)
        self.stop = 0
        self.an = math.pi / 2
        self.font = pygame.font.Font(None, 25)

    def draw(self):
        if self.an > 0:
            self.screen.blit(pygame.transform.rotate(image_hostile_tank, - self.an / math.pi * 180),
                             (self.x - (113 * math.sin(self.an) + 39 * math.cos(self.an)) / 2,
                              self.y - (113 * math.cos(self.an) + 39 * math.sin(self.an)) / 2))
        else:
            self.screen.blit(pygame.transform.rotate(image_hostile_tank, - self.an / math.pi * 180),
                             (self.x - (-113 * math.sin(self.an) + 39 * math.cos(self.an)) / 2,
                              self.y - (113 * math.cos(self.an) - 39 * math.sin(self.an)) / 2))
        screen.blit(self.font.render(str(self.HP), False, YELLOW), (self.x - 7, self.y - 5))

    def move(self):
        if self.x >= self.path:
            self.x -= self.v
        else:
            self.stop = 1
            if self.y - tank.y != 0:
                self.an = math.atan((tank.x - self.x) / (self.y - tank.y))
            elif tank.x > self.x:
                self.an = math.pi / 2
            elif tank.y < self.x:
                self.an = -math.pi / 2

    def fire(self):
        if self.stop:
            if self.reload == 0:
                new_ball = Ball(self.screen)
                new_ball.live = 60
                new_ball.x = self.x - 56 * math.sin(self.an)
                new_ball.y = self.y + 56 * math.cos(self.an)
                new_ball.vx = - self.power * math.sin(self.an)
                new_ball.vy = - self.power * math.cos(self.an)
                balls.append(new_ball)
                self.reload = 50
            else:
                self.reload -= 1


class Enemies:
    def __init__(self, screen):
        self.screen = screen
        self.time = 0

    def truck_spawn(self):
        if self.time == 0:
            new_truck = Truck(self.screen)
            trucks.append(new_truck)
            self.time = random.randint(90, 300)
        else:
            self.time -= 1

    def tank_spawn(self):
        if len(tanks) == 0:
            new_tank = Hostile(self.screen)
            tanks.append(new_tank)


class Enter:
    def __init__(self):
        self.screen = pygame.Surface((28, 28))
        self.win = pygame.display.set_mode((700, 700))
        self.points = []
        self.colors = []
        self.flag = False
        self.finished = False
        self.FPS = 120

    def add(self, event):
        self.points.append((event.pos[0] / 25, event.pos[1] / 25))

    def drawing(self):
        for i in self.points:
            pygame.draw.line(self.screen, BLACK, i, i, 1)

    def display(self):
        clock = pygame.time.Clock()

        while not self.finished:
            self.screen.fill(WHITE)

            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.flag = True
                elif event.type == pygame.MOUSEMOTION and self.flag:
                    self.add(event)
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.flag = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.screen.fill([0, 0, 0])
                    self.points = []
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.finished = True

            self.drawing()

            clock.tick(FPS)
            self.win.blit(pygame.transform.scale(self.screen, self.win.get_rect().size), (0, 0))
            pygame.display.update()

        self.screen.set_colorkey(WHITE)


class Bullet:
    def __init__(self, screen):
        self.screen = screen
        self.x = tank.x + 25 * math.sin(tank.an)
        self.y = tank.y - 25 * math.cos(tank.an)
        self.vx = 0
        self.vy = 0
        self.live = 40
        self.number = 2

    def move(self):
        self.x += self.vx
        self.y -= self.vy
        if self.live == 0:
            bullets.remove(self)
        else:
            self.live -= 1

    def draw(self):
        self.screen.blit(enter.screen, (self.x - 14, self.y - 14))

    def new(self):
        new_bullet = Bullet(self.screen)
        new_bullet.vx = random.randint(-5, 5)
        new_bullet.vy = random.randint(-5, 5)
        new_bullet.live = 10
        new_bullet.x = self.x + new_bullet.vx*15
        new_bullet.y = self.y + new_bullet.vy*15
        bullets.append(new_bullet)

    def hit(self):
        for t in trucks:
            if (t.x <= self.x <= t.x + 100) and t.y <= self.y <= t.y + 53:
                t.HP -= 1
                bullets.remove(self)
                for i in range(self.number):
                    self.new()

        for r in interface.rocks:
            if (r[0] <= self.x <= r[0] + 72) and r[1] <= self.y <= r[1] + 50:
                bullets.remove(self)

        for t in tanks:
            if t.stop:
                if t.an != 0:
                    b11 = (56 * math.cos(t.an) + t.y) - math.tan(t.an) * (t.x - 56 * math.sin(t.an))
                    b10 = self.y - math.tan(t.an) * self.x
                    b12 = (t.y - 56 * math.cos(t.an)) - math.tan(t.an) * (t.x + 56 * math.sin(t.an))
                    b21 = (t.y - 20 * math.sin(t.an)) + (1 / math.tan(t.an)) * (t.x - 20 * math.cos(t.an))
                    b20 = self.y + (1 / math.tan(t.an) * self.x)
                    b22 = (t.y + 20 * math.sin(t.an)) + (1 / math.tan(t.an)) * (t.x + 20 * math.cos(t.an))
                    if t.an < 0:
                        if b11 > b10 > b12 and b21 > b20 > b22:
                            t.HP -= 1
                            bullets.remove(self)
                            for i in range(self.number):
                                self.new()
                    else:
                        if b11 > b10 > b12 and b21 < b20 < b22:
                            t.HP -= 1
                            bullets.remove(self)
                            for i in range(self.number):
                                self.new()
                else:
                    b11 = (56 * math.cos(t.an) + t.y) - math.tan(t.an) * (t.x - 56 * math.sin(t.an))
                    b10 = self.y - math.tan(t.an) * self.x
                    b12 = (t.y - 56 * math.cos(t.an)) - math.tan(t.an) * (t.x + 56 * math.sin(t.an))
                    if b11 > b10 > b12 and t.x > self.x > t.x + 39:
                        t.HP -= 1
                        bullets.remove(self)
                        for i in range(self.number):
                            self.new()
            else:
                if -56 < self.x - t.x < 56 and -20 < self.y - t.y < 20:
                    t.HP -= 1
                    bullets.remove(self)
                    for i in range(self.number):
                        self.new()


pygame.init()

enter = Enter()
enter.display()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

image_background = pygame.transform.scale(pygame.image.load('background.png'), (800, 600))
image_tank = pygame.transform.scale(pygame.image.load('tank.png').convert_alpha(), (62, 69))
image_town_hall = pygame.transform.scale(pygame.image.load('town hall.png').convert_alpha(), (162, 172))
image_road = pygame.transform.scale(pygame.image.load('road.png').convert_alpha(), (100, 100))
image_truck = pygame.transform.scale(pygame.image.load('truck.png').convert_alpha(), (100, 53))
image_rock = pygame.transform.scale(pygame.image.load('rock.png').convert_alpha(), (72, 50))
image_hostile_tank = pygame.transform.scale(pygame.image.load('hostile tank.png').convert_alpha(), (39, 113))

balls = []
bullets = []
trucks = []
tanks = []
tank = Tank(screen)
interface = Interface(screen)
enemies = Enemies(screen)

finished = False

while not finished:
    clock.tick(FPS)

    enemies.truck_spawn()
    enemies.tank_spawn()
    screen.blit(image_background, (0, 0))
    interface.draw_road()
    interface.draw_town_hall()
    interface.draw_rock()
    interface.draw_reload()
    interface.hit()
    for t in trucks:
        t.draw()
    for t in tanks:
        t.draw()
        t.move()
        t.fire()
    tank.draw()
    for b in balls:
        b.draw()
        b.hit()
    for b in bullets:
        b.draw()
        b.hit()

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == 27):
            finished = True
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if tank.bullet:
                tank.bullet = 0
            else:
                tank.bullet = 1
        elif event.type == pygame.MOUSEMOTION:
            tank.targetting(event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            tank.fire2_start()
        if event.type == pygame.KEYUP and event.key == pygame.K_a:
            tank.flag_a = 0
        elif (event.type == pygame.KEYDOWN and event.key == pygame.K_a) or tank.flag_a:
            tank.flag_a = 1
        if event.type == pygame.KEYUP and event.key == pygame.K_d:
            tank.flag_d = 0
        elif (event.type == pygame.KEYDOWN and event.key == pygame.K_d) or tank.flag_d:
            tank.flag_d = 1

    tank.move()
    for b in balls:
        b.move()
    for b in bullets:
        b.move()
    for t in trucks:
        if t.HP <= 0:
            trucks.remove(t)
    for t in tanks:
        if t.HP <= 0:
            tanks.remove(t)

    interface.game_over()

    pygame.display.update()

pygame.quit()

