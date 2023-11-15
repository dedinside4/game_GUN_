import math
from random import choice
import random
import pygame


FPS = 120

RED = (255,0,0)
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = (125,125,125)
print(GREY,RED)
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 700
HEIGHT = 760


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
        self.r = 4
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 1
        self.gy = -0.15
        self.killtime=pygame.time.get_ticks()+230000
    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        # FIXME
        self.x += self.vx
        self.y += self.vy
        if self.x>WIDTH - self.r:
            self.x = WIDTH - self.r
            self.vx*=-0.5
            self.vy*=0.9
            if abs(self.vx)<0.5:
                self.vx=0
        if self.x<self.r:
            self.x = self.r
            self.vx*=-0.5
            self.vy*=0.9
            if abs(self.vx)<0.5:
                self.vx=0
        if self.y>=HEIGHT - self.r:
            self.y = HEIGHT - self.r
            self.vy*=-0.5
            self.vx*=0.9
            if abs(self.vy)<0.5 and self.gy<0:
                self.vy=0
                self.gy=0
                self.killtime=pygame.time.get_ticks()
        if self.y<self.r:
            self.y = self.r
            self.vy*=-0.5
            self.vx*=0.9
            if abs(self.vy)<0.5:
                self.killtime=pygame.time.get_ticks()
                self.vy=0
                self.gy=0
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
    def do_you_want_to_die(self):
        if pygame.time.get_ticks()-self.killtime>=300:
            balls.remove(self)

class Gun:
    def __init__(self, screen, x=WIDTH/2, y=HEIGHT):
        self.screen = screen
        self.f2_power = WIDTH/60
        self.f2_on = 0
        self.an = 0
        self.color = GREY
        self.bottom=WIDTH/30
        self.top=WIDTH/40
        self.left=WIDTH/30
        self.right=self.left
        self.x = x
        self.y = y-self.bottom
        self.rect = pygame.Rect(self.x-self.left,self.y,2*self.left,self.bottom)
        self.v1 = WIDTH/(FPS*1.3)
        self.v2 = self.v1*0.4
        self.v = 0
        self.tank_color = GREY
        self.live=7
        self.cooldown=False
        self.cooldown_time=5000
        self.last_shot=-230000
        self.invincible=False
        self.got_invincible=pygame.time.get_ticks()
        self.invincible_time=4000
        self.continues=0
    def get_rect(self):
        self.rect = pygame.Rect(self.x-self.left,self.y,2*self.left,self.bottom)
    def fire2_start(self, event):
        self.f2_on = 1
        self.color = YELLOW
    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls
        new_ball = Ball(self.screen,self.x,self.y)
        new_ball.r += 5
        #self.an = math.atan2((event.pos[0] - new_ball.x), (new_ball.y - event.pos[1]))
        new_ball.vx = self.f2_power * math.sin(self.an)*0.7+self.v
        new_ball.vy = - self.f2_power * math.cos(self.an)*0.7
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = WIDTH/60
        self.cooldown=True
        self.last_shot=pygame.time.get_ticks()
        gunshot_normal_sound.play()
    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        try:
            self.an = math.atan2((event[0] - self.x), (self.y - event[1]))
        except:
            self.an = -math.pi/2
        if self.f2_on:
            self.color = RED
    def draw(self):
        # FIXIT don't know how to do it
        self.get_rect()
        pygame.draw.line(screen, self.color, (self.x,self.y),(self.x+math.sin(self.an)*self.f2_power,self.y-math.cos(self.an)*self.f2_power), width=5)
        pygame.draw.ellipse(screen, self.tank_color, self.rect)
    def power_up(self):
        if self.f2_on:
            if self.f2_power < WIDTH/20:
                self.f2_power += WIDTH/(60*FPS*1)
            self.color = RED
    def get_hit(self):
        if pygame.time.get_ticks()-self.got_invincible>=self.invincible_time:
            self.invincible=False
        if not self.invincible:
            global bullets
            self.live-=1
            if self.live==0:
                self.deadend()
            bullets=[]
            self.invincible=True
            self.got_invincible=pygame.time.get_ticks()
        
    def deadend(self):
        if self.continues>0:
            offer_continue()
            self.continues-=1
        else:
            game_over()
    def move(self):
        keystate=pygame.key.get_pressed()
        if keystate[pygame.K_LSHIFT]:
            v=self.v2
        else:
            v=self.v1
        if keystate[pygame.K_a]:
            self.v=-v
        elif keystate[pygame.K_d]:
            self.v=v
        else:
            self.v=0
        self.x+=self.v
        if self.x<self.left:
            self.x=self.left
        elif self.x>WIDTH-self.right:
            self.x=WIDTH-self.right
    def cooling(self):
        if self.cooldown:
            if pygame.time.get_ticks() - self.last_shot>=self.cooldown_time:
                self.color = GREY
                self.cooldown = False
            else:
                k = (pygame.time.get_ticks() - self.last_shot)/self.cooldown_time
                r1,g1,b1=RED
                r2,g2,b2=GREY
                self.color = (r1+k*(r2-r1),g1+k*(g2-g1),b1+k*(b2-b1))
