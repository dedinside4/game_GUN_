import pygame
import random
import math
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
class AttackPattern1:
    def __init__(self,x,y,r,period,count1,count2,v,size,lifetime):
        self.first_delay=2500
        self.last_shot=pygame.time.get_ticks()+self.first_delay
        self.delay=period*1000
        self.v=v
        self.count=random.randint(count1,count2)
        self.phase=random.random()*2*math.pi/self.count
        self.x=x
        self.y=y
        self.r=r
        self.size=size
        self.lifetime=lifetime
    def activate(self,bullets):
        if pygame.time.get_ticks() - self.last_shot>=self.delay:
            self.phase=random.random()*2*math.pi/self.count
            self.scatter(bullets)
            self.last_shot=pygame.time.get_ticks()
    def scatter(self,bullets):
        for i in range(0,self.count):
            angle=i*2*math.pi/self.count+self.phase
            x1=self.x+math.sin(angle)*self.r
            y1=self.y-math.cos(angle)*self.r
            bullet=bullet_types.CircleBullet1(self.v*math.sin(angle),-math.cos(angle)*self.v,x1,y1,self.size,self.lifetime)
            bullets.append(bullet)
class AttackPattern3:
    def __init__(self,x,y,r,period,count,r_speed,rotate_speed,size,lifetime):    
        self.first_delay=2500
        self.last_shot=pygame.time.get_ticks()+self.first_delay
        self.delay=period*1000
        self.rotate_speed=rotate_speed
        self.r_speed=r_speed
        self.count=count
        self.phase=random.random()*2*math.pi/self.count
        self.x=x
        self.y=y
        self.r=r
        self.size=size
        self.clusters=[]
        self.lifetime=lifetime
    def activate(self,bullets):
        self.update()
        if pygame.time.get_ticks() - self.last_shot>=self.delay:
            self.phase=random.random()*2*math.pi/self.count
            self.scatter(bullets)
            self.last_shot=pygame.time.get_ticks()
    def scatter(self,bullets):
        cluster=[self.r,self.phase,random.randint(-1,1)]
        for i in range(0,self.count):
            angle=i*2*math.pi/self.count+self.phase
            x1=self.x+math.sin(angle)*self.r
            y1=self.y-math.cos(angle)*self.r
            bullet=bullet_types.CircleBullet1(0,0,x1,y1,self.size,self.lifetime)
            bullets.append(bullet)
            cluster.append(bullet)
        self.clusters.append(cluster)
    def update(self):
        for cluster in self.clusters:
            cluster[0]+=self.r_speed
            cluster[1]+=self.rotate_speed*cluster[2]
            #print(cluster[0])
            for i in range(3,len(cluster)):
                angle=(i-3)*2*math.pi/self.count+cluster[1]
                cluster[i].x=self.x+math.sin(angle)*cluster[0]
                cluster[i].y=self.y-math.cos(angle)*cluster[0]
            if cluster[0]>2*HEIGHT:
                self.clusters.remove(cluster)
            
class AttackPattern2:
    def __init__(self,x,y,period,v,size,gun):
        self.l,self.h1,self.h2=size
        self.first_delay=2000
        self.last_shot=pygame.time.get_ticks()+self.first_delay
        self.delay=period*1000
        self.v=v
        self.x=x
        self.y=y
        self.target=gun
    def activate(self,bullets):
        if pygame.time.get_ticks() - self.last_shot>=self.delay:
            try:
                an = math.atan2((self.target.x - self.x), (self.y - self.target.y))
            except:
                an = -math.pi/2
            self.scatter(bullets,an)
            self.last_shot=pygame.time.get_ticks()
    def scatter(self,bullets,an):
        bullets.append(bullet_types.ArrowBullet1(self.v,an,self.x,self.y,self.l,self.h1,self.h2))
