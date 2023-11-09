import math
from random import choice
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
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600


class Ball:
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 30
        self.gy = 0.4

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        # FIXME
        self.x += self.vx
        self.y -= self.vy
        if self.x>800:
            self.x = 800
            self.vx*=-0.5
            if abs(self.vx)<0.5:
                self.vx=0
        if self.x<0:
            self.x = 0
            self.vx*=-0.5
            if abs(self.vx)<0.5:
                self.vx=0
        if self.y>600:
            self.y = 600
            self.vy*=-0.5
            if abs(self.vy)<0.5:
                self.vy=0
        if self.y<0:
            self.y = 0
            self.vy*=-0.5
            if abs(self.vy)<0.5:
                self.vy=0
        self.vy -= self.gy
    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        collision = False
        if (obj.x-self.x)**2+(obj.y-self.y)**2<=(self.r + obj.r)**2:
            collision=True
        return collision


class Gun:
    def __init__(self, screen, x=40, y=450):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY
        self.x = x
        self.y = y
        self.color = BLACK
    def fire2_start(self, event):
        self.f2_on = 1
        self.color = YELLOW
    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan((event.pos[1]-450) / (event.pos[0]-20))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self,):
        # FIXIT don't know how to do it
        pygame.draw.line(screen, self.color, (self.x,self.y),(self.x+math.cos(self.an)*self.f2_power,self.y+math.sin(self.an)*self.f2_power), width=5)
    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY
font_name=pygame.font.match_font('arial')
def draw_text(text,c,size,color=(0,0,0)):
    font=pygame.font.Font(pygame.font.match_font('arial'),size)
    text_surface=font.render(text,True,color)
    text_rect=text_surface.get_rect()
    text_rect.center=c
    screen.blit(text_surface,text_rect)
def rnd(x,y):
    return random.randint(x,y)
class Target:
    def __init__(self):
        self.points = 0
        self.live = 1
        # FIXME: don't work!!! How to call this functions when object is created?
        self.new_target()

    def new_target(self):
        """ Инициализация новой цели. """
        self.x = rnd(600, 780)
        self.y = rnd(300, 550)
        self.r = rnd(2, 50)
        self.color = RED
        self.points = 0
        self.live = 1

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x,self.y), self.r)


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []

clock = pygame.time.Clock()
gun = Gun(screen)
target = Target()
finished = False
winner = False
total_count = 0
while not finished:
    screen.fill(WHITE)
    gun.draw()
    if not winner:
        target.draw()
    for b in balls:
        b.draw()
    draw_text(f'{total_count}',(10,10),18)
    if winner:
        draw_text(f'Вы уничтожили цель за {count} выстрелов!',(400,300),18)
        if pygame.time.get_ticks() - win_time>=3000:
            winner = False
            target.new_target()
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)
    for b in balls:
        b.move()
        if b.hittest(target) and target.live:
            count = len(balls)
            balls = []
            target.live = 0
            total_count += 1
            target.hit()
            winner=True
            win_time=pygame.time.get_ticks()
    gun.power_up()

pygame.quit()
