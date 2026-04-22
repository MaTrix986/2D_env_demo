from mr_sim import *
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
    rob_shape = Polygon(
        [[-1,-1], [-1,1], [1,1], [1,-1]]
    )
    ctrler1 = SimpleController(-1, 0, 0)
    world.add_robot(Robot(
        id=0,
        init_pos=np.array([2.0, 0.0, np.pi]),
        controller=ctrler1,
        shape=rob_shape,
    ))
    ctrler2 = SimpleController(1, 1, 1)
    world.add_robot(Robot(
        id=1,
        init_pos=np.array([-1.0, -5.0, 0.0]),
        controller=ctrler2,
        shape=rob_shape,
    ))

    world.add_obstacle(Obstacle(
        id=0,
        geometry=Polygon(
            [[-5,-1], [-5,1], [-3,1], [-3,-1]]
    )))

    world.add_obstacle(Obstacle(
        id=0,
        geometry=Point([7, 5]).buffer(1)
    ))

    env = Env(world)
    env.render()


if __name__ == "__main__":
    main()

