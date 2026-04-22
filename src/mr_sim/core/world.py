# src/mr_sim/core/world.py
from shapely.strtree import STRtree

class World:
    def __init__(self, dt=0.1):
        self.agents = []
        self.obstacles = []
        self.dt = dt
        self.time = 0.0

    def add_robot(self, robot):
        self.agents.append(robot)

    def add_obstacle(self, obstacle):
        self.obstacles.append(obstacle)

    def step(self, actions):
        # actions: list of (vx, vy, w) for each rob

        for i, robot in enumerate(self.agents):

            robot.step(actions[i], self.dt)

            self.check_collision(robot)

        self.time += self.dt

    def check_collision(self, robot):
        geom_rob = robot.get_geometry()

        geom_obstacles = [obs.get_geometry() for obs in self.obstacles]
        for i, agent in enumerate(self.agents):
            if robot.id != agent.id:
                geom_obstacles.append(agent.get_geometry())
        
        tree = STRtree(geom_obstacles)
        collided_inds = tree.query(geom_rob, predicate='intersects')

        for i in collided_inds:
            print(f"[warning] robot(id={robot.id}) has collided.")


    def get_time(self):
        # print(self.time)
        return self.time
    
    def get_agents(self):
        return self.agents
    
    def get_obstacles(self):
        return self.obstacles