class SpellCard1:
    def __init__(self,gun,x,y):#,bullets):
        self.x=x
        self.y=y
        #self.bullets
        self.target=gun
        self.drones=[]
        self.shards=[]
        self.rotatable=[]
        self.first_delay=2500
        self.last_shot=pygame.time.get_ticks()+self.first_delay
        self.count=35
        self.hight=HEIGHT/2
        self.v=7
        self.rotate_speed=0.01
        self.l=WIDTH/(self.count*2.4)
        self.h2=self.l*2.4
        self.h1=self.h2*0.2
        self.period=80
        self.phase=1
        self.act=None
        self.phase_1_done=None
        self.delay_1=100
        self.detection_range=math.sqrt((HEIGHT/2)**2+(WIDTH*3/17)**2)
        self.phase_2_time=2500
        self.thrusted=[]
        self.detonation_time=600
        self.wave_expansion_time=50
        self.r_shard=WIDTH/29
        self.count_shard=17
    def phase_1(self,bullets):
        i=1
        while i==1:
            if pygame.time.get_ticks()-self.last_shot>=self.period:
                an = math.atan2((1*WIDTH/(self.count+1) - self.x), (self.y - self.hight))
                drone=bullet_types.ArrowBullet1(self.v,an,self.x,self.y,self.l,self.h1,self.h2)
                #print('added')
                bullets.append(drone)
                self.drones.append(drone)
                self.last_shot=pygame.time.get_ticks()
                i+=1
            yield 1
        j=0
        killed_drones=[]
        while j<self.count-len(killed_drones):
            for drone in self.rotatable:
                self.rotate_1(drone)
            for drone in self.drones:
                if drone.killed and killed_drones.count(drone)==0:
                    killed_drones.append(drone)
                if ((self.drones.index(drone)+1)*WIDTH/(self.count+1) - self.x)**2+(self.y - self.hight)**2<(drone.x - self.x)**2+(self.y - drone.y)**2:
                    drone.v=0
                    drone.get_speed()
                    drone.x=(self.drones.index(drone)+1)*WIDTH/(self.count+1)
                    drone.y=self.hight
                    self.rotatable.append(drone)
                    j+=1
            if i<=self.count and pygame.time.get_ticks()-self.last_shot>=self.period:
                an = math.atan2((i*WIDTH/(self.count+1) - self.x), (self.y - self.hight))
                drone=bullet_types.ArrowBullet1(self.v,an,self.x,self.y,self.l,self.h1,self.h2)
                #print('added')
                bullets.append(drone)
                self.drones.append(drone)
                self.last_shot=pygame.time.get_ticks()
                i+=1
            yield (j,self.count-len(killed_drones))
        while len(self.rotatable)>0:
            for drone in self.rotatable:
                self.rotate_1(drone)
            yield 3
        self.phase_1_done=pygame.time.get_ticks()
        yield None
    def phase_2(self,bullets):
        while pygame.time.get_ticks()-self.phase_1_done<self.delay_1:
            yield 1
        started=pygame.time.get_ticks()
        yield 2
        while pygame.time.get_ticks()-started<self.phase_2_time:
            #print(pygame.time.get_ticks()-started
            for drone in self.drones:
                if (drone.x-self.target.x)**2+(drone.y-self.target.y)**2<=self.detection_range**2:
                    self.rotate_2(drone)
                else:
                    self.rotatable.append(drone)
                    self.rotate_1(drone)
            yield 3
        for drone in self.drones:
            drone.v=self.v
            drone.get_speed()
        yield 4
    def phase_3(self,bullets):
        #print('worked')
        while len(self.thrusted)!=len(self.drones):
            #print(len(self.thrusted),len(self.drones))
            for drone in self.drones:
                #print(drone.killed)
                if drone.killed:
                    self.drones.remove(drone)
                    try:  
                        self.thrusted.remove(drone)
                    except:
                        pass
                else:
                    x,y=drone.edge
                    if y>HEIGHT and self.thrusted.count(drone)==0:
                        drone.v=0
                        drone.get_speed()
                        self.thrusted.append(drone)
            yield 1
        countdown=pygame.time.get_ticks()
        while pygame.time.get_ticks()-countdown<self.detonation_time:
            for drone in self.drones:
                if drone.killed:
                    self.drones.remove(drone)
                    self.thrusted.remove(drone)
            yield 2
        yield 3
    def phase_4(self,bullets):
        #print(len(self.drones))
        for drone in self.drones:
            shard=AttackPattern1(drone.x,drone.y,self.r_shard,1000,self.count_shard,self.count_shard,0,WIDTH/100,self.wave_expansion_time)
            shard.scatter(bullets)
        last_expansion=pygame.time.get_ticks()
        while pygame.time.get_ticks()-last_expansion<self.wave_expansion_time:
            yield 1
        for drone in self.drones:
            if not drone.killed:
                try:
                    bullets.remove(drone)
                except:
                    pass
            shard=AttackPattern1(drone.x,drone.y,2*self.r_shard,1000,2*self.count_shard,2*self.count_shard,0,WIDTH/100,self.wave_expansion_time)
            shard.scatter(bullets)
        last_expansion=pygame.time.get_ticks()
        while pygame.time.get_ticks()-last_expansion<self.wave_expansion_time:
            yield 2
        for drone in self.drones:
            shard=AttackPattern1(drone.x,drone.y,3*self.r_shard,1000,3*self.count_shard,3*self.count_shard,0,WIDTH/100,self.wave_expansion_time)
            shard.scatter(bullets)
        last_expansion=pygame.time.get_ticks()
        while pygame.time.get_ticks()-last_expansion<self.wave_expansion_time:
            yield 3
        self.drones = []
        self.thrusted=[]
        self.rotatable=[]
        self.act=None
        self.phase=1
        yield 4
    def rotate_2(self,drone):
        angle1 = (2*math.pi+math.atan2((self.target.x - drone.x), (drone.y - self.target.y)))%(2*math.pi)
        angle2 = (2*math.pi+drone.an)%(2*math.pi)
        
        if angle1>angle2:
            angle2+=self.rotate_speed
            if angle1<angle2:
                angle2=angle1
        elif angle1<angle2:
            angle2-=self.rotate_speed
            if angle1>angle2:
                angle2=angle1
        drone.an=angle2%math.pi-(angle2//math.pi)*math.pi
    def rotate_1(self,drone):
        if drone.an<0:
            drone.an-=self.rotate_speed
            if drone.an<=-math.pi:
                drone.an=math.pi
                self.rotatable.remove(drone)
        elif drone.an>0:
            drone.an+=self.rotate_speed
            if drone.an>=math.pi:
                drone.an=math.pi
                self.rotatable.remove(drone)
    def activate(self,bullets):
        #exec(f'self.phase_{self.phase}(bullets)')
        if self.act is None:
            self.act=eval(f'self.phase_{self.phase}(bullets)')
        else:
            try:
                next(self.act)
            except: #Exception as e:
                #print(e)
                self.act=None
                exec(f'self.phase_{self.phase}_done=pygame.time.get_ticks()')
                self.phase+=1
class SpellCard2:
    def __init__(self,gun):
        self.gun=gun
        self.dead=False
        self.delay=1500
        self.started=pygame.time.get_ticks()
    def activate(self,bullets):
        if not self.dead and pygame.time.get_ticks()-self.started>=self.delay:
            if self.gun.landed:
                self.gun.update_trigger()
                self.gun.targetting()
                self.gun.fire_start()
                self.gun.power_up()
                self.gun.cooling()
            else:
                self.gun.fall()
            self.dead=self.gun.get_hit()
            self.dead=self.gun.get_hit_tank() or self.dead
        
