import numpy as np
import networkx as nx
from scipy.spatial import KDTree
from scipy.interpolate import CubicSpline

def traj_gen(pose, goal, reachable, bounds=((-10, 10), (-10, 10), (-np.pi, np.pi)), num_samples=300, k_neighbors=15):
    """
    二维环境下机器人的位形空间 (x, y, omega) 轨迹规划
    基于 PRM (概率路图法)
    
    :param pose: 起始姿态 (x, y, omega)
    :param goal: 目标姿态 (x, y, omega)
    :param reachable: 可达性检测函数 reachable(x, y, omega) -> bool
    :param bounds: 采样边界 [(x_min, x_max), (y_min, y_max), (omega_min, omega_max)]
    :param num_samples: 采样点数量
    :param k_neighbors: 每个节点的K个近邻连接数
    :return: 能够接收时间 t 并返回 (x, y, omega) 的分段多项式函数 (CubicSpline)
    """
    # ---------------- 步骤 1: 采样 (Sampling) ----------------
    # 强制将起点和终点加入节点列表
    nodes = [np.array(pose), np.array(goal)]
    
    # 在边界内随机采样，只保留 reachable 为 True 的节点
    while len(nodes) < num_samples + 2:
        sample = np.array([np.random.uniform(b[0], b[1]) for b in bounds])
        # print(sample)
        if reachable(sample):
            nodes.append(sample)
            
    nodes = np.array(nodes)

    # ---------------- 步骤 2 & 3: 连接与增强 (Connection) ----------------
    G = nx.Graph()
    for i in range(len(nodes)):
        G.add_node(i)
        
    # 定义局部路径碰撞检测 (在两个位形之间进行线性插值检测)
    def is_edge_free(q1, q2, steps=10):
        for i in range(1, steps):
            t = i / steps
            q_interp = q1 + t * (q2 - q1)
            if not reachable(q_interp):
                return False
        return True

    # 使用 KDTree 快速查找 K 近邻节点
    tree = KDTree(nodes)
    for i, node in enumerate(nodes):
        # 查找最近的 k_neighbors+1 个点 (包含自身)
        distances, indices = tree.query(node, k=k_neighbors + 1)
        for d, j in zip(distances[1:], indices[1:]):  # 跳过自身
            # 如果尚未连接，且直线路径上无碰撞，则添加边
            if not G.has_edge(i, j) and is_edge_free(node, nodes[j]):
                G.add_edge(i, j, weight=d)

    # ---------------- 步骤 4: 搜索路径 (Search Path) ----------------
    try:
        # 使用 Dijkstra/A* 算法在图上搜索最短路径 (0是起点，1是终点)
        path_indices = nx.shortest_path(G, source=0, target=1, weight='weight')
    except nx.NetworkXNoPath:
        print("PRM 未能找到可行路径，请尝试增加采样点数量 (num_samples)。")
        return None

    path_nodes = nodes[path_indices]

    # ---------------- 轨迹生成 (Trajectory Generation) ----------------
    # 根据两点之间的欧式距离分配时间戳 (假设机器人以单位速度运动)
    times = [0.0]
    for i in range(1, len(path_nodes)):
        dist = np.linalg.norm(path_nodes[i] - path_nodes[i-1])
        times.append(times[-1] + dist)

    # 生成三次样条插值 (Cubic Spline)，这是一种平滑的多维分段多项式
    # bc_type='natural' 表示起点和终点的二阶导数(加速度)为0
    trajectory = CubicSpline(times, path_nodes, bc_type='natural')

    return trajectory