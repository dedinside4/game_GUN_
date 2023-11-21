import math
from random import choice
import random
import pygame
from scipy.optimize import root_scalar
import spellcards
import bullet_types
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
    def __init__(self, x, y,r=9):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.speed_loss=0.5
        self.screen = screen
        self.x = x
        self.y = y
        self.r = r
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 1
        self.gy = -0.15
        self.killtime=pygame.time.get_ticks()+230000
        self.density=0.8/(9**3)
        self.std=1/7
        self.mindamage = self.density*(self.r**3)*(1-self.std)
        self.maxdamage = self.density*(self.r**3)*(1+self.std)
        #print(self.mindamage,self.maxdamage)
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
            self.vx*=-(1-self.speed_loss)
            self.vy*=1-self.speed_loss*0.2
            if abs(self.vx)<0.5:
                self.vx=0
        if self.x<self.r:
            self.x = self.r
            self.vx*=-(1-self.speed_loss)
            self.vy*=1-self.speed_loss*0.2
            if abs(self.vx)<0.5:
                self.vx=0
        if self.y>=HEIGHT - self.r:
            self.y = HEIGHT - self.r
            self.vy*=-(1-self.speed_loss)
            self.vx*=1-self.speed_loss*0.2
            if abs(self.vy)<0.5 and self.gy<0:
                self.vy=0
                self.gy=0
                self.killtime=pygame.time.get_ticks()
        if self.y<self.r:
            self.y = self.r
            self.vy*=-(1-self.speed_loss)
            self.vx*=1-self.speed_loss*0.2
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
        x,y,r=obj
        collision = False
        if (x-self.x)**2+(y-self.y)**2<=(self.r + r)**2:
            collision=True
        return collision
    def do_you_want_to_die(self):
        if pygame.time.get_ticks()-self.killtime>=100:
            balls.remove(self)
