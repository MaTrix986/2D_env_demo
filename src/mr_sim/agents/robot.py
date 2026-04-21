from typing import TYPE_CHECKING

import numpy as np
from shapely.geometry import Polygon, Point
from shapely import affinity
# from shapely.prepared import prep

from mr_sim.utils.obs import Observation

class Robot:
    def __init__(self, id , init_pos, controller, shape=Point(0,0).buffer(0.5)):
        self.id = id
        # posx, posy, ori
        self.pos = init_pos
        
        # vx, vy, omega
        self.vel = np.array([
            0.0, 0.0, 0.0
        ])

        self.shape = shape
        self.geometry = None
        self.update_geometry()

        self.controller = controller

    def step(self, action, dt):

        vx, vy, w = action
        
        self.pos[0] += vx * dt
        self.pos[1] += vy * dt
        self.pos[2] += w * dt

        self.vel = action

        self.update_geometry()

    def update_geometry(self):
        rotated = affinity.rotate(self.shape, self.pos[2], use_radians=True)
        self.geometry = affinity.translate(rotated, self.pos[0], self.pos[1])

    def sense(self, world):
        obs = Observation(
            world.get_time()
        )
        return obs

    def get_pos(self):
        return self.pos
    
    def get_geometry(self):
        return self.geometry
