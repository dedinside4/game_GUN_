import math
from random import choice
import random
import pygame
from scipy.optimize import root_scalar

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
        self.mindamage = 0.03
        self.maxdamage = 0.04
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
class Stick:
    def __init__ (self,x,y,an,v,v1):
        self.x=x
        self.y=y
        self.lenght = WIDTH/10
        self.an=an
        self.v=v
        self.edge=(self.x+math.sin(self.an)*self.lenght,self.y-math.cos(self.an)*self.lenght)
        self.vx=v * math.sin(self.an)+v1
        self.vy = - v * math.cos(self.an)
        self.color = choice(GAME_COLORS)
        self.mindamage = 0.0045
        self.maxdamage = 0.0055
        self.live=1
        self.killtime=pygame.time.get_ticks()+230000
    def move(self):
        self.x+=self.vx
        self.y+=self.vy
        self.edge=(self.x+math.sin(self.an)*self.lenght,self.y-math.cos(self.an)*self.lenght)
        x,y=self.edge
        if self.v>0 and x>WIDTH:
            self.vx=0
            self.vy=0
            self.v=0
            self.killtime=pygame.time.get_ticks()
        elif self.v>0 and  x<0:
            self.vx=0
            self.vy=0
            self.v=0
            self.killtime=pygame.time.get_ticks()
        elif self.v>0 and  y>HEIGHT:
            self.vx=0
            self.vy=0
            self.v=0
            self.killtime=pygame.time.get_ticks()
        elif self.v>0 and y<0:
            self.vx=0
            self.vy=0
            self.v=0
            self.killtime=pygame.time.get_ticks()
    def do_you_want_to_die(self):
        if pygame.time.get_ticks()-self.killtime>=300:
            balls.remove(self)
    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        x,y=self.edge
        collision = False
        if (x-obj.x)**2+(y-obj.y)**2<=obj.r**2:
            collision=True
        return collision
    def draw(self):
        pygame.draw.line(screen, self.color, (self.x,self.y),self.edge, width=5)
        
        
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
        self.b=float(root_scalar(self.find_ellipse, bracket=[0, self.left]).root)
        self.hitbox=None
        self.fire_type=None
    def get_rect(self):
        self.rect = pygame.Rect(self.x-self.left,self.y,2*self.left,self.bottom)
        #pygame.draw.rect(screen,RED,self.rect)
    def get_hitbox(self):
        b=self.b
        k=self.left/self.bottom/2
        a=b/k
        rect=pygame.Rect(self.x-a,self.y+self.bottom/2-b,2*a,2*b)
        self.hitbox=rect
        keystate=pygame.key.get_pressed()
        if keystate[pygame.K_LSHIFT]:
            pygame.draw.rect(screen,RED,rect)
    def find_ellipse(self,b2):
        a1=self.left
        b1=self.bottom/2
        k=a1/b1
        c=math.sqrt(a1**2-b1**2)
        f=math.sqrt(b2**2+(k*b2-c)**2)+math.sqrt(b2**2+(k*b2+c)**2)-2*k*b1
        return f
    def fire_start(self, event):
        if self.fire_type is None:
            if event.button==1:
                self.fire1_start()
                self.fire_type=1
            elif event.button==3:
                self.fire3_start()
                self.fire_type=3
    def fire_end(self, event):
        if event.button==self.fire_type:
            exec(f'self.fire{event.button}_end()')
    def fire3_start(self):
        self.f2_on = 1
    def fire1_start(self):
        self.f2_on = 1
    def fire1_end(self):
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
        self.cooldown_time=5000
        self.last_shot=pygame.time.get_ticks()
        gunshot_normal_sound.play()
        self.fire_type=None
    def fire3_end(self):
        self.cooldown=True
        self.cooldown_time=7000+1537
        self.last_shot=pygame.time.get_ticks()
        gunshot_stick_sound.play()
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
        if not self.invincible:
            self.get_rect()
            pygame.draw.line(screen, self.color, (self.x,self.y),(self.x+math.sin(self.an)*self.f2_power,self.y-math.cos(self.an)*self.f2_power), width=5)
            pygame.draw.ellipse(screen, self.tank_color, self.rect)
        elif ((pygame.time.get_ticks()-self.got_invincible)//150)%2==0:
            self.get_rect()
            pygame.draw.line(screen, self.color, (self.x,self.y),(self.x+math.sin(self.an)*self.f2_power,self.y-math.cos(self.an)*self.f2_power), width=5)
            pygame.draw.ellipse(screen, self.tank_color, self.rect)
        elif pygame.time.get_ticks()-self.got_invincible>=self.invincible_time:
            self.invincible=False
    def power_up(self):
        if self.f2_on:
            if self.f2_power < WIDTH/20 and not self.cooldown:
                self.f2_power += WIDTH/(60*FPS*1)
            elif self.cooldown and pygame.time.get_ticks()- self.last_shot>=1537:
                new_stick = Stick(self.x,self.y,self.an,self.f2_power*2,self.v)
                balls.append(new_stick)
                self.f2_on = 0
                self.f2_power = WIDTH/60
                self.fire_type=None
                gunshot_stick_sound.fadeout(5151)
            self.color = RED
    def get_hit(self):
        if pygame.time.get_ticks()-self.got_invincible>=self.invincible_time:
            self.invincible=False
        if not self.invincible:
            global bullets
            self.live-=1
            if self.live==0:
                self.deadend()
            explosion_wave.activate(self.x,self.y)
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
class ExplosionWave:
    def __init__(self):
        self.active=False
        self.x=None
        self.y=None
        self.r=0
        self.color=YELLOW
    def activate(self,x,y):
        self.active=True
        self.x=x
        self.y=y
        self.r=0
        death_sound.play()
        death_sound.fadeout(2500)
    def grow(self):
        self.r+=HEIGHT/(120*0.6)
        if self.r**2>WIDTH**2+HEIGHT**2:
            self.active=False
    def annihilate(self):
        for bullet in bullets:
            if (bullet.x-self.x)**2 + (bullet.y-self.y)**2<=self.r**2:
                bullets.remove(bullet)
    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x,self.y),self.r,width=int(WIDTH/19))
    
        
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
    def __init__(self,vx,vy,x,y,r=HEIGHT/100):
        Bullet.__init__(self,vx,vy,x,y)
        self.r=r
        self.color=RED
        self.rect=self.x-self.r/math.sqrt(2),self.y-self.r/math.sqrt(2),self.r/math.sqrt(8),self.r/math.sqrt(8)
    def ball_hittest(self,obj):
