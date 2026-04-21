import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class world:
   def __init__(self, pos):
      self.x = pos
   def step(self):
      self.x += 0.05

   def get_x(self):
      return self.x


def update(_, world):
   # print(frame)
   line.set_ydata(world.get_x() * np.sin(x)) # 更新 y 数据
   world.step()
   return line,

init_val = 0.1
w = world(init_val)

fig, ax = plt.subplots()
ax.set_ylim(-1,1)
x = np.linspace(0, 2 * np.pi, 100)
line, = ax.plot(x, init_val * np.sin(x))





ani = FuncAnimation(fig, update, frames=100, fargs=(w,), interval=20, blit=True)
plt.show()