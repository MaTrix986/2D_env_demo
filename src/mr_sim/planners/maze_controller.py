from mr_sim.planners.base_controller import BaseController
from shapely.strtree import STRtree
import numpy as np
from enum import Enum
import math

class State(Enum):
    FOLLOWING = 1
    TURNING_LEFT = 2
    TURNING_RIGHT = 3

class MazeController(BaseController):
    def __init__(self, robot, destination, dist_wall=0.5, max_speed=1.0, min_follow_dist=0.6):
        self.robot = robot
        self.destination = destination
        self.dist_wall = dist_wall
        self.max_speed = max_speed
        
        # PD 居中控制器
        self.kp = 2.0   
        self.kd = 10.0  
        self.prev_error = 0.0 
        
        # 转向控制参数
        self.target_yaw = None  
        self.turn_kp = 15      
        
        self.min_follow_dist = min_follow_dist  # 进入 FOLLOWING 后必须至少走多远
        self.following_start_pose = None        # 记录进入 FOLLOWING 时的坐标
        
        self.state = State.FOLLOWING

    def normalize_angle(self, angle):
        
        return (angle + np.pi) % (2 * np.pi) - np.pi

    def compute_action(self, obs):
        pose = self.robot.get_pose()
        current_yaw = pose[2]
        
        if self.following_start_pose is None:
            self.following_start_pose = pose[:2]
        
        # 到达终点检测
        dist_dest = np.linalg.norm(pose[:2] - self.destination[:2])
        if dist_dest < 0.1:
            return (0.0, 0.0, 0.0)

        depth = obs.data
        num_beams = len(depth)

        dist_front = np.min(depth[int(num_beams*0.45):int(num_beams*0.55)])
        dist_right = np.min(depth[int(num_beams*0.20):int(num_beams*0.30)])
        dist_left  = np.min(depth[int(num_beams*0.70):int(num_beams*0.80)])

        if self.robot.id == 0: 
            # print(f"State: {self.state}, Front: {dist_front:.2f}, Right: {dist_right:.2f}")
            pass

        if self.state == State.FOLLOWING:
            # 计算自从进入 FOLLOWING 状态后走过的距离
            dist_traveled = np.linalg.norm(pose[:2] - self.following_start_pose)
            
            if dist_traveled >= self.min_follow_dist:
                # 右手法则
                if dist_right > self.dist_wall * 2.0:
                    self.state = State.TURNING_RIGHT
                    self.target_yaw = self.normalize_angle(current_yaw - np.pi / 2.0)
                    self.prev_error = 0.0
                    
                elif dist_front < self.dist_wall * 1.7:
                    self.state = State.TURNING_LEFT
                    self.target_yaw = self.normalize_angle(current_yaw + np.pi / 2.0)
                    self.prev_error = 0.0
            
            else:
                if dist_front < self.dist_wall * 0.6:
                    self.state = State.TURNING_LEFT
                    self.target_yaw = self.normalize_angle(current_yaw + np.pi / 2.0)
                    self.prev_error = 0.0

        elif self.state == State.TURNING_LEFT:
            # 检查是否完成了 90 度左转
            yaw_error = self.normalize_angle(self.target_yaw - current_yaw)
            if abs(yaw_error) < 0.1:
                self.state = State.FOLLOWING
                self.following_start_pose = pose[:2] 

        elif self.state == State.TURNING_RIGHT:
            # 检查是否完成了 90 度右转
            yaw_error = self.normalize_angle(self.target_yaw - current_yaw)
            if abs(yaw_error) < 0.1:
                self.state = State.FOLLOWING
                self.following_start_pose = pose[:2]


        v, omega = 0.0, 0.0

        if self.state == State.FOLLOWING:
            # 避让
            if self.dist_wall * 0.8 < dist_front < self.dist_wall * 1.8 and dist_left < self.dist_wall * 2.0:
                v = self.max_speed * 0.3  # 减速
                error = (self.dist_wall * 0.6) - dist_right 
                omega = self.kp * error
                
            # 居中
            else:
                v = self.max_speed
                if dist_left < self.dist_wall * 2.0 and dist_right < self.dist_wall * 2.0:
                    error = dist_right - dist_left
                    d_error = error - self.prev_error
                    omega = -(self.kp * error + self.kd * d_error)
                    self.prev_error = error
                
                elif dist_right < self.dist_wall * 2.0:
                    error = self.dist_wall - dist_right
                    d_error = error - self.prev_error
                    omega = self.kp * error + self.kd * d_error
                    self.prev_error = error

        elif self.state == State.TURNING_LEFT:
            v = self.max_speed * 0.2 
            yaw_error = self.normalize_angle(self.target_yaw - current_yaw)
            omega = np.sign(yaw_error) * max(0.5, abs(self.turn_kp * yaw_error))

        elif self.state == State.TURNING_RIGHT:
            v = self.max_speed * 0.2
            yaw_error = self.normalize_angle(self.target_yaw - current_yaw)
            omega = np.sign(yaw_error) * max(0.5, abs(self.turn_kp * yaw_error))

        
        omega = np.clip(omega, -2.5, 2.5)

        vx = v * np.cos(current_yaw)
        vy = v * np.sin(current_yaw)

        return vx, vy, omega