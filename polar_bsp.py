import random
import math
from matplotlib import pyplot as plt
from numpy import arange, ones

class polarBSP:
    def __init__(self, r_min, r_max,depth):
        self.r_min = r_min
        self.r_max = r_max
        self.depth = depth
        self.boxes = []
        self.min_r_size = 20
        self.min_th_size = 30
        self.splits = [[]]*(depth+1)
        self.splits[0] = [[r_min,0,r_max,360]]

    def init_plot(self):
        theta = arange(0,361)*math.pi/180
        r = self.r_min*ones((len(theta),))
        ax.plot(theta, r,color='red',lw=1)
        r = self.r_max*ones((len(theta),))
        ax.plot(theta, r,color='red',lw=1)

    def split_and_create_boxes(self):
        for i in range(self.depth):
            if self.splits[i] == []:
                for i in range(self.depth-i+1):
                    self.splits.pop()
                break
            new_splits = []
            for split in self.splits[i]:
                r_start, th_start, r_end, th_end = split
                if th_end-th_start<2*self.min_th_size and r_end-r_start>=2*self.min_r_size: # can't split angularly anymore
                    split_type = 'radial' # that is, r=const split
                elif r_end-r_start<2*self.min_r_size and th_end-th_start>=2*self.min_th_size: # can't split radially anymore
                    split_type = 'angular' # that is, th=const split
                else:
                    split_type = random.choice(['radial','angular'])
                if split_type == 'angular' and th_end-th_start>=2*self.min_th_size:
                    split_pos = random.randint(th_start+self.min_th_size,th_end-self.min_th_size)
                    self.draw_radial_split(r_start,r_end,split_pos)
                    if th_start == 0:
                        """if it's an angular split and the start is at theta=0,
                        there's no real split and the next split is simply "around" the whole circle"""
                        new_splits.append([r_start,split_pos,r_end,split_pos+360])
                    else:
                        new_splits.append([r_start,th_start,r_end,split_pos])
                        new_splits.append([r_start,split_pos,r_end,th_end])
                elif split_type =='radial' and r_end-r_start>=2*self.min_r_size:
                    split_pos = math.sqrt(random.random()*((r_end-self.min_r_size)**2-(r_start+self.min_r_size)**2) + (r_start+self.min_r_size)**2)
                    self.draw_angular_split(th_start,th_end,split_pos)
                    new_splits.append([r_start,th_start,split_pos,th_end])
                    new_splits.append([split_pos,th_start,r_end,th_end])
                else:
                    if random.random() > 0.3:
                        continue
                    else:
                        self.place_planet(split)
            self.splits[i+1] = new_splits

    def place_planet(self,split):
        r_s,th_s,r_e,th_e = split
        dr = 0.25*self.min_r_size
        dth = 0.25*self.min_th_size
        p_r = math.sqrt(random.random()*((r_e-dr)**2-(r_s+dr)**2) + (r_s+dr)**2)
        p_th = random.random()*((th_e-dth)-(th_s+dth))+(th_s+dth)
        ax.scatter(p_th*math.pi/180,p_r,color='blue')
        # self.draw_orbit(p_r)

    def draw_orbit(self,r_orbit):
        theta = arange(0,2*math.pi,0.01)
        r = r_orbit * ones((len(theta),))
        ax.plot(theta,r,color='red',lw=0.5,alpha=0.1)


    def draw_radial_split(self,r1,r2,th0):
        r = arange(r1,r2,0.1)
        theta = th0*math.pi/180 * ones((len(r),))
        ax.plot(theta, r,color='black',lw=0.5,alpha=0.2)

    def draw_angular_split(self,th1,th2,r0):
        theta = arange(th1,th2,0.1) * math.pi/180
        r = r0 * ones((len(theta),))
        ax.plot(theta, r,color='black',lw=0.5,alpha=0.2)

fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
ax.grid(False)
plt.axis('off')
dg = polarBSP(10,100,10)
dg.init_plot()
dg.split_and_create_boxes()
# print(dg.splits)

plt.show()
