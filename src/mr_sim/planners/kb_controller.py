from mr_sim.planners.base_controller import BaseController
import numpy as np
from pynput import keyboard
from enum import Enum

class State(Enum):
    FORWARD = 0
    FOLLOWING = 1
    TURNING_LEFT = 2
    TURNING_RIGHT = 3

class KeyboardController(BaseController):
    def __init__(self, robot, max_v=2.0, max_omega=3.0):
        self.robot = robot
        
        # 速度状态 (机器人自身坐标系)
        self.local_vx = 0.0   # 前后速度 (W/S)
        self.local_vy = 0.0   # 左右平移速度 (A/D)
        self.omega = 0.0      # 旋转角速度 (Q/E)
        
        # 限制参数
        self.max_v = max_v
        self.max_omega = max_omega

        self.target_yaw = None
        self.state = State.FOLLOWING
        self.dist_wall = 0.5
        
        # 加速度参数 (假设每次 compute_action 调用的时间步长固定，这里的值代表每步的速度增量)
        self.accel_linear = 0.05   # 线加速度
        self.accel_angular = 0.1   # 角加速度
        
        # 阻尼加速度参数 (无输入时的减速力度)
        self.damping_linear = 0.3
        self.damping_angular = 0.3

        # 键盘状态集合
        self.pressed_keys = set()
        
        # 启动后台键盘监听线程
        self.listener = keyboard.Listener(
            on_press=self._on_press,
            on_release=self._on_release)
        self.listener.start()

    def normalize_angle(self, angle):
        """将角度标准化到 [-pi, pi] 之间"""
        return (angle + np.pi) % (2 * np.pi) - np.pi

    def _on_press(self, key):
        """键盘按下事件回调"""
        try:
            self.pressed_keys.add(key.char.lower())
        except AttributeError:
            if key == keyboard.Key.up:
                self.pressed_keys.add('w')
            elif key == keyboard.Key.down:
                self.pressed_keys.add('s')
            elif key == keyboard.Key.left:
                self.pressed_keys.add('a')
            elif key == keyboard.Key.right:
                self.pressed_keys.add('d')

    def _on_release(self, key):
        """键盘抬起事件回调"""
        try:
            self.pressed_keys.discard(key.char.lower())
        except AttributeError:
            if key == keyboard.Key.up:
                self.pressed_keys.discard('w')
            elif key == keyboard.Key.down:
                self.pressed_keys.discard('s')
            elif key == keyboard.Key.left:
                self.pressed_keys.discard('a')
            elif key == keyboard.Key.right:
                self.pressed_keys.discard('d')

    def apply_acceleration_and_damping(self, current_v, key_pos, key_neg, accel, damping, max_val):
        """
        通用的加速度与阻尼计算函数
        :param current_v: 当前速度
        :param key_pos: 正向加速按键 (如 'w')
        :param key_neg: 反向加速按键 (如 's')
        :param accel: 加速度大小
        :param damping: 阻尼加速度大小
        :param max_val: 最大速度限制
        :return: 更新后的速度
        """
        is_pos_pressed = key_pos in self.pressed_keys
        is_neg_pressed = key_neg in self.pressed_keys

        # 1. 施加用户输入的加速度
        if is_pos_pressed and not is_neg_pressed:
            current_v += accel
        elif is_neg_pressed and not is_pos_pressed:
            current_v -= accel
        else:
            # 2. 无输入或按键冲突时，施加反向阻尼加速度
            if current_v > 0:
                current_v = max(0.0, current_v - damping) # 减速到0为止，防止反向
            elif current_v < 0:
                current_v = min(0.0, current_v + damping)

        # 3. 限制最大速度
        current_v = np.clip(current_v, -max_val, max_val)
        return current_v

    def compute_action(self, obs):
        
        pose = self.robot.get_pose()
        current_yaw = pose[2]

        depth = obs.data
        num_beams = len(depth)
        print(num_beams)

        dist_front = np.min(depth[int(num_beams*0.45):int(num_beams*0.55)])
        dist_right = np.min(depth[int(num_beams*0.20):int(num_beams*0.30)])
        dist_left  = np.min(depth[int(num_beams*0.70):int(num_beams*0.80)])

        if self.robot.id == 0: 
            print(f"State: {self.state}, Front: {dist_front:.2f}, Right: {dist_right:.2f}, Left: {dist_left:.2f}")
            pass
        
        if self.state == State.FOLLOWING:
            # 优先右手法则：右侧出现明显路口
            if dist_right > self.dist_wall * 2.0:
                self.state = State.TURNING_RIGHT
                self.target_yaw = self.normalize_angle(current_yaw - np.pi / 2.0)
                self.prev_error = 0.0
                
            # 前方遇到死胡同或拐角，且右侧没路 -> 必须左转
            elif dist_front < self.dist_wall * 1.2:
                self.state = State.TURNING_LEFT
                self.target_yaw = self.normalize_angle(current_yaw + np.pi / 2.0)
                self.prev_error = 0.0

        elif self.state == State.TURNING_LEFT:
            # 检查是否完成了 90 度左转 (误差小于 0.1 弧度，约 5.7 度)
            yaw_error = self.normalize_angle(self.target_yaw - current_yaw)
            if abs(yaw_error) < 0.1:
                self.state = State.FOLLOWING

        elif self.state == State.TURNING_RIGHT:
            # 检查是否完成了 90 度右转
            yaw_error = self.normalize_angle(self.target_yaw - current_yaw)
            if abs(yaw_error) < 0.1:
                self.state = State.FOLLOWING




        # W前进, S后退 (局部 X 轴)
        self.local_vx = self.apply_acceleration_and_damping(
            self.local_vx, 'w', 's', self.accel_linear, self.damping_linear, self.max_v
        )
        
        # A左平移, D右平移 (局部 Y 轴 - 适用于全向轮，如果是差速轮，此处速度将不生效或仅作为逻辑保留)
        self.local_vy = self.apply_acceleration_and_damping(
            self.local_vy, 'a', 'd', self.accel_linear, self.damping_linear, self.max_v
        )
        
        # Q左转(逆时针), E右转(顺时针) (旋转轴)
        self.omega = self.apply_acceleration_and_damping(
            self.omega, 'n', 'm', self.accel_angular, self.damping_angular, self.max_omega
        )

        # Debug 输出当前按键和速度状态
        # if self.robot.id == 0:
        #     print(f"Keys: {self.pressed_keys} | vx: {self.local_vx:.2f}, vy: {self.local_vy:.2f}, w: {self.omega:.2f}")

        

        # 将机器人的局部线速度转换为世界坐标系下的绝对速度 vx, vy
        # (这与你之前的控制器逻辑保持一致)
        global_vx = self.local_vx * np.cos(current_yaw) - self.local_vy * np.sin(current_yaw)
        global_vy = self.local_vx * np.sin(current_yaw) + self.local_vy * np.cos(current_yaw)

        # 返回速度值给底层仿真器
        return global_vx, global_vy, self.omega

    def __del__(self):
        """析构时关闭监听线程"""
        if hasattr(self, 'listener'):
            self.listener.stop()