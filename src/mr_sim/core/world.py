# src/mr_sim/core/world.py


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

            # collision()

        self.time += self.dt

    def get_time(self):
        return self.time
    
    def get_agents(self):
        return self.agents
    
    def get_obstacles(self):
        return self.obstacles