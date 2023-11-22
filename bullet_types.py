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
        self.indestructible=False
        self.disturbed=False
    def hit_ball(self,ball,bullets):
        if not self.indestructible:
            bullets.remove(self)
            self.killed=True
        elif not self.disturbed:
            self.disturbed=True
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
        if self.x>13*WIDTH or self.x<-13*WIDTH or self.y>13*HEIGHT or self.y<-13*HEIGHT or pygame.time.get_ticks()-self.birthtime>=self.lifetime:
            try:
                bullets.remove(self)
            except:
                pass
    def tank_hittest(self,gun):
        self.get_rect()
        collision=self.rect.colliderect(gun.hitbox)
        return collision
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
class Train(Bullet):
    def __init__(self,v,direction,y,count,delay,color=BLACK,lifetime=4000):
        self.vx=v*direction
        self.direction=direction
        offset=(delay/1000*120)*v
        self.x=(-offset if direction==1 else WIDTH+offset)
        self.color=color
        self.height=HEIGHT/40
        self.y=y-self.height/2
        self.count=count
        self.wagon_length=WIDTH/7
        self.cord_length=self.wagon_length/24
        self.length=self.wagon_length*count+self.cord_length*(count-1)
        Bullet.__init__(self,self.vx,0,self.x,self.y,lifetime)
    def get_rect(self):
        x=min(self.x,self.x-self.direction*self.length)
        self.rect=pygame.Rect(x,self.y-self.height/2,self.length,self.height)
    def ball_hittest(self,obj):
        x=self.x-self.wagon_length*self.direction/2
        for i in range(0,self.count):
            collision=obj.hittest((x-i*(self.wagon_length+self.cord_length)*self.direction-self.wagon_length/2,self.y-self.height/2,self.wagon_length,self.height))
            if collision:
                break
        return collision
    def draw(self,screen):
        x=self.x-self.wagon_length*self.direction/2
        #pygame.draw.rect(screen,RED,self.rect)
        for i in range(0,self.count):
            pygame.draw.rect(screen,self.color,(x-i*(self.wagon_length+self.cord_length)*self.direction-self.wagon_length/2,self.y-self.height/2,self.wagon_length,self.height))
            if i<self.count-1:
                pygame.draw.line(screen,self.color,(x-(i*(self.wagon_length+self.cord_length)+self.wagon_length/2)*self.direction,self.y+self.height/3),(x-(i*(self.wagon_length+self.cord_length)+self.wagon_length/2+self.cord_length)*self.direction,self.y+self.height/3),width=3)
            elif i==0:
                pygame.draw.line(screen,self.color,(x+self.wagon_length*self.direction/3,self.y-self.height/2),(x+self.wagon_length*self.direction/3,self.y-self.height/2-self.height/4),width=4)
class Shell(Bullet):
    def __init__(self,vy,vx,x,y,l,h1,h2,color=BLACK,lifetime=5000):
        self.vy=vy
        self.vx=vx
        Bullet.__init__(self,self.vx,self.vy,x,y,lifetime)
        self.l=l
        self.h1=h1
        self.h2=h2
        self.color=color
        self.rect=None
        self.edge=(self.x,self.y+self.h2)
    def get_rect(self):
        self.rect=pygame.Rect(self.x-self.l,self.y,2*self.l,self.h1)
    def ball_hittest(self,obj):
        x=self.x
        y=self.y+self.h1/2
        collision=obj.hittest((x,y,self.l))
        if collision:
            self.killed=True
        return collision
    def draw(self,screen):
        x1=self.x-self.l
        y1=self.y
        x2=self.x+self.l
        y2=self.y
        x3=self.x+self.l
        y3=self.y+self.h1
        x5=self.x-self.l
        y5=self.y+self.h1
        self.edge=(self.x,self.y+self.h2)
        pygame.draw.polygon(screen,self.color,((x1,y1),(x2,y2),(x3,y3),self.edge,(x5,y5)))
        #pygame.draw.rect(screen,RED,self.rect)
        #pygame.draw.circle(screen, YELLOW, (self.x,self.y+self.h1/2), self.l)
class Gap:
    def __init__(self,x,y,height,width,bullets,lifetime=1000,color=MAGENTA):
        self.x=x
        self.y=y
        self.lifetime=lifetime
        self.color=color
        self.height=height
        self.width=width
        self.opening_time=400
        self.created=pygame.time.get_ticks()
        self.closed=None
        self.closing=False
        self.k=0.0001
        self.indestructible=True
        self.bullets=bullets
        print('')
    def close(self):
        self.closing=True
        self.closed=pygame.time.get_ticks()
    def draw(self,screen):
        rect=pygame.Rect(self.x-self.k*self.width/2,self.y-self.height/2,self.k*self.width,self.height)
        pygame.draw.ellipse(screen, self.color, rect)
    def ball_hittest(self,obj):
        collision=obj.hittest((self.x-self.k*self.width/2,self.y-self.height/2,self.height/2))
        if collision:
            obj.x=13*WIDTH
            obj.y=13*WIDTH
            obj.vx=0
            obj.vy=0
        return False
    def hit_ball(self,ball,bullets):
        bullets.remove(self)
    def hit_tank(self,bullets,gun):
        pass
    def tank_hittest(self,gun):
        if not self.closing:
            self.k=min((pygame.time.get_ticks()-self.created)/self.opening_time,1)
            if pygame.time.get_ticks()-self.created>=self.lifetime:
                self.close()
        else:
            self.k=max(1-(pygame.time.get_ticks()-self.closed)/self.opening_time,0)
        if self.k==0:
            self.disappear()
        return False
    def move(self,bullets):
        pass
    def disappear(self):
        self.bullets.remove(self)











            
