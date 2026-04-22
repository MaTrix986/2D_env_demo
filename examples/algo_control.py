from mr_sim import *
from mr_sim.planners.traj_controller import TrajController
import numpy as np
from shapely.geometry import Polygon, Point

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

    rob_shape = Polygon(
        [[-1,-1], [-1,1], [1,1], [1,-1]]
    )

    rob1 = Robot(
        id=0,
        init_pose=np.array([2.0, 0.0, np.pi]),
        shape=rob_shape,
    )
    ctrler1 = TrajController(
        rob1, [-9, 0, 0], world.get_obstacles()
    )
    rob1.control(ctrler1)
    world.add_robot(rob1)

    rob2 = Robot(
        id=1,
        init_pose=np.array([-1.0, -5.0, 0.0]),
        shape=rob_shape,
    )
    ctrler2 = TrajController(
        rob2, [9, 9, np.pi/4], world.get_obstacles()
    )
    rob2.control(ctrler2)
    world.add_robot(rob2)


    env = Env(world)
    env.render()


if __name__ == "__main__":
    main()

