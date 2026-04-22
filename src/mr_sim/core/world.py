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

            self.check_collision(robot)

            

        self.time += self.dt

    def check_collision(self, robot):
        geom_rob = robot.get_geometry()

        for i, obstacle in enumerate(self.obstacles):
            geom_obs = obstacle.get_geometry()

            if geom_rob.intersects(geom_obs):
                # colli_area = geom_obs.intersection(geom_obs)
                # coords = list(colli_area.coords)
                print(f"[waning] robot(id={robot.id}) has collided.")

    def collided(self, robot):

        for i, obstacle in enumerate(self.obstacles):
            if robot.get_geometry().intersects(obstacle.get_geometry()):
                return True
            
        return False

    def get_time(self):
        return self.time
    
    def get_agents(self):
        return self.agents
    
    def get_obstacles(self):
        return self.obstacles