from mr_sim.planners.base_controller import BaseController

from shapely.strtree import STRtree
import numpy as np

class MazeController(BaseController):
    def __init__(self, robot, destination, dist_wall=0.05, max_speed=1):
        self.robot = robot
        self.destination = destination
        self.dist_wall = dist_wall
        self.kp = 2.5
        self.max_speed = max_speed

        self.turn_left = False
        self.turn_right = False
        self.forward = True

    def compute_action(self, obs):

        pose = self.robot.get_pose()
        dist_dest = np.linalg.norm(pose[:2] - self.destination[:2])
        if dist_dest < 0.1:
            return (0.0, 0.0, 0.0)


        depth = obs.data
        num_beams = len(depth)

        # if self.robot.id == 0: print(depth)

        dist_front = np.min(depth[
            int(num_beams*0.48):int(num_beams*0.52)
        ])
        dist_right = np.min(depth[
            int(num_beams*0.23):int(num_beams*0.27)
        ])


        if self.robot.id == 0: print(self.turning, dist_front, dist_right)


        if self.turning:
            if dist_right > self.dist_wall * 0.8:
                self.turning == False
        else:
            if dist_front < self.dist_wall * 0.8:
                self.turning == True

        if self.turning:
            v = 0
            omega = 1
        else:
            v = min(self.max_speed, dist_front * 0.5)

            err = self.dist_wall - dist_right
            omega = self.kp * err
        
        vx = v * np.cos(pose[2])
        vy = v * np.sin(pose[2])


        return vx, vy, omega

