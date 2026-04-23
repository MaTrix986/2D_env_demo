from mr_sim import *
from mr_sim.planners import BaseController
from mr_sim.sensors import BaseSensor
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

    world.add_obstacle(Obstacle(
        id=0,
        geometry=Polygon(
            [[-5,-1], [-5,1], [-3,1], [-3,-1]]
    )))

    world.add_obstacle(Obstacle(
        id=0,
        geometry=Point([7, 5]).buffer(1)
    ))


    # rob_shape = Point(0,0).buffer(0.5)
    rob_shape = Polygon(
        [[-1,-1], [-1,1], [1,1], [1,-1]]
    )
    ctrler1 = SimpleController(-1, 0, 0)
    rob1 = Robot(
        id=0,
        init_pose=np.array([2.0, 0.0, np.pi]),
        shape=rob_shape,
    )

    rob1.add_controller(ctrler1)
    world.add_robot(rob1)

    ctrler2 = SimpleController(1, 1, 1)
    rob2 = Robot(
        id=1,
        init_pose=np.array([-1.0, -5.0, 0.0]),
        shape=rob_shape,
    )
    rob2.add_controller(ctrler2)
    world.add_robot(rob2)

    sensor = BaseSensor()
    rob1.add_sensor(sensor)
    rob2.add_sensor(sensor)

   
    env = Env(world)
    env.render()


if __name__ == "__main__":
    main()

