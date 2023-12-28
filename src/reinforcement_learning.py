from file_utils import *
from database import *
from optimizer import Optimizer

import gym
from gym import spaces
import numpy as np
from stable_baselines3 import DDPG
from stable_baselines3.common.noise import NormalActionNoise


'''
定义学习环境
状态空间 = 超参数组合+当前性能指标
动作空间 = 超参数组合
'''
class SearchEnv(gym.Env):
    
    def __init__(self, database_int, file_interactor):
        # 定义参数范围
        param_ranges = file_interactor.get_config_param()
        super(SearchEnv, self).__init__()
        self.hyperparameter_ranges = param_ranges
        self.current_hyperparameters = {}
        self.database_interactor = database_int

        print(param_ranges)

         # 定义状态空间
        self.observation_space = spaces.Box(low=np.array([param_ranges[param]['range'][0] for param in param_ranges]),
                                           high=np.array([param_ranges[param]['range'][1] for param in param_ranges]),
                                           dtype=np.int32)

        # 定义动作空间
        self.action_space = spaces.Box(low=np.array([param_ranges[param]['range'][0] for param in param_ranges]),
                                        high=np.array([param_ranges[param]['range'][1] for param in param_ranges]),
                                        dtype=np.int32)

        self.current_state = self.generate_random_params(param_ranges)
        
    # 生成随机初始参数
    def generate_random_params(self, param_ranges):
        random_params = []
        for param in param_ranges.items():
            min_val = param[1]['range'][0]
            max_val = param[1]['range'][1]
            if min_val == max_val:
                random_val = min_val
            else:
                random_val = np.random.randint(low=min_val, high=max_val+1)
            random_params.append(random_val)
        return np.array(random_params)

    def list2dic(self, param_list):
        param = {}
        keys = list(self.hyperparameter_ranges.keys())
        for i in range(len(param_list)):
            key = keys[i]
            param[key] = param_list[i]
        return param

    def step(self, action):
        # 根据动作更新超参数
        new_params = self.list2dic(action)
        reward = self.database_interactor.get_data(new_params)
        # reward = np.sum(action)-action[0]-action[1]
        # if (np.random.rand() < 0.5):
        #     reward = -np.sum(action)
        # else:
        #     reward = np.sum(action)
        self.current_state = action
        return self.current_state, reward, False, {}
    
    def reset(self):
        # 初始化超参数
        self.current_state = self.generate_random_params(self.hyperparameter_ranges)
        # 返回初始观察
        return self.current_state

class RLOptimizer(Optimizer):
    def __init__(self, database_interactor, file_interactor, iter_count, benchmark):
        super().__init__(database_interactor, file_interactor, iter_count, benchmark)
        self.name = "RL"
        self.env = SearchEnv(database_interactor, file_interactor)
        # 创建动作噪声
        n_actions = self.env.action_space.shape[-1]
        self.action_noise = NormalActionNoise(mean=np.zeros(n_actions), sigma=0.1 * np.ones(n_actions))
        # 创建DDPG智能体
        self.agent = DDPG('MlpPolicy', self.env, action_noise=self.action_noise, verbose=1)

    def suggest_param(self) -> dict:
        pass

    def optimize(self):
        # 训练智能体
        for episode in range(1):
            observation = self.env.reset()
            print(f"Episode: {episode}, Initial state: {observation}")
            observation, reward, done, info = self.env.step(observation)
            if reward > self.GFlops:
                self.GFlops = reward
                self.best_params = self.env.list2dic(observation)
            total_reward = reward
            # total_reward = 0
            for step in range(self.iter_count):
                action, _ = self.agent.predict(observation)
                action = np.array(action, dtype=int)
                # print(f"Step: {step}, State: {env.current_state}")
                # print(f"Step: {step}, Action: {action}")
                observation, reward, done, info = self.env.step(action)
                if reward > self.GFlops:
                    self.GFlops = reward
                    self.best_params = self.env.list2dic(observation)
                total_reward += reward
                if done:
                    break
            print(f"Episode: {episode}, Total reward: {total_reward}, Last state: {observation}")

    def visualize(self):
        pass