##        collision = False
##        if (obj.x-self.x)**2+(obj.y-self.y)**2<=(self.r + obj.r)**2:
##            collision=True
##        return collision
        return obj.hittest(self)
    def get_rect(self):
        self.rect=pygame.Rect(self.x-self.r/math.sqrt(2),self.y-self.r/math.sqrt(2),self.r/math.sqrt(8),self.r/math.sqrt(8))
    def tank_hittest(self):
        self.get_rect()
        collision=self.rect.colliderect(gun.hitbox)
        return collision
    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x,self.y), self.r) 
        
class Boss:
    def __init__(self,x=WIDTH/2,y=HEIGHT*1/5,r=WIDTH/10):
        self.x=x
        self.y=y
        self.r=r
        self.color=RED
        self.live=None
        self.attack_pattern=None
        self.max_live=None
        #self.pattern=1
    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x,self.y), self.r)
    def move(self):
        pass
    def hit(self,ball):
        pass
        an=math.atan((ball.x-self.x)/(ball.y-self.y))
        v=-ball.vy*math.cos(an)-ball.vx*math.sin(an)
        mindamage=int(ball.mindamage*v**2)
        maxdamage=int(ball.maxdamage*v**2)
        self.live-=random.randint(mindamage,maxdamage)
        balls.remove(ball)
        if self.live<=0:
            self.next_attack()      