class Target:
    def __init__(self):
        self.points = 0
        self.live = 1
        # FIXME: don't work!!! How to call this functions when object is created?
        self.new_target()

    def new_target(self):
        """ Инициализация новой цели."""
        self.x = rnd(600, 780)
        self.y = rnd(300, 550)
        self.r = rnd(46, 50)#self.r = rnd(2, 50)
        self.vx = rnd(0,0)#self.vx = rnd(-5,5)
        self.vy = rnd(0,0)#self.vy = rnd(-5,5)
        self.color = RED
        self.points = 0
        self.live = 1
        
    def move(self):
        self.x += self.vx
        self.y += self.vy
        if self.x>WIDTH - self.r:
            self.x = WIDTH - self.r
            self.vx*=-1
        if self.x<self.r:
            self.x = self.r
            self.vx*=-1
        if self.y>HEIGHT - self.r:
            self.y = HEIGHT - self.r
            self.vy*=-1
        if self.y<self.r:
            self.y = self.r
            self.vy*=-1
    def hit(self,ball ,points=1):
        """Попадание шарика в цель."""
        self.points += points
        self.live-=1
    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x,self.y), self.r)
    def attack(self):
        pass
class Bullet:
    def __init__(self,vx,vy,x,y):
        self.vy=vy
        self.vx=vx
        self.x=x
        self.y=y
    def hit_ball(self,ball):
        bullets.remove(self)
    def hit_tank(self):
        bullets.remove(self)
        gun.get_hit()
    def move(self):
        self.x+=self.vx
        self.y+=self.vy
class CircleBullet1(Bullet):
    def __init__(self,vx,vy,x,y,r=8):
        Bullet.__init__(self,vx,vy,x,y)
        self.r=r
        self.color=RED
        self.rect=self.x-self.r/math.sqrt(2),self.y-self.r/math.sqrt(2),self.r/math.sqrt(8),self.r/math.sqrt(8)
    def ball_hittest(self,obj):
        collision = False
        if (obj.x-self.x)**2+(obj.y-self.y)**2<=(self.r + obj.r)**2:
            collision=True
        return collision
    def get_rect(self):
        self.rect=pygame.Rect(self.x-self.r/math.sqrt(2),self.y-self.r/math.sqrt(2),self.r/math.sqrt(8),self.r/math.sqrt(8))
    def tank_hittest(self):
        gun.get_rect()
        self.get_rect()
        collision=self.rect.colliderect(gun.rect)
        return collision
    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x,self.y), self.r) 
        
class Boss:
    def __init__(self,x=WIDTH/2,y=HEIGHT*1/5,r=WIDTH/10):
        self.x=x
        self.y=y
        self.r=r
        self.color=RED
        self.live=4
    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x,self.y), self.r)
    def move(self):
        pass
    def hit(self,ball):
        self.live-=1
        balls.remove(ball)
        print(self.live)
    def attack(self):
        AttackPattern1.activate(self.x,self.y,WIDTH/8)  
