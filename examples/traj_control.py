from mr_sim.core.world import Simulator
from mr_sim.agents.robot import Robot
from mr_sim.core.env import Visualizer
from mr_sim.planners.base_controller import BaseController

class TrajController(BaseController):
    def __init__(self, destination):
        self.dest = destination

    def compute_action(self, obs):


        return super().compute_action(obs)


def main():

    sim = Simulator(dt = 0.1)


    ctrler = TrajController([0, 0])
    sim.add_robot(Robot(
        id=0,
        x=-2, y=0,
        controller=ctrler
    ))

    sim.add_robot(Robot(
        id=1,
        x=2, y=1,
        controller=ctrler
    ))


    # sim.add_obstacle(

    # )

    viz = Visualizer(sim)

    viz.render()

    # fig, ax = plt.subplots()
    # x = np.linspace(0, 2 * np.pi, 100)
    # line, = ax.plot(x, np.sin(x))

    # def update(frame):
    # print(frame)
    # line.set_ydata(np.sin(x + frame / 10.0)) # 更新 y 数据
    # return line,

    # ani = FuncAnimation(fig, update, frames=100, interval=20, blit=True)
    # plt.show()





def get_action():
    action = [
        (0.5, 0.0, 1.0),
        (-0.5, 0.0, 0.0)
    ]
    return action

if __name__ == "__main__":
    main()

