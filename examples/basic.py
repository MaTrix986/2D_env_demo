from mr_sim.core.world import World
from mr_sim.agents.robot import Robot
from mr_sim.core.env import Env
from mr_sim.planners.base_controller import BaseController

import numpy as np
from shapely.geometry import Polygon, Point

class SimpleController(BaseController):
    def __init__(self, vx, vy, omega):
        self.vx = vx
        self.vy = vy
        self.omega = omega

    def compute_action(self, obs):
        return (self.vx, self.vy, self.omega)


def main():

    world = World(dt = 0.1)

    # shape = Point(0,0).buffer(0.5)
    shape = Polygon(
        [[-1,-1], [-1,1], [1,1], [1,-1]]
    )
    ctrler1 = SimpleController(-1, 0, 0)
    world.add_robot(Robot(
        id=0,
        init_pos=np.array([2.0, 0.0, 0.0]),
        controller=ctrler1,
        shape=shape,
    ))
    ctrler2 = SimpleController(1, 1, 1)
    world.add_robot(Robot(
        id=1,
        init_pos=np.array([-1.0, -5.0, 0.0]),
        controller=ctrler2,
        shape=shape,
    ))

    # world.add_obstacle(

    # )

    env = Env(world)

    env.render()


if __name__ == "__main__":
    main()

