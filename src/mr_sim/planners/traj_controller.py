from mr_sim.planners.base_controller import BaseController
from mr_sim.utils.traj import traj_gen

from shapely.strtree import STRtree

class TrajController(BaseController):
    def __init__(self, robot, goal, obstacles):
        self.robot = robot
        self.obstacles = obstacles

        self.traj = traj_gen(
            self.pose, self.goal,
            self.reachable
        )

    def compute_action(self, obs):
        t = obs.time

        total_t = self.traj.x[-1]

        if t >= total_t:
            return (0.0, 0.0, 0.0)
        
        vel = self.traj(t, nu=1)

        vx = float(vel[0])
        vy = float(vel[1])
        omega = float(vel[2])

        return (vx, vy, omega)


    def reachable(self, pose):
        geom_rob = self.robot.fk(pose)

        geom_obs = [obs.get_geometry() for obs in self.obstacles]
        for i, agent in enumerate(self.robot):
            if self.robot.id != agent.id:
                geom_obs.append(agent.get_geometry())
        
        tree = STRtree(geom_obs)
        collided_inds = tree.query(geom_rob, predicate='intersects')

        return collided_inds == []
