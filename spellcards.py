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
class Bomb1:
    def __init__(self,gun):
        self.name='Bouncy hell'
        self.gun=gun
        self.v=25
        self.period=500
        self.count=4
        self.launched=0
        self.phase=random.random()*math.pi/7
        self.last_scatter=pygame.time.get_ticks()-self.period
        self.balls_count=13
    def activate(self,balls,Ball):
        stopped=False
        if pygame.time.get_ticks()-self.last_scatter>=self.period:
            self.last_scatter=pygame.time.get_ticks()
            self.scatter(balls,Ball)
            self.launched+=1
            if self.launched==5:
                stopped=True
        return stopped
    def scatter(self,balls,Ball):
        phase=random.random()*2*math.pi/self.balls_count
        for i in range(0,self.balls_count):
            ball=Ball(self.gun.x,self.gun.y)
            an=i*2*math.pi/self.balls_count+phase
            ball.gy*=0.7
            ball.vx = self.v * math.sin(an)+self.gun.v
            ball.vy = - self.v * math.cos(an)
            ball.mindamage*=0.1
            ball.maxdamage*=0.1
            #print(ball.mindamage,ball.maxdamage)
            ball.speed_loss=0.1
            balls.append(ball)
    
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
    def clear(self,bullets):
        pass
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
    def clear(self,bullets):
        for cluster in self.clusters:
            radius=cluster.pop(0)
            phase=cluster.pop(0)
            direction=cluster.pop(0)
            for bullet in cluster:
                angle=cluster.index(bullet)*2*math.pi/self.count+phase
                bullet.vx+=-math.sin(angle-math.pi/2)*direction*self.rotate_speed*radius
                bullet.vy+=math.cos(angle-math.pi/2)*direction*self.rotate_speed*radius
                bullet.vx+=math.sin(angle)*self.r_speed
                bullet.vy+=-math.cos(angle)*self.r_speed
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
    def clear(self,bullets):
        pass
class AttackPattern4:
    def __init__(self,x,y,period,count,v,size,lifetime=2000):
        self.first_delay=2500
        self.last_shot=pygame.time.get_ticks()+self.first_delay
        self.delay=period*1000
        self.v=v
        self.count=count
        self.phase=random.random()*2*math.pi/self.count
        self.x=x
        self.y=y
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
            l,h1,h2=self.size
            bullet=bullet_types.ArrowBullet1(self.v,angle,self.x,self.y,l,h1,h2,lifetime=self.lifetime)
            bullets.append(bullet)
    def clear(self,bullets):
        pass
class AttackPattern5:
    def __init__(self,y,period,count,v,size,lifetime=3000):
        self.first_delay=2500
        self.last_shot=pygame.time.get_ticks()+self.first_delay
        self.delay=period*1000
        self.v=v
        self.count=count
        self.distance=WIDTH/(self.count)
        self.y=y
        self.size=size
        self.lifetime=lifetime
        self.bullets=[]
        self.max_relocations=3
    def activate(self,bullets):
        self.relocate(bullets)
        if pygame.time.get_ticks() - self.last_shot>=self.delay:
            self.scatter(bullets)
            self.last_shot=pygame.time.get_ticks()
    def scatter(self,bullets):
        direction=random.choice((-1,1))
        l,h1,h2=self.size
        phase=random.uniform(l,self.distance)
        for i in range(0,self.count):
            bullet=bullet_types.ArrowBullet1(self.v,math.pi if direction==1 else 0,phase+self.distance*i,self.y,l,h1,h2,lifetime=self.lifetime)
            bullets.append(bullet)
            self.bullets.append([0,bullet])
    def relocate(self,bullets):
        l,h1,h2=self.size
        for bullet in self.bullets:
            #print(bullet[0])
            if bullet[1].y+bullet[1].h2>HEIGHT and bullet[1].an==math.pi:
                bullet[0]+=1
                if bullet[0]>self.max_relocations:
                    self.bullets.remove(bullet)
                else:   
                    n_bullet=bullet_types.ArrowBullet1(bullet[1].v,bullet[1].an,bullet[1].x,bullet[1].y-HEIGHT,l,h1,h2,lifetime=self.lifetime)
                    bullets.append(n_bullet)
                    bullet[1]=n_bullet
            elif bullet[1].y-bullet[1].h2<0 and bullet[1].an==0:
                bullet[0]+=1
                if bullet[0]>self.max_relocations:
                    self.bullets.remove(bullet)
                else:   
                    n_bullet=bullet_types.ArrowBullet1(bullet[1].v,bullet[1].an,bullet[1].x,bullet[1].y+HEIGHT,l,h1,h2,lifetime=self.lifetime)
                    bullets.append(n_bullet)
                    bullet[1]=n_bullet
    def clear(self,bullets):
        pass
    
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
    def clear(self,bullets):
        pass
class SpellCard2:
    def __init__(self,gun):
        self.gun=gun
        self.dead=False
        self.delay=1800
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
    def clear(self,bullets):
        pass        
