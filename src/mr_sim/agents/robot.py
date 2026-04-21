import numpy as np
from mr_sim.utils.obs import Observation
from mr_sim.core.world import World
from mr_sim.planners.base_controller import BaseController

class Robot:
    def __init__(self, id , x, y, controller: BaseController):
        self.id = id
        # posx, posy, ori
        self.state = np.array([
            x, y, 0.0
            ])
        
        # vx, vy, omega
        self.vel = np.array([
            0.0, 0.0, 0.0
        ])

        self.controller = controller

    def step(self, action, dt):

        vx, vy, w = action
        
        self.state[0] += vx * dt
        self.state[1] += vy * dt
        self.state[2] += w * dt

        self.vel = action

    def sense(self, world: World):
        obs = Observation(world.get_time())

        return obs

    def get_state(self):
        return self.state.copy()