class Boss1(Boss):
    def __init__(self,x=WIDTH/2,y=HEIGHT*1/5,r=WIDTH/10):
        Boss.__init__(self,x,y,r)
        self.pull=['attack_1','spellcard_1','attack_2','spellcard_2']
        self.order=0
        self.attack_pattern=None
    def attack(self):
        self.attack_pattern.activate()
    def next_attack(self):
        try:
            exec('self.'+self.pull[self.order]+'()')
            self.order+=1
        except:
            self.live=0
    def attack_1(self):
        self.live=50
        self.max_live=50
        self.attack_pattern=AttackPattern1(self.x,self.y,WIDTH/8,0.2,20,25,4,HEIGHT/100)
    def spellcard_1(self):
        self.live=50
        self.max_live=50
        self.attack_pattern=AttackPattern1(self.x,self.y,WIDTH/8,0.3,20,25,4,HEIGHT/100)
    def attack_2(self):
        self.live=50
        self.max_live=50
        self.attack_pattern=AttackPattern1(self.x,self.y,WIDTH/8,1.3,7,10,5,HEIGHT/20)
    def spellcard_2(self):
        self.live=50
        self.max_live=50
        self.attack_pattern=AttackPattern1(self.x,self.y,WIDTH/8,0.8,10,15,5,HEIGHT/40)
        
        
    
class AttackPattern1:
    def __init__(self,x,y,r,period,count1,count2,v,size):
        self.first_delay=2000
        self.last_shot=pygame.time.get_ticks()+self.first_delay
        self.delay=period*1000
        self.v=v
        self.count=random.randint(count1,count2)
        self.phase=random.random()*2*math.pi/self.count
        self.x=x
        self.y=y
        self.r=r
        self.size=size
    def activate(self):
        if pygame.time.get_ticks() - self.last_shot>=self.delay:
            self.phase=random.random()*2*math.pi/self.count
            self.scatter()
            self.last_shot=pygame.time.get_ticks()
    def scatter(self):
        global bullets
        for i in range(0,self.count):
            angle=i*2*math.pi/self.count+self.phase
            x1=self.x+math.sin(angle)*self.r
            y1=self.y-math.cos(angle)*self.r
            bullets.append(CircleBullet1(self.v*math.sin(angle),-math.cos(angle)*self.v,x1,y1,self.size))
            
def next_boss(number):
    try:
        print(number)
        b=eval('Boss'+str(number)+'()')
        b.next_attack()
        targets.append(b)
        #set_music(boss_music[number])
    except:
        game_over()
font_name=pygame.font.match_font('arial')
def draw_health_bar(boss):
    k=max(0,boss.live/boss.max_live)
    pygame.draw.line(screen, BLACK, (WIDTH/60,HEIGHT/30),(WIDTH-WIDTH/60,HEIGHT/30), width=5)
    pygame.draw.line(screen, RED, (WIDTH/60,HEIGHT/30),(WIDTH/60+(WIDTH-WIDTH/30)*k,HEIGHT/30), width=5)
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
gunshot_stick_sound=pygame.mixer.Sound('railgun_shot.mp3')
gunshot_normal_sound.set_volume(0.8)
death_sound=pygame.mixer.Sound('tank_explosion.mp3')
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []
bullets = []
targets = []
boss_music = []
boss = 6*[(WIDTH/2,HEIGHT*1/5,WIDTH/10)]

clock = pygame.time.Clock()
explosion_wave=ExplosionWave()
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
boss_number=1
while not finished:
    screen.fill(WHITE)
    gun.draw()
    gun.get_hitbox()
    done=True
    for target in targets:
        if target.live:
            target.draw()
            done=False
        if type(target)==type(eval(f'Boss{boss_number}()')):
            draw_health_bar(target)
    for bullet in bullets:
        bullet.draw()
    for b in balls:
        b.draw()
    if explosion_wave.active:
        explosion_wave.draw()
        explosion_wave.grow()
        explosion_wave.annihilate()
    draw_text(f'{total_count}',(10,10),18)  
    pygame.display.update()
    if done:
        #end_music()
        balls = []
        draw_text(f'Вы уничтожили цель за {shot_count} выстрелов!',(WIDTH/2,HEIGHT/2),WIDTH//39)
        shot_count = 0
        pygame.display.update()
        pygame.time.delay(1000)
        done=False
        if next1%2==0:
            next_boss(boss_number)
            next1+=1
        else:
            for target in targets:
                if type(target) is type(eval(f'Boss{boss_number}()')):
                    boss_number+=1
                    targets.remove(target)
                else:
                    target.new_target()
            next1+=1
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN and not gun.cooldown:
            gun.fire_start(event)
        elif event.type == pygame.MOUSEBUTTONUP and gun.f2_on:
            gun.fire_end(event)
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
