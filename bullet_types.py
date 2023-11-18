import pygame
import random
import math
from scipy.optimize import root_scalar
from scipy.optimize import minimize
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
class Bullet:
    def __init__(self,vx,vy,x,y,lifetime):
        self.vy=vy
        self.vx=vx
        self.x=x
        self.y=y
        self.lifetime=lifetime
        self.birthtime=pygame.time.get_ticks()
        self.killed=False
    def hit_ball(self,ball,bullets):
        bullets.remove(self)
        self.killed=True
    def hit_tank(self,bullets,gun):
        try:
            bullets.remove(self)
            gun.get_hit()
            self.killed=True
        except:
            pass

    def move(self,bullets):
        self.x+=self.vx
        self.y+=self.vy
        if self.x>2*WIDTH or self.x<-WIDTH or self.y>2*HEIGHT or self.y<-HEIGHT or pygame.time.get_ticks()-self.birthtime>=self.lifetime:
            try:
                bullets.remove(self)
            except:
                pass
class CircleBullet1(Bullet):
    def __init__(self,vx,vy,x,y,r,lifetime=20000,color=RED):
        Bullet.__init__(self,vx,vy,x,y,lifetime)
        self.r=r
        self.color=color
        self.rect=pygame.Rect(self.x-self.r/math.sqrt(2),self.y-self.r/math.sqrt(2),2*self.r/math.sqrt(2),2*self.r/math.sqrt(2))
        self.killed=False
    def ball_hittest(self,obj):
        return obj.hittest((self.x,self.y,self.r))
    def get_rect(self):
        self.rect=pygame.Rect(self.x-self.r/math.sqrt(2),self.y-self.r/math.sqrt(2),2*self.r/math.sqrt(2),2*self.r/math.sqrt(2))
    def tank_hittest(self,gun):
        self.get_rect()
        collision=self.rect.colliderect(gun.hitbox)
        return collision
    def draw(self,screen):
        pygame.draw.circle(screen, self.color, (self.x,self.y), self.r)
class ArrowBullet1(Bullet):
    def __init__(self,v,angle,x,y,l,h1,h2,color=MAGENTA,lifetime=20000):
        self.v=v
        self.an=angle
        self.get_speed()
        Bullet.__init__(self,self.vx,self.vy,x,y,lifetime)
        self.x=x
        self.y=y
        self.l=l
        self.h1=h1
        self.h2=h2
        self.r1=2*l*(l**2+h2**2)/(4*l*h2)
        self.r2=l*h2/(l+math.sqrt(l**2+h2**2))
        self.h3=math.sqrt(self.r1**2-l**2)
        self.color=color
        self.edge=(self.x+self.h2*math.sin(self.an),self.y-self.h2*math.cos(self.an))
        self.rect=None
    def get_speed(self):
        self.vy=-self.v*math.cos(self.an)
        self.vx=self.v*math.sin(self.an)
    def get_rect(self):
        x=self.x+self.r2*math.sin(self.an)
        y=self.y-self.r2*math.cos(self.an)
        self.rect=pygame.Rect(x-self.r2,y-self.r2,2*self.r2,2*self.r2)
    def tank_hittest(self,gun):
        self.get_rect()
        collision=self.rect.colliderect(gun.hitbox)
        return collision
    def ball_hittest(self,obj):
        x=self.x+self.h3*math.sin(self.an)
        y=self.y-self.h3*math.cos(self.an)
        collision=obj.hittest((x,y,self.r1))
        if collision:
            self.killed=True
        return collision
    def draw(self,screen):
        x1=self.x-self.l*math.cos(self.an)
        y1=self.y-self.l*math.sin(self.an)
        x2=self.x+self.h1*math.sin(self.an)
        y2=self.y-self.h1*math.cos(self.an)
        x3=self.x+self.l*math.cos(self.an)
        y3=self.y+self.l*math.sin(self.an)
        x4=self.x+self.h3*math.sin(self.an)
        y4=self.y-self.h3*math.cos(self.an)
        self.edge=(self.x+self.h2*math.sin(self.an),self.y-self.h2*math.cos(self.an))
        #pygame.draw.circle(screen, YELLOW, (x4,y4), self.r1)
        pygame.draw.polygon(screen,self.color,((x1,y1),(x2,y2),(x3,y3),self.edge))
        #pygame.draw.rect(screen,RED,self.rect)
