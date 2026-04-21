from mr_sim.core.world import World
from mr_sim.agents.robot import Robot
from mr_sim.core.env import Env
from mr_sim.planners.base_controller import BaseController

class SimpleController(BaseController):
    def __init__(self, vx, vy, omega):
        self.vx = vx
        self.vy = vy
        self.omega = omega

    def compute_action(self, obs):
        return (self.vx, self.vy, self.omega)


def main():

    world = World(dt = 0.1)

    ctrler1 = SimpleController(-1, 0, 0)
    world.add_robot(Robot(
        id=0,
        x=-2, y=0,
        controller=ctrler1
    ))
    ctrler2 = SimpleController(1, 1, 1)
    world.add_robot(Robot(
        id=1,
        x=2, y=1,
        controller=ctrler2
    ))


    # sim.add_obstacle(

    # )

    env = Env(world)

    env.render()


if __name__ == "__main__":
    main()

