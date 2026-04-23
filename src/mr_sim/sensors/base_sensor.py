class Observation:
    def __init__(self, time=None, data=None):
        self.time = time
        self.data = data



class BaseSensor():

    def __init__(self):
        pass

    def sense(self, world):
        obs = Observation(
            world.get_time()
        )

        return obs