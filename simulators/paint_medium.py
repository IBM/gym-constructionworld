# MIT License
#
# Copyright (C) IBM Corporation 2018, 2019
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
# Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import sys,os
import pygame
import numpy as np
import datetime
import random
import math

from pygame.locals import *
from pygame.color import THECOLORS

GRID_DIM = (16,16)


def distance(x1,y1,x2,y2):
    return math.sqrt((x2-x1)**2+(y2-y1)**2)

def draw_rgb_matrix(screen,rgb_matrix,x_offset=0):

    rows=rgb_matrix.shape[0]
    cols=rgb_matrix.shape[1]

    pygame.draw.rect(screen,pygame.Color(50,50,50), pygame.Rect(0+x_offset,0,800,600))

    for x in range(0, rows):
        for y in range(0, cols):
            r=int(rgb_matrix[x,y,0])
            g=int(rgb_matrix[x,y,1])
            b=int(rgb_matrix[x,y,2])
            if r<0:
                r=0
            elif r>255:
                r=255
            if b<0:
                b=0
            elif b>255:
                b=255
            if g<0:
                g=0
            elif g>255:
                g=255
            color=pygame.Color(r,g,b)
                
            #if val==4 or val==5 or val==6 or val==7:
            #    pygame.draw.rect(screen,pygame.Color(200,200,200), pygame.Rect(x*20,600-y*20,20,20))

            border=1
            pygame.draw.rect(screen,color, pygame.Rect(x*20+border+x_offset,500-y*20+border,20-2*border,20-2*border))

class Window:
    def __init__(self, screen_dim):
        self.width_px = screen_dim[0]
        self.height_px = screen_dim[1]

        self.surface = pygame.display.set_mode(screen_dim)
        self.black_update()
        
    def update_title(self, title):
        pygame.display.set_caption(title)
        self.title = title
        
    def black_update(self):
        self.surface.fill(THECOLORS["black"])
        pygame.display.flip()

    def get_user_input(self):

        for event in pygame.event.get():
            if (event.type == pygame.QUIT): 
                return 'quit'
            elif (event.type == pygame.KEYDOWN):
                if (event.key == K_ESCAPE):
                    return 'quit'
                elif (event.key==K_1):            
                    return '1'           
                elif (event.key==K_2):                          
                    return '2'
                elif (event.key==K_3):                          
                    return '3'
                elif (event.key==K_4):                          
                    return '4'
                elif (event.key==K_5):                          
                    return '5'
                elif(event.key==K_UP):
                    return 'up'
                elif(event.key==K_DOWN):
                    return 'down'
                elif(event.key==K_LEFT):
                    return 'left'
                elif(event.key==K_RIGHT):
                    return 'right'
                elif(event.key==K_m):
                    return "m"
                elif(event.key==K_RETURN):
                    return "reset"
                else:
                    return "Nothing set up for this key."
            
            elif (event.type == pygame.KEYUP):
                pass
            
            elif (event.type == pygame.MOUSEBUTTONDOWN):
                pass
            
            elif (event.type == pygame.MOUSEBUTTONUP):
                pass

                
