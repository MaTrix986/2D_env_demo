# 2D 多机器人环境模拟

这是一个简单的2D多机器人环境模拟库，用于测试和演示多机器人系统中的规划、控制和传感算法。

## 代码结构

项目采用模块化设计，主要代码位于 `src/mr_sim/` 目录下：

- **`agents/`**: 包含机器人代理的实现

  - `base_agent.py`: 基础代理类
  - `robot.py`: 机器人类，继承自基础代理
- **`core/`**: 核心环境组件

  - `env.py`: 环境类，管理模拟循环和渲染
  - `world.py`: 世界类，管理障碍物和机器人
- **`planners/`**: 规划和控制算法

  - `base_controller.py`: 基础控制器接口
  - `kb_controller.py`: 键盘控制器
  - `maze_controller.py`: 迷宫导航控制器
  - `traj_controller.py`: 轨迹规划控制器
- **`sensors/`**: 传感器模块

  - `base_sensor.py`: 基础传感器类
  - `lidar.py`: Lidar传感器实现
- **`utils/`**: 工具函数

  - `draw.py`: 绘图工具
  - `traj.py`: 轨迹相关工具

其他目录：

- **`examples/`**: 示例脚本，演示不同功能
- **`tests/`**: 测试文件
- **`scripts/`**: 辅助脚本

## 示例

项目提供了三个示例脚本，位于 `examples/` 目录下，每个示例演示不同的功能：

### 1. basic.py - 基础示例

这个示例展示了最基本的环境设置：

- 创建一个世界环境
- 添加静态障碍物（矩形和圆形）
- 创建两个机器人，每个使用简单的固定速度控制器
- 为机器人添加基础传感器

运行方式：

```bash
python examples/basic.py
```

### 2. algo_control.py - 算法控制示例

这个示例演示了更复杂的控制算法：

- 使用 `MazeController` 进行迷宫导航
- 机器人配备Lidar传感器进行环境感知
- 创建一个随机生成的迷宫作为障碍物
- 两个机器人从起点导航到各自的目的地

运行方式：

```bash
python examples/algo_control.py
```

### 3. traj_control.py - 轨迹控制示例

这个示例展示了轨迹规划功能：

- 使用 `TrajController` 进行轨迹规划
- 考虑静态避障，机器人规划从当前位置到目标位置的轨迹

运行方式：

```bash
python examples/traj_control.py
```

## 安装和运行

1. 安装依赖：

```bash
conda env create -f environment.yml
conda activate 2d_env_demo
```

2. 运行示例：

```bash
python examples/<example_name>.py
```

## 依赖

主要依赖包括：

- numpy: 数值计算
- shapely: 几何运算
- matplotlib: 可视化
