from mr_sim.planners.base_controller import BaseController
from mr_sim.utils.traj import traj_gen

from shapely.strtree import STRtree
import numpy as np

class TrajController(BaseController):
    def __init__(self, robot, goal, obstacles):
        self.robot = robot
        self.obstacles = obstacles

        geom_obs = [obs.get_geometry() for obs in self.obstacles]
        self.tree = STRtree(geom_obs) # static
        
        init_pose = robot.get_pose()

        # print(self.reachable(init_pose))
        # print(self.reachable(goal))

        self.traj = traj_gen(
            init_pose, goal,
            self.reachable,
            bounds=((-10, 10), (-10, 10), (-np.pi, np.pi)),
            # num_samples=1000,
            # k_neighbors=20
        )

    def compute_action(self, obs):
        t = obs.time

        total_t = self.traj.x[-1]
        # print(t, total_t)
        if t >= total_t:
            return (0.0, 0.0, 0.0)
        
        vel = self.traj(t, nu=1)

        vx = float(vel[0])
        vy = float(vel[1])
        omega = float(vel[2])

        return (vx, vy, omega)


    def reachable(self, pose):
        geom_rob = self.robot.fk(pose)

        collided_inds = self.tree.query(geom_rob, predicate='intersects')

        return collided_inds.size == 0
