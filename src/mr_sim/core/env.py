from mr_sim.utils.draw import draw_geometry, draw_heading

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

class Env:
    def __init__(self, world):
        self.world = world
        self.fig, self.ax = plt.subplots()

    def render(self, ):
        
        ani = FuncAnimation(
            self.fig, 
            self.update, 
            frames = self.time_gen, 
            init_func=self.init_update,
            cache_frame_data = False,
            interval = 20, 
            blit = True
        )
        plt.show()

    def update(self, time):
        # dynamic
        actions = []
        for agent in self.world.get_agents():
            obs = agent.sense(self.world)
            action = agent.controller.compute_action(obs)
            actions.append(action)

        self.world.step(actions)

        objs1 = self.plot_agents()
        objs2 = self.plot_obstacles()

        return *objs1, *objs2,  


    def init_update(self):
        # static
        self.ax.set_xlim(-10, 10)
        self.ax.set_ylim(-10, 10)
        self.ax.set_aspect('equal')
        objs = self.plot_obstacles()

        return *objs,

    def time_gen(self):
        time = 0
        while True:
            time += self.world.dt
            yield time


    def plot_agents(self):

        objs = []

        for agent in self.world.get_agents():

            obj = draw_geometry(
                self.ax, agent.get_geometry(),
                color='blue'
            )
            objs.append(obj)

            ori = draw_heading(
                self.ax, agent.get_pos(),
                length=1,
                color="red"
            )
            objs.append(ori)

        return objs
    
    def plot_obstacles(self):
        objs = []
        for obstacle in self.world.get_obstacles():

            obj = draw_geometry(
                self.ax, obstacle.get_geometry(),
                color='gray'
            )
            objs.append(obj)

        return objs