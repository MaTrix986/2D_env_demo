from mr_sim.utils.obs import Observation

class BaseController:
    def __init__(self):
        pass

    def compute_action(self, obs: Observation):
        pass
