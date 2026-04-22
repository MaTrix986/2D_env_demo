import numpy as np
from mr_sim.planners import TrajController
from mr_sim.utils.traj import traj_gen


def test_reachable(x, y, omega):
    # 假设 (5, 5) 处有一个半径为 2 的圆形障碍物
    if (x - 5)**2 + (y - 5)**2 < 4:
        return False
    return True

start_pose = (1.0, 1.0, 0.0)
goal_pose = (9.0, 9.0, np.pi/2)

traj = traj_gen(start_pose, goal_pose, test_reachable)

if traj is not None:
    
    total_time = traj.x[-1]  # 获取轨迹的总时长
    
    print(f"规划成功！总预计运动时间: {total_time:.2f}s")
    print(f"t=0.0s 时刻的位置: {traj(0.0)}")
    print(f"t={total_time/2:.2f}s 时刻的位置: {traj(total_time/2)}")
    print(f"t={total_time:.2f}s 时刻的位置: {traj(total_time)}")