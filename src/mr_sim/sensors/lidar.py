from mr_sim.sensors.base_sensor import *

import numpy as np
from shapely.geometry import LineString, Point
from shapely.ops import unary_union

class Lidar(BaseSensor):
    def __init__(self, robot, num_beams=360, max_range=2.0, fov=2*np.pi):
        self.robot = robot
        self.num_beams = num_beams
        self.max_range = max_range
        self.fov = fov
        self.angles = np.linspace(-fov/2, fov/2, num_beams)

    def sense(self, world):
        geom_obstacles = [obs.get_geometry() for obs in world.get_obstacles()]

        geom_otheragts = [
            agt.get_geometry() for agt in world.get_agents()
            if agt.id != self.robot.id
        ]

        geom_obstacles = unary_union(geom_obstacles + geom_otheragts)

        x, y, theta = self.robot.get_pose()
        center = Point(x, y)

        depth = np.full(self.num_beams, self.max_range)

        for i, angle in enumerate(self.angles):
            ab_angle = theta + angle

            end_x = x + self.max_range * np.cos(ab_angle)
            end_y = y + self.max_range * np.sin(ab_angle)

            ray = LineString([
                (x, y), (end_x, end_y)
            ])

            intersection = ray.intersection(geom_obstacles)

            if not intersection.is_empty:
                
                depth[i] = center.distance(intersection)

                # if self.robot.id == 0: print(depth[i])

        obs = Observation(data=depth)
        return obs
            