class SpellCard3:
    def __init__(self,gun):
        self.target=gun
        self.standart_r=WIDTH/2
        self.r=self.standart_r
        self.exist=False
        self.speed=10
        self.narrowing_speed=0.01
        self.bullets=[]
        self.creation_period=50
        self.deployed=pygame.time.get_ticks()
        self.last_created=pygame.time.get_ticks()
        self.count=35
        self.delay=2500
    def activate(self,bullets):
        if not self.exist and pygame.time.get_ticks()-self.deployed>=self.delay:
            self.delay=1300
            self.create(bullets)
        else:
            self.violation_check()
        self.update()
    def create(self,bullets):
        if pygame.time.get_ticks()-self.last_created>=self.creation_period and len(self.bullets)<self.count:
            count=len(self.bullets)
            angle=count*2*math.pi/self.count
            x=self.target.x+self.r*math.sin(angle)
            y=self.target.y-self.r*math.cos(angle)
            bullet=bullet_types.ArrowBullet1(0,angle+math.pi,x,y,WIDTH/30,0,WIDTH/30,lifetime=3000000)
            bullet.indestructible=True
            bullets.append(bullet)
            self.bullets.append(bullet)
            self.last_created=pygame.time.get_ticks()
            if len(self.bullets)==self.count:
                self.exist=True
    def update(self):
        self.r-=self.narrowing_speed
        for i in range(0,len(self.bullets)):
            angle=i*2*math.pi/self.count
            self.bullets[i].x=self.target.x+self.r*math.sin(angle)
            self.bullets[i].y=self.target.y-self.r*math.cos(angle)
        
    def violation_check(self):
        for bullet in self.bullets:
            if bullet.disturbed==True:
                self.no_violation_allowed()
                break
    def no_violation_allowed(self):
        self.deployed=pygame.time.get_ticks()
        for bullet in self.bullets:
            bullet.v=self.speed
            bullet.get_speed()
        self.r=self.standart_r
        self.bullets=[]
        self.exist=False
    def clear(self,bullets):
        for bullet in self.bullets:
            bullets.remove(bullet)
class SpellCard4:
    def __init__(self,gun):
        self.target=gun
        self.delay=2500
        self.std=self.delay/7
        self.last_deployed=pygame.time.get_ticks()
        self.max_height=4*HEIGHT/5
        #self.target.x+=self.target.bottom/2
        self.target.y=HEIGHT-self.target.left
        self.target.inverted=True
        self.trains=[]
        self.sections=8
        self.section_length=self.max_height/self.sections
    def activate(self,bullets):
        if pygame.time.get_ticks()-self.last_deployed>=self.delay+random.choice((-1,1))*self.std*random.random():
            self.delay=600
            self.last_deployed=pygame.time.get_ticks()
            self.deploy(bullets)
    def deploy(self,bullets):
        for train in self.trains:
            if bullets.count(train[0])==0:
                self.trains.remove(train)
        try:
            section=random.choice(list(filter(self.is_section_free,[i*2 for i in range(0,self.sections//2)])))
            height=HEIGHT-(section+random.random())*self.section_length
            train=bullet_types.Train(13,random.choice((1,-1)),height,15,430)
            gap1=bullet_types.Gap(WIDTH/170,train.y,HEIGHT/30,WIDTH/100,bullets,(train.length+WIDTH)/abs(train.vx)/120*1000+450)
            gap2=bullet_types.Gap(WIDTH-WIDTH/170,train.y,HEIGHT/30,WIDTH/100,bullets,(train.length+WIDTH)/abs(train.vx)/120*1000+450)
            bullets.append(train)
            bullets.append(gap1)
            bullets.append(gap2)
            self.trains.append((train,gap1,gap2))
        except:
            pass
    def clear(self,bullets):
        self.target.inverted=False
        self.target.y=HEIGHT-self.target.bottom
    def is_section_free(self,number):
        free=True
        for train,g1,g2 in self.trains:
            if train.y<=HEIGHT-self.section_length*number and train.y>=HEIGHT-self.section_length*(number+1):
                free=False
        return free
class SpellCard5:
    def __init__(self,guns):
        self.guns=guns
        self.dead=False
        self.delay=2500
        self.started=pygame.time.get_ticks()
        self.gaps=[]
        self.shells=[]
        self.explosions=[]
        self.wave_expansion_time=30
        self.r_shard=WIDTH/50
        self.count_shard=17
    def activate(self,bullets):
        if pygame.time.get_ticks()-self.started>=self.delay:
            if len(self.gaps)==0:
                for gun in self.guns:
                    gap1=bullet_types.Gap(WIDTH/170,gun.y+gun.bottom/2,gun.bottom*1.3,WIDTH/100,bullets,12300000)
                    gap2=bullet_types.Gap(WIDTH-WIDTH/170,gun.y+gun.bottom/2,gun.bottom*1.3,WIDTH/100,bullets,12300000)
                    self.gaps.append(gap1)
                    self.gaps.append(gap2)
                    bullets.append(gap1)
                    bullets.append(gap2)
            for gun in self.guns:
                gun.move()
                gun.targetting()
                if gun.deployed:
                    gun.fire_start()
                    shell=gun.power_up()
                    gun.cooling()
                    gun.get_hit()
                    if not shell is None:
                        self.shells.append(shell)
            self.check_shells(bullets)
            self.explode(bullets)
    def clear(self,bullets):
        for gap in self.gaps:
            gap.lifetime=0
    def check_shells(self,bullets):
        for shell in self.shells:
            x,y=shell.edge
            if y>HEIGHT:
                self.explosions.append([shell,0,pygame.time.get_ticks()-12333])
                bullets.remove(shell)
                self.shells.remove(shell)
    def explode(self,bullets):
        shell,stage,last_time=0,1,2
        for exp in self.explosions:
            if pygame.time.get_ticks()-exp[2]>=self.wave_expansion_time and exp[1]<5:
                exp[1]+=1
                shard=AttackPattern1(exp[0].x,exp[0].y,exp[1]*self.r_shard,1000,exp[1]*self.count_shard,exp[1]*self.count_shard,0,WIDTH/100,self.wave_expansion_time)
                shard.scatter(bullets)
                exp[2]=pygame.time.get_ticks()
                if exp[1]>5:
                    self.explosions.remove(exp)
    










            