class World:
    def __init__(self):
        self.grid=np.zeros(GRID_DIM)
        #self.grid=np.random.randint(6,size=GRID_DIM)

        rows=self.grid.shape[0]
        cols=self.grid.shape[1]

        self.t=0

        dist1=0
        dist2=0
        dist3=0
    
        while dist1<5 or dist2<5 or dist3<5:
            self.x1=random.randint(2,rows-3)
            self.y1=random.randint(2,cols-3)
            self.x2=random.randint(2,rows-3)
            self.y2=random.randint(2,cols-3)
            self.x3=random.randint(2,rows-3)
            self.y3=random.randint(2,cols-3)
            dist1=distance(self.x1,self.y1,self.x2,self.y2)
            dist2=distance(self.x1,self.y1,self.x3,self.y3)
            dist3=distance(self.x3,self.y3,self.x2,self.y2)

        #self.grid[self.x1,self.y1]=3
        #self.grid[self.x2,self.y2]=3


        '''
        mx=(int)(self.x1+self.x2)/2
        my=(int)(self.y1+self.y2)/2
        self.grid[mx,my]=1
        '''

        #self.grid[self.x1-1:self.x1+2,self.y1-1:self.y1+2]=2 
        #self.grid[self.x2-1:self.x2+2,self.y2-1:self.y2+2]=2 
        '''
        self.x1=0
        self.y1=0
        self.x2=0
        self.y2=0
        '''
        

        self.x=random.randint(0,rows-1)
        self.y=random.randint(0,cols-1)

        self.grid[self.x,self.y]+=4
        

                    
    def step(self,action):
        reward=0.0
        terminated=False

        rows=self.grid.shape[0]
        cols=self.grid.shape[1]

        if action=='up':
            if self.y+1<cols:
                self.grid[self.x,self.y]-=4
                self.y+=1
                self.grid[self.x,self.y]+=4

        if action=='down':
            if self.y-1>=0:
                self.grid[self.x,self.y]-=4
                self.y-=1
                self.grid[self.x,self.y]+=4

        if action=='left':
            if self.x-1>=0:
                self.grid[self.x,self.y]-=4
                self.x-=1
                self.grid[self.x,self.y]+=4

        if action=='right':
            if self.x+1<rows:
                self.grid[self.x,self.y]-=4
                self.x+=1
                self.grid[self.x,self.y]+=4

        if action=='1':
            self.grid[self.x,self.y]=1+4

        if action=='2':
            self.grid[self.x,self.y]=2+4

        if action=='3':
            self.grid[self.x,self.y]=3+4

        if action=='4':
            self.grid[self.x,self.y]=0+4

        if action=='reset':
            self.__init__()
            terminated=True

        self.t+=1

        return reward, terminated

    def match(self,x,y,c):
        if self.grid[x,y]==c or self.grid[x,y]-4==c or self.grid[x,y]==c-4:
            return True
        else:
            return False

    
    def get_rgb_matrix(self):
        rows=GRID_DIM[0]
        cols=GRID_DIM[1]

        rgb_matrix=np.zeros((rows,cols,3))

        for x in range(0, rows):
            for y in range(0, cols):
                val=self.grid[x,y]
                if val==0:
                    rgb_matrix[x,y,:]=[0,0,0]
                elif val==1:
                    rgb_matrix[x,y,:]=[200,20,20]
                elif val==2:
                    rgb_matrix[x,y,:]=[20,200,20]
                elif val==3:
                    rgb_matrix[x,y,:]=[20,20,200]
                elif val==4:
                    rgb_matrix[x,y,:]=[200-0,200-0,200-0]
                elif val==5:
                    rgb_matrix[x,y,:]=[0,200-20,200-20]
                elif val==6:
                    rgb_matrix[x,y,:]=[200-20,0,200-20]
                elif val==7:
                    rgb_matrix[x,y,:]=[200-20,200-20,0]

        return rgb_matrix




