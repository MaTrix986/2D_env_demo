import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

fig, ax = plt.subplots()
x = np.linspace(0, 2 * np.pi, 100)
line, = ax.plot(x, np.sin(x))

def update(frame):
   line.set_ydata(np.sin(x + frame / 10.0)) # 更新 y 数据
   return line,

ani = FuncAnimation(fig, update, frames=100, interval=20, blit=True)
plt.show()