class Stick:
    def __init__ (self,x,y,an,v,v1):
        self.x=x
        self.y=y
        self.length = WIDTH/10
        self.an=an
        self.v=v
        self.edge=(self.x+math.sin(self.an)*self.length,self.y-math.cos(self.an)*self.length)
        self.vx=v * math.sin(self.an)+v1
        self.vy = - v * math.cos(self.an)
        self.color = choice(GAME_COLORS)
        self.density=0.15/(9**3)
        self.std=1/7
        self.mindamage = self.density*(5*self.length*5)*(1-self.std)
        self.maxdamage = self.density*(5*self.length*5)*(1+self.std)
        self.live=1
        self.killtime=pygame.time.get_ticks()+230000
    def move(self):
        self.x+=self.vx
        self.y+=self.vy
        self.edge=(self.x+math.sin(self.an)*self.length,self.y-math.cos(self.an)*self.length)
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
        x1,y1,r=obj
        x,y=self.edge
        collision = False
        if (x-x1)**2+(y-y1)**2<=r**2:
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
        self.bombing=False
        self.spellcard=None
        self.spellcard_count=3
        self.spell_name='Bouncy Hell'
        self.inverted=False
    def get_rect(self):
        if not self.inverted:
            self.rect = pygame.Rect(self.x-self.left,self.y,2*self.left,self.bottom)
        else:
            self.rect = pygame.Rect(self.x-self.bottom,self.y-self.left,self.bottom,2*self.left)
        #pygame.draw.rect(screen,RED,self.rect)
    def get_hitbox(self):
        b=self.b
        k=self.left/self.bottom/2
        a=b/k
        if not self.inverted:
            rect=pygame.Rect(self.x-a,self.y+self.bottom/2-b,2*a,2*b)
        else:
            rect=pygame.Rect(self.x-self.bottom/2-b,self.y-a,2*b,2*a)
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
    def bomb(self):
        if not self.bombing and self.spellcard_count>0:
            self.bombing=True
            self.got_invincible=pygame.time.get_ticks()
            self.invincible=True
            self.spellcard=spellcards.Bomb1(self)
            self.spellcard_count-=1
    def fire_start(self, event):
        if self.fire_type is None:
            if event.button==1:
                self.fire1_start()
                self.fire_type=1
            elif event.button==3:
                self.fire3_start()
                self.fire_type=3
    def fire_end(self, event):
        if event.button==self.fire_type and not self.cooldown:
            exec(f'self.fire{event.button}_end()')
    def fire3_start(self):
        self.f2_on = 1
    def fire1_start(self):
        self.f2_on = 1
    def fire1_end(self):
        global balls
        new_ball = Ball(self.x,self.y)
        #self.an = math.atan2((event.pos[0] - new_ball.x), (new_ball.y - event.pos[1]))
        if self.inverted:
            vx=0
            vy=self.v
        else:
            vy=0
            vx=self.v
        new_ball.vx = self.f2_power * math.sin(self.an)*0.7+vx
        new_ball.vy = - self.f2_power * math.cos(self.an)*0.7+vy
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
        if not self.invincible or self.bombing:
            self.get_rect()
            pygame.draw.line(screen, self.color, (self.x,self.y),(self.x+math.sin(self.an)*self.f2_power,self.y-math.cos(self.an)*self.f2_power), width=5)
            pygame.draw.ellipse(screen, self.tank_color, self.rect)
        elif ((pygame.time.get_ticks()-self.got_invincible)//150)%2==0:
            self.get_rect()
            pygame.draw.line(screen, self.color, (self.x,self.y),(self.x+math.sin(self.an)*self.f2_power,self.y-math.cos(self.an)*self.f2_power), width=5)
            pygame.draw.ellipse(screen, self.tank_color, self.rect)
        elif pygame.time.get_ticks()-self.got_invincible>=self.invincible_time and not self.bombing:
            self.invincible=False
    def power_up(self):
        if self.bombing:
            stop=self.spellcard.activate(balls,Ball)
            if stop:
                self.bombing=False
                self.invincible=False
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
            self.live-=1
            self.spellcard_count=3
            if self.live==0:
                self.deadend()
            explosion_waves.append(ExplosionWave(self.x,self.y))
            play_death_sound()
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
        if not self.inverted:
            self.x+=self.v
        else:
            self.y+=self.v
        if self.x<self.left:
            self.x=self.left
        elif self.x>WIDTH-self.right:
            self.x=WIDTH-self.right
        if self.y<HEIGHT*2/5:
            self.y=HEIGHT*2/5
        elif self.y>HEIGHT-self.left and self.inverted:
            self.y=HEIGHT-self.left
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
class EvilGun(Gun):
    def __init__(self, screen, x, y):
        Gun.__init__(self,screen,x,y)
        self.trigger=(x,y)
        self.trigger_speed=4
        self.g=0.15
        self.vy=0
        self.landed=False
        self.live=4
        self.speed_factor=0.5
    def fall(self):
        if not self.landed or self.y<HEIGHT-WIDTH/30:
            self.vy+=self.g
            self.y+=self.vy
            if self.y>=HEIGHT-WIDTH/30:
                self.y=HEIGHT-WIDTH/30
                self.landed=True
    def get_hit_tank(self):
        dead=False
        if gun.x-gun.left>=self.x and gun.x-gun.left<=self.x+self.left:
            gun.get_hit()
            if not self.invincible:
                self.live-=1
                self.invincible=True
                self.got_invincible=pygame.time.get_ticks()
                if self.live==0:
                    dead=True
                    self.dead_end()
                play_death_sound()
            gun.x=self.x+self.left+gun.left
        elif gun.x+gun.left<=self.x and gun.x+gun.left>=self.x-self.left:
            gun.get_hit()
            if not self.invincible:
                self.live-=1
                self.invincible=True
                self.got_invincible=pygame.time.get_ticks()
                if self.live==0:
                    dead=True
                    self.dead_end()
                play_death_sound()
            gun.x=self.x-self.left-gun.left
        return dead
    def get_hit(self):
        if pygame.time.get_ticks()-self.got_invincible>=self.invincible_time:
            self.invincible=False
        dead=False
        if not self.invincible:
            for ball in balls:
                if ball.hittest((self.x,self.y+self.bottom/2,self.bottom/2)):
                    self.live-=1
                    self.invincible=True
                    self.got_invincible=pygame.time.get_ticks()
                    if self.live==0:
                        dead=True
                        self.dead_end()
                    play_death_sound()
        return dead
    def dead_end(self):
        global evilgun
        evilgun=None
        explosion_waves.append(ExplosionWave(self.x,self.y))
    def targetting(self):
        """Прицеливание. Зависит от положения мыши."""
        x,y=self.trigger
        try:
            self.an = math.atan2((x - self.x), (self.y - y))
        except:
            self.an = -math.pi/2
        if self.f2_on:
            self.color = RED
        #print(self.an)
    def update_trigger(self):
        x,y=self.trigger
        an = math.atan2((gun.x - x), (y - gun.y))
        x+=self.trigger_speed*math.sin(an)
        y+=-self.trigger_speed*math.cos(an)
        if gun.x - x<=10:
            x=gun.x
        if gun.y - y<=10:
            y=gun.y
        self.trigger=(x,y)
        #print(self.trigger,(gun.x,gun.y))
    def fire_start(self):
        an1 = math.atan2((gun.x - self.x), (self.y - gun.y-gun.bottom))
        an2 = math.atan2((gun.x - self.x), (self.y - gun.y+gun.top))
        #print(an1,an2,self.an)
        if ((an1>an2 and self.an<=an1 and self.an>=an2) or (an2>an1 and self.an<=an2 and self.an>=an1)) and not self.cooldown:
            #print('started',self.y)
            self.f2_on = 1
    def fire_end(self):
        new_ball = Ball(self.x,self.y)
        #self.an = math.atan2((event.pos[0] - new_ball.x), (new_ball.y - event.pos[1]))
        vx = self.f2_power * math.sin(self.an)*0.7*self.speed_factor+self.v
        vy = - self.f2_power * math.cos(self.an)*0.7*self.speed_factor
        new_bullet = bullet_types.CircleBullet1(vx,vy,self.x,self.y,9)
        bullets.append(new_bullet)
        self.f2_on = 0
        self.f2_power = WIDTH/60
        self.cooldown=True
        self.cooldown_time=5000
        self.last_shot=pygame.time.get_ticks()
        pygame.mixer.Sound('normal_shot.mp3').play()
    def power_up(self):
        if self.f2_on:
            if self.f2_power < WIDTH/20:
                self.f2_power += WIDTH/(60*FPS*1)
                if self.f2_power>=WIDTH/20:
                    self.fire_end()
            self.color = RED
class ExplosionWave:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.r=0
        self.color=YELLOW
    def grow(self):
        self.r+=HEIGHT/(120*0.6)
        if self.r**2>3*WIDTH**2+3*HEIGHT**2:
            explosion_waves.remove(self)
    def annihilate(self):
        for bullet in bullets:
            if (bullet.x-self.x)**2 + (bullet.y-self.y)**2<=self.r**2 and not bullet.indestructible:
                bullets.remove(bullet)
                bullet.killed=True
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
        draw_text(self.name,(WIDTH/10,HEIGHT/70),WIDTH//39)
    def move(self):
        pass
    def hit(self,ball):
        an_ball=math.atan2((ball.x-self.x),(self.y-ball.y))
        an_speed=math.atan2(ball.vx,-ball.vy)
        v=-math.sqrt(ball.vy**2+ball.vx**2)*math.cos(an_speed-an_ball)
        mindamage=ball.mindamage*v
        maxdamage=ball.maxdamage*v
        random.random()*(maxdamage-mindamage)
        self.live-=mindamage+random.random()*(maxdamage-mindamage)
        balls.remove(ball)
        if self.live<=0:
            self.next_attack()
    def attack(self):
        for attack in self.attack_patterns:
            attack.activate(bullets)
    def next_attack(self):
        global evilgun
        evilgun=None
        for attack in self.attack_patterns:
            attack.clear(bullets)
        try:
            if self.order>0:
                explosion_waves.append(ExplosionWave(self.x,self.y))
            exec('self.'+self.pull[self.order]+'()')
            self.order+=1
        except Exception as e:
            #self.live=0
            print(e)
class Boss2(Boss):
    def __init__(self,x=WIDTH/2,y=HEIGHT*1/5,r=WIDTH/10):
        Boss.__init__(self,x,y,r)
        self.pull=['attack_1','spellcard_1','attack_2','spellcard_2']
        self.order=0
        self.attack_patterns=[]
        self.name='Ball 1'
        self.spell_name=''
    def attack_1(self):
        self.attack_patterns=[]
        self.spell_name=''
        self.live=70
        self.max_live=70
        self.attack_patterns.append(spellcards.AttackPattern1(self.x,self.y,WIDTH/8,0.3,20,25,4,HEIGHT/100,10000))
    def spellcard_1(self):
        self.attack_patterns=[]
        self.spell_name='Kamikaze Drones'
        self.live=70
        self.max_live=70
        self.attack_patterns.append(spellcards.SpellCard1(gun,self.x,self.y))
    def attack_2(self):
        self.attack_patterns=[]
        self.spell_name=''
        self.live=70
        self.max_live=70
        self.attack_patterns.append(spellcards.AttackPattern3(self.x,self.y,WIDTH/8,1,15,6,0.0085,HEIGHT/50,15000))
    def spellcard_2(self):
        global evilgun
        self.attack_patterns=[]
        self.spell_name='The Tank Has Landed'
        self.live=70
        self.max_live=70
        evilgun=EvilGun(screen,self.x,self.y)
        self.attack_patterns.append(spellcards.AttackPattern2(self.x,self.y,0.4,6,(WIDTH/40,WIDTH/30,WIDTH/80),gun))
        self.attack_patterns.append(spellcards.SpellCard2(evilgun))    
class Boss1(Boss):
    def __init__(self,x=WIDTH/2,y=HEIGHT*1/5,r=WIDTH/10):
        Boss.__init__(self,x,y,r)
        self.pull=['spellcard_2','spellcard_1','spellcard_3','spellcard_4']
        self.order=0
        self.attack_patterns=[]
        self.name='Ball 2'
        self.spell_name=''
    def spellcard_1(self):
        self.attack_patterns=[]
        self.spell_name='Inviolable Border'
        self.live=70
        self.max_live=70
        self.attack_patterns.append(spellcards.AttackPattern2(self.x,self.y,0.7,7,(WIDTH/60,WIDTH/30,WIDTH/80),gun))
        self.attack_patterns.append(spellcards.SpellCard3(gun))
    def spellcard_2(self):
        self.attack_patterns=[]
        self.spell_name='Anomaly: Rotated Space'
        self.live=70
        self.max_live=70
        self.attack_patterns.append(spellcards.SpellCard4(gun))
            
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
def draw_lives():
    for i in range(0,gun.live-1):
        pygame.draw.circle(screen, MAGENTA, (WIDTH-WIDTH/7-7*WIDTH/80+i*WIDTH/40,HEIGHT/14), WIDTH/90)
    for i in range(gun.live-1,8):
        pygame.draw.circle(screen, BLACK, (WIDTH-WIDTH/7-7*WIDTH/80+i*WIDTH/40,HEIGHT/14), WIDTH/90)
    #draw_text('Lives', (WIDTH-WIDTH/7,HEIGHT/30), WIDTH//30, BLACK)
def draw_bombs():
    for i in range(0,gun.spellcard_count):
        pygame.draw.circle(screen, GREEN, (WIDTH-WIDTH/7-7*WIDTH/80+i*WIDTH/40,HEIGHT/10), WIDTH/90)
    for i in range(gun.spellcard_count,8):
        pygame.draw.circle(screen, BLACK, (WIDTH-WIDTH/7-7*WIDTH/80+i*WIDTH/40,HEIGHT/10), WIDTH/90)
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
def play_death_sound():
    death_sound=pygame.mixer.Sound('tank_explosion.mp3')
    death_sound.play()
    death_sound.fadeout(2500)
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
explosion_waves=[]
gun = Gun(screen)
target = Target()
targets.append(target)
target = Target()
targets.append(target)
finished = False
winner = False
evilgun=None
total_count = 0
shot_count = 0
next1=0
boss_number=1
while not finished:
    screen.fill(WHITE)
    gun.draw()
    try:
        evilgun.draw()
    except:
        pass
    gun.get_hitbox()
    done=True
    for target in targets:
        if target.live:
            target.draw()
            done=False
        if type(target)==type(eval(f'Boss{boss_number}()')):
            draw_health_bar(target)
            draw_text(target.spell_name, (WIDTH-WIDTH/7,HEIGHT/30), WIDTH//30, BLACK)
    for bullet in bullets:
        bullet.draw(screen)
    for b in balls:
        b.draw()
    for wave in explosion_waves:
        wave.draw()
    if gun.bombing:
        draw_text(gun.spell_name,(WIDTH/7,HEIGHT-HEIGHT/30), WIDTH//30, BLACK)
    draw_lives()
    draw_bombs()
    #draw_text(f'{total_count}',(10,10),18)  
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
        elif event.type == pygame.KEYDOWN and event.key==pygame.K_s:
            gun.bomb()
            
    for target in targets:
        target.move()
        target.attack()
        for b in balls:
            if b.hittest((target.x,target.y,target.r)) and target.live:
                total_count += 1
                target.hit(b)
    for b in balls:
        b.do_you_want_to_die()
        b.move()
        for target in targets:
            if b.hittest((target.x,target.y,target.r)) and target.live:
                total_count += 1
                target.hit(b)
        for bullet in bullets:
            if bullet.ball_hittest(b):
                bullet.hit_ball(b,bullets)
    for bullet in bullets:
        bullet.move(bullets)
        if bullet.tank_hittest(gun):
            bullet.hit_tank(bullets,gun)
    for wave in explosion_waves:
        wave.grow()
        wave.annihilate()
    gun.move()
    gun.targetting(list(pygame.mouse.get_pos()))
    gun.cooling()
    gun.power_up()

pygame.quit()
