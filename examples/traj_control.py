from mr_sim import *
from mr_sim.planners.traj_controller import TrajController
from mr_sim.sensors import BaseSensor

import numpy as np
from shapely.geometry import Polygon, Point
from shapely import affinity

def main():


    world = World(dt = 0.1)

    # Obstacle Definition
    wall_down = Polygon(
            [[-5,-10], [-5,-1], [-3,-1], [-3,-10]]
    )
    wall_up = affinity.translate(wall_down, 0, 11)

    world.add_obstacle(Obstacle(
        id=0,
        geometry=wall_down
    ))
    world.add_obstacle(Obstacle(
        id=1,
        geometry=wall_up
    ))
    

    world.add_obstacle(Obstacle(
        id=0,
        geometry=Point([7, 5]).buffer(1)
    ))

    # Agents Definition
    rob_shape1 = Polygon(
        [[-1.5,-0.1], [-1.5,0.1], [1.5,0.1], [1.5,-0.1]]
    )

    rob_shape2 = Polygon(
        [[-1,-1], [-1,1], [1,1], [1,-1]]
    )

    rob1 = Robot(
        id=0,
        init_pose=np.array([3.0, 0.0, np.pi/3]),
        shape=rob_shape1,
    )
    ctrler1 = TrajController(
        rob1, [-9, 0, np.pi], world.get_obstacles()
    )
    rob1.add_controller(ctrler1)
    world.add_robot(rob1)

    rob2 = Robot(
        id=1,
        init_pose=np.array([7.0, -7.0, 0.0]),
        shape=rob_shape2,
    )
    ctrler2 = TrajController(
        rob2, [9, 9, np.pi/4], world.get_obstacles()
    )
    rob2.add_controller(ctrler2)
    world.add_robot(rob2)

    sensor = BaseSensor()
    rob1.add_sensor(sensor)
    rob2.add_sensor(sensor)

    # Build env
    env = Env(world)
    env.render()


if __name__ == "__main__":
    main()

