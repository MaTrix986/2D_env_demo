import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# --- 1. 初始化画布和绘图对象 ---
fig, ax = plt.subplots()
xdata, ydata = [], []
ln, = ax.plot([], [], 'r-', animated=True) # animated=True 配合 blit 使用

def init():
    """设置坐标轴的初始范围"""
    ax.set_xlim(0, 10)
    ax.set_ylim(-1.2, 1.2)
    ax.set_title("Real-time Decaying Sine Wave (Generator)")
    return ln,

# --- 2. 生成器函数 (数据源) ---
def data_gen():
    """
    这是一个生成器。它不返回列表，而是每次 'yield' 一个结果。
    FuncAnimation 会自动迭代这个生成器。
    """
    t = 0
    cnt = 0
    while True:  # 也可以设为 while True 实现无限滚动
        t += 0.1
        # 计算物理逻辑：随时间衰减的简谐运动
        y = np.sin(t) * np.exp(-t * 0.05)
        # 产生当前帧需要的 x 和 y
        yield t, y 
        cnt += 1

# --- 3. 更新函数 (绘图逻辑) ---
def update(frame):
    """
    frame 参数就是从 data_gen 里面 yield 出来的 (t, y)
    """
    print(frame)
    t, y = frame
    xdata.append(t)
    ydata.append(y)
    
    # 动态调整横坐标窗口（实现滚动效果）
    xmin, xmax = ax.get_xlim()
    if t >= xmax:
        ax.set_xlim(xmin, xmax + 5)
        ax.figure.canvas.draw() # 坐标轴改变时需要重绘画布
    
    ln.set_data(xdata, ydata)
    return ln,

# --- 4. 组装动画 ---
# 注意：frames 指向的是函数名 data_gen，而不是调用 data_gen()
ani = FuncAnimation(fig, update, frames=data_gen, init_func=init, 
                    blit=True, interval=100, repeat=False)

plt.show()