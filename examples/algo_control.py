from mr_sim import *
from mr_sim.planners import MazeController
from mr_sim.sensors import Lidar

import numpy as np
from shapely.geometry import Polygon, Point, box, LineString
from shapely.ops import unary_union

def main():


    world = World(dt = 0.1)

    maze = create_maze(0, 20, 20)
    maze.move(-10, -10)
    world.add_obstacle(maze)

    rob_shape = Point(0, 0).buffer(0.2)

    rob1 = Robot(
        id=0,
        init_pose=np.array([-8.5, -9.5, np.pi/3]),
        shape=rob_shape,
    )

    ctrler1 = MazeController(rob1, destination=np.array([8.5, 9.5]), dist_wall=0.05)
    rob1.add_controller(ctrler1)
    sensor1 = Lidar(rob1, max_range=1.0)
    rob1.add_sensor(sensor1)
    world.add_robot(rob1)

    rob2 = Robot(
        id=1,
        init_pose=np.array([8.5, 9.5, -np.pi/2]),
        shape=rob_shape,
    )
    ctrler2 = MazeController(rob2 , destination=np.array([-8.5, -9.5]), dist_wall=0.05)
    rob2.add_controller(ctrler2)
    sensor2 = Lidar(rob2, max_range=1.0)
    rob2.add_sensor(sensor2)
    world.add_robot(rob2)


    env = Env(world)
    env.render()


def create_maze(maze_id, target_w, target_h):
    """
    生成一个符合 target_w * target_h 尺寸的随机迷宫
    """
    # 1. 计算内部路径节点的数量
    # 为了保证有墙有路，我们将目标尺寸映射到内部网格
    nodes_w = (target_w - 1) // 2
    nodes_h = (target_h - 1) // 2
    
    grid_w = 2 * nodes_w + 1
    grid_h = 2 * nodes_h + 1
    grid = [[1 for _ in range(grid_w)] for _ in range(grid_h)]

    # 2. 经典的 DFS 生成
    def carve(cx, cy):
        dirs = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        np.random.shuffle(dirs)
        for dx, dy in dirs:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < nodes_w and 0 <= ny < nodes_h and grid[2*ny+1][2*nx+1] == 1:
                grid[2*cy+1+dy][2*cx+1+dx] = 0
                grid[2*ny+1][2*nx+1] = 0
                carve(nx, ny)

    grid[1][1] = 0
    carve(0, 0)
    
    # 开口
    grid[0][1] = 0
    grid[grid_h-1][grid_w-2] = 0

    # 3. 几何映射与尺寸拉伸
    # 我们计算缩放比例，使得 grid 能够完美填充到 target_w * target_h 的空间
    scale_x = target_w / grid_w
    scale_y = target_h / grid_h
    
    maze_geom_list = []
    for y in range(grid_h):
        for x in range(grid_w):
            if grid[y][x] == 1:
                # 根据比例调整每个墙块的大小和位置
                wall = box(
                    x * scale_x, 
                    y * scale_y, 
                    (x + 1) * scale_x, 
                    (y + 1) * scale_y
                )
                maze_geom_list.append(wall)
    
    # maze_geom_list = maze_geom_list + [
    #     LineString([[-10, -10], [-10, 10]]).buffer(0.02),
    #     LineString([[-10, 10], [10, 10]]).buffer(0.02),
    #     LineString([[10, 10], [10, -10]]).buffer(0.02),
    #     LineString([[10, -10], [-10, -10]]).buffer(0.02),
    # ]

    merged_geometry = unary_union(maze_geom_list)

    return Obstacle(maze_id, merged_geometry)


if __name__ == "__main__":
    main()

