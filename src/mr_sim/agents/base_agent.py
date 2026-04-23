import numpy as np

class BaseAgent:
    def __init__(self, id , init_pose, shape):
        self.id = id
        self.pose = init_pose
        
        # vx, vy, omega
        self.vel = np.array([
            0.0, 0.0, 0.0
        ])

        self.shape = shape
        self.geometry = None
        self.update_geometry()

        self.controller = None
        self.sensor = None

    def add_controller(self, controller):
        self.controller = controller

    def add_sensor(self, sensor):
        self.sensor = sensor

    def step(self, action, dt):
        pass

    def update_geometry(self):
        self.geometry = self.fk(self.pose)

    def fk(self, pose):
        pass


    def get_pose(self):
        return self.pose
    
    def get_geometry(self):
        return self.geometry