class AttackPattern1:
    last_shot=pygame.time.get_ticks()
    delay=1000
    v=7
    count=random.randint(35,45)
    phase=random.random()
    def activate(x,y,r):
        if pygame.time.get_ticks() - AttackPattern1.last_shot>=AttackPattern1.delay:
            AttackPattern1.phase=random.random()*2*math.pi/AttackPattern1.count
            AttackPattern1.scatter(x,y,r)
            AttackPattern1.last_shot=pygame.time.get_ticks()
    def scatter(x,y,r):
        global bullets
        for i in range(0,AttackPattern1.count):
            angle=i*2*math.pi/AttackPattern1.count+AttackPattern1.phase
            x1=x+math.sin(angle)*r
            y1=y-math.cos(angle)*r
            bullets.append(CircleBullet1(AttackPattern1.v*math.sin(angle),-math.cos(angle)*AttackPattern1.v,x1,y1))
            
def next_boss(number):
    try:
        x,y,r=boss[number]
        targets.append(Boss(x,y,r))
        set_music(boss_music[number])
    except:
        game_over()
font_name=pygame.font.match_font('arial')
def draw_text(text,c,size,color=(0,0,0)):
    font=pygame.font.Font(pygame.font.match_font('arial'),size)
    text_surface=font.render(text,True,color)
    text_rect=text_surface.get_rect()
    text_rect.center=c
    screen.blit(text_surface,text_rect)
def rnd(x,y):
    return random.randint(x,y)
def set_music(track):
    pygame.mixer.music.load(track)
    pygame.mixer.music.play(loops=-1)
def end_music():
    pygame.mixer.music.unload()
def game_over():
    global finished
    screen.fill(BLACK)
    draw_text("GAME OVER",(WIDTH/2,HEIGHT/2),WIDTH//10,RED)
    pygame.display.update()
    pygame.time.delay(1000)
    finished=True
    
pygame.init()
pygame.mixer.init()
gunshot_normal_sound=pygame.mixer.Sound('normal_shot.mp3')
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []
bullets = []
targets = []
boss_music = 6*['March_of_the_Defenders.mp3']
boss = 6*[(WIDTH/2,HEIGHT*1/5,WIDTH/10)]

clock = pygame.time.Clock()
gun = Gun(screen)
target = Target()
targets.append(target)
target = Target()
targets.append(target)
finished = False
winner = False
total_count = 0
shot_count = 0
next1=0
while not finished:
    screen.fill(WHITE)
    gun.draw()
    done=True
    for target in targets:
        if target.live:
            target.draw()
            done=False
    for bullet in bullets:
        bullet.draw()
    for b in balls:
        b.draw()
    draw_text(f'{total_count}',(10,10),18)  
    pygame.display.update()
    if done:
        end_music()
        balls = []
        draw_text(f'Вы уничтожили цель за {shot_count} выстрелов!',(WIDTH/2,HEIGHT/2),WIDTH//39)
        shot_count = 0
        pygame.display.update()
        pygame.time.delay(1000)
        done=False
        if next1%2==0:
            next_boss(next1//2-1)
            next1+=1
        else:
            for target in targets:
                if type(target) is type(Boss()):
                    targets.remove(target)
                else:
                    target.new_target()
            next1+=1
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button==1 and not gun.cooldown:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP and gun.f2_on:
            gun.fire2_end(event)
            shot_count+=1
    for target in targets:
        target.move()
        target.attack()
        for b in balls:
            if b.hittest(target) and target.live:
                total_count += 1
                target.hit(b)
    for b in balls:
        b.do_you_want_to_die()
        b.move()
        for target in targets:
            if b.hittest(target) and target.live:
                total_count += 1
                target.hit(b)
        for bullet in bullets:
            if bullet.ball_hittest(b):
                bullet.hit_ball(b)
    for bullet in bullets:
        bullet.move()
        if bullet.tank_hittest():
            bullet.hit_tank()
    gun.move()
    gun.targetting(list(pygame.mouse.get_pos()))
    gun.cooling()
    gun.power_up()

pygame.quit()
