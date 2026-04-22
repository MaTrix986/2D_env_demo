from mr_sim.agents.obs import Observation

class BaseController:
    def __init__(self):
        pass

    def compute_action(self, obs: Observation):
        pass
