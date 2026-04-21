from mr_sim.core.world import World

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

def frame_gen():
    frame = 0
    while True:
        frame += 1
        yield frame

class Env:
    def __init__(self, world: World):
        self.world = world
        self.fig, self.ax = plt.subplots()

    def render(self, ):
        
        ani = FuncAnimation(
            self.fig, 
            self.update, 
            frames = frame_gen, 
            interval = self.world.dt * 1000, 
            blit = True
        )
        plt.show()

    def update(self, frame):
        print(frame)
        
        actions = []
        for agent in self.world.get_agents():
            obs = agent.sense(self.world)
            action = agent.controller.compute_action(obs)
            actions.append(action)

        self.world.step(actions)
        self.plot()

        return self.ax,


    def plot(self):
        self.ax.clear()
        self.ax.set_xlim(-10, 10)
        self.ax.set_ylim(-10, 10)

        for agent in self.world.get_agents():

            pos = agent.state[:2]
            r = 1

            circle = plt.Circle(
                pos, r, 
                color="blue", fill=True
            )

            self.ax.add_patch(circle)


            direction = pos + [
                r * np.cos(agent.state[2]),
                r * np.sin(agent.state[2])
            ]

            self.ax.plot(
                [pos[0], direction[0]],
                [pos[1], direction[1]],
                'r-'
            )