class AutoPaint:
    def __init__(self,world):
        self.world=world
        
        self.mx=(int)(self.world.x1+self.world.x2)/2
        self.my=(int)(self.world.y1+self.world.y2)/2
        self.phase='green_circles'
        self.pstep=0
        self.tasks=[]
        self.cur_task=None
        self.dx=0
        self.dy=0
        self.dc=0
        self.mask=None
        self.dests=[]

         

    def auto_step(self):

        action='none'
        annotation='none'

        rows=self.world.grid.shape[0]
        cols=self.world.grid.shape[1]



        if self.phase=='green_circles':
            if self.pstep==0:
                self.mask=self.world.grid.copy()
                self.tasks.append((self.world.x1,self.world.y1,'2'))
                self.tasks.append((self.world.x2,self.world.y2,'2'))
                self.tasks.append((self.world.x3,self.world.y3,'2'))
                random.shuffle(self.tasks)
                self.pstep=1

            if self.pstep==1:
                if len(self.tasks)>0:

                    self.cur_task=self.tasks.pop()

                        

                    for x in range(0, rows):
                        for y in range(0, cols):
                            tx,ty,tc=self.cur_task
                            dist=distance(tx,ty,x,y)
                            if x==tx and y==ty:
                                self.mask[x,y]=3
                            elif dist<2:
                                self.mask[x,y]=int(tc)
                            

                    self.pstep=2
                else:
                    self.phase='random_move'
                    self.pstep=0

            if self.pstep==2:
                dest_found=False
                paint_center=False
                x=0
                dests=[]
                while x<rows and not paint_center:
                    y=0
                    while y<cols and not paint_center:
                        c=self.mask[x,y]
                        if not self.world.match(x,y,c):
                            dest_found=True
                            if c==3:
                                paint_center=True
                                dests=[(x,y)]

                            else:
                                dests.append((x,y))
                        y+=1
                    x+=1
                if dest_found:
                    (x,y)=random.choice(dests)
                    self.dx=x
                    self.dy=y
                    self.dc=str(int(self.mask[x,y]))
                    self.pstep=3
                else:
                    annotation='end_green_box'
                    self.pstep=1

            if self.pstep>=3:
                action=self.calc_action()
                if action=='3':
                    annotation='begin_green_box'
                if not action:
                    self.pstep=2
                else:
                    self.pstep+=1

        if self.phase=='red_plus':
            if self.pstep==0:

                tx=self.mx 
                ty=self.my
                for x in range(0, rows):
                    for y in range(0, cols):
                        #if (x==tx and abs(y-ty)<2) or (y==ty and abs(x-tx)<2):
                        if abs(x-tx)<2 and abs(y-ty)<2:
                            self.mask[x,y]=1

                self.pstep=1

            if self.pstep==1:
                x=0
                dests=[]
                while x<rows:
                    y=0
                    while y<cols:
                        c=self.mask[x,y]
                        if not self.world.match(x,y,c):
                            dests.append((x,y))
                        y+=1
                    x+=1
                if len(dests)>0:
                    (x,y)=random.choice(dests)
                    self.dx=x
                    self.dy=y
                    self.dc='1'
                    self.pstep=2
                else:
                    if len(self.tasks)==0:
                        annotation='end_red_plus'
                    self.phase='random_move'
                    self.pstep=0

            if self.pstep>=2:
                action=self.calc_action()
                if not action:
                    self.pstep=1
                else:
                    self.pstep+=1

        if self.phase=='random_move':

            if self.pstep==0: 
                self.dx=random.randint(0,self.world.grid.shape[0]-1)
                self.dy=random.randint(0,self.world.grid.shape[1]-1)
                self.dc='-1'
                self.pstep=1

            if self.pstep>=1:

                temp_action=self.calc_action()
                if temp_action=='up' or temp_action=='down' or temp_action=='left' or temp_action=='right':
                    action=temp_action
                    self.pstep+=1
                else:
                    self.phase='complete'
                    self.pstep=0
            
        if self.phase=='complete':
            action='reset'

        #print(self.phase,self.pstep)
        reward, terminated=self.world.step(action)

        if self.phase=='complete':
            self.__init__(self.world)

        return action, annotation, reward, terminated

    def calc_action(self):
        if abs(self.dx-self.world.x)>abs(self.dy-self.world.y):
            if self.dx<self.world.x:
                return 'left'
            elif self.dx>self.world.x:
                return 'right'
        else:
            if self.dy<self.world.y:
                return 'down'
            elif self.dy>self.world.y:
                return 'up'

        if self.world.grid[self.world.x,self.world.y]!=int(self.dc)+4:
            return self.dc
        else:
            return None


class Paint:
    def __init__(self):
        self.name='paint_medium'
        self.world=World()
        self.auto_paint=AutoPaint(self.world)

    def step(self,action):
        self.world.step(action)

    def auto_step(self):
        state0=self.world.get_rgb_matrix()
        action,annotation,reward,terminated=self.auto_paint.auto_step()
        state1=self.world.get_rgb_matrix()
        return state0,state1,action,annotation,reward,terminated,self.world.t

    def random_step(self):
        actions=['up','down','left','right','1','2','3','4']
        action=random.choice(actions)
        state0=self.world.get_rgb_matrix()
        reward,terminated=self.world.step(action)
        annotation=None
        state1=self.world.get_rgb_matrix()
        return state0,state1,action,annotation,reward,terminated,self.world.t

    def draw(self,screen):
        rgb_matrix=self.world.get_rgb_matrix()
        draw_rgb_matrix(screen,rgb_matrix) 



def main():

    world=World()
    auto_paint=AutoPaint(world)
    
    pygame.init()

    window_size=(800, 600)

    window=Window(window_size)
    screen=window.surface
    window.update_title(__file__)

    myclock=pygame.time.Clock()
        
    framerate_limit=4000

    t = 0.0
    finished=False
    mode='user'
    
    while not finished:
        
        window.surface.fill(THECOLORS["black"])
        dt=float(myclock.tick(framerate_limit) * 1e-3)
        
        command=window.get_user_input()

        if command:
            pass

        if command=='reset':
            world=World()
            auto_paint=AutoPaint(world)
        
        elif (command=='quit'):
            finished=True
            
        elif (command!=None):
            pass

        if command=='m':
            if mode=='user':
                mode='auto'
            elif mode=='auto':
                mode='user'
        
        if mode=='auto':
            auto_paint.auto_step()

        if     command=='up'\
            or command=='down'\
            or command=='left'\
            or command=='right'\
            or command=='1'\
            or command=='2'\
            or command=='3'\
            or command=='4':
                world.step(command)

        s0=world.get_rgb_matrix()
        draw_rgb_matrix(screen,s0) 
        
        t+=dt
        pygame.display.flip()



if __name__=="__main__":
    main()
