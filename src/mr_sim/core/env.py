from mr_sim.core.world import World
from mr_sim.utils.draw import draw_geometry, draw_heading

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

class Env:
    def __init__(self, world: World):
        self.world = world
        self.fig, self.ax = plt.subplots()

    def render(self, ):
        
        ani = FuncAnimation(
            self.fig, 
            self.update, 
            frames = self.time_gen, 
            interval = 20, 
            blit = True
        )
        plt.show()

    def update(self, time):
        
        actions = []
        for agent in self.world.get_agents():
            obs = agent.sense(self.world)
            action = agent.controller.compute_action(obs)
            actions.append(action)

        self.world.step(actions)
        objs = self.plot()

        return *objs, 

    def time_gen(self):
        time = 0
        while True:
            time += self.world.dt
            yield time


    def plot(self):
        self.ax.clear()
        self.ax.set_xlim(-10, 10)
        self.ax.set_ylim(-10, 10)

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

            # pos = agent.pos[:2]
            # r = 1

            # circle = plt.Circle(
            #     pos, r, 
            #     color="blue", fill=True
            # )

            # self.ax.add_patch(circle)


            # direction = pos + [
            #     r * np.cos(agent.pos[2]),
            #     r * np.sin(agent.pos[2])
            # ]

            # self.ax.plot(
            #     [pos[0], direction[0]],
            #     [pos[1], direction[1]],
            #     'r-'
            # )

        return objs