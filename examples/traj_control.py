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


    # shape = Point(0,0).buffer(0.5)
    rob_shape = Polygon(
        [[-1,-1], [-1,1], [1,1], [1,-1]]
    )

    
    world.add_robot(Robot(
        id=0,
        init_pose=np.array([2.0, 0.0, np.pi]),
        controller=ctrler1,
        shape=rob_shape,
    ))
    
    world.add_robot(Robot(
        id=1,
        init_pose=np.array([-1.0, -5.0, 0.0]),
        controller=ctrler2,
        shape=rob_shape,
    ))

    

    env = Env(world)
    env.render()


if __name__ == "__main__":
    main()

