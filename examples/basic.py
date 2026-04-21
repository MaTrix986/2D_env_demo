from mr_sim.core.world import World
from mr_sim.agents.robot import Robot
from mr_sim.core.env import Env
from mr_sim.planners.base_controller import BaseController

class SimpleController(BaseController):
    def __init__(self):
        pass

    def compute_action(self, obs):
        return (0.5, 0.0, 1.0)

        return super().compute_action(obs)


def main():

    world = World(dt = 0.1)


    ctrler = SimpleController()
    world.add_robot(Robot(
        id=0,
        x=-2, y=0,
        controller=ctrler
    ))

    world.add_robot(Robot(
        id=1,
        x=2, y=1,
        controller=ctrler
    ))


    # sim.add_obstacle(

    # )

    env = Env(world)

    env.render()

    # fig, ax = plt.subplots()
    # x = np.linspace(0, 2 * np.pi, 100)
    # line, = ax.plot(x, np.sin(x))

    # def update(frame):
    # print(frame)
    # line.set_ydata(np.sin(x + frame / 10.0)) # 更新 y 数据
    # return line,

    # ani = FuncAnimation(fig, update, frames=100, interval=20, blit=True)
    # plt.show()






if __name__ == "__main__":
    main()

