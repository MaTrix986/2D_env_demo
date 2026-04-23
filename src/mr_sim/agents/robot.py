from typing import TYPE_CHECKING

import numpy as np
from shapely.geometry import Polygon, Point
from shapely import affinity
# from shapely.prepared import prep


class Robot:
    def __init__(self, id , init_pose, shape=Point(0,0).buffer(0.5)):
        self.id = id
        # posex, posey, ori
        self.pose = init_pose
        
        # vx, vy, omega
        self.vel = np.array([
            0.0, 0.0, 0.0
        ])

        self.shape = shape
        self.geometry = None
        self.update_geometry()

        self.controller = None
        self.sensor = None

    def add_controller(self, controller):
        self.controller = controller

    def add_sensor(self, sensor):
        self.sensor = sensor

    def step(self, action, dt):
        if action:
            vx, vy, w = action
            
            self.pose[0] += vx * dt
            self.pose[1] += vy * dt
            self.pose[2] += w * dt

            self.vel = action

            self.update_geometry()

    def update_geometry(self):
        self.geometry = self.fk(self.pose)

    def fk(self, pose):
        rotated = affinity.rotate(self.shape, pose[2], use_radians=True)
        geom = affinity.translate(rotated, pose[0], pose[1])
        return geom


    def get_pose(self):
        return self.pose
    
    def get_geometry(self):
        return self.geometry
