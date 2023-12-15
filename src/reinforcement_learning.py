from file_utils import *
from database import *
import gym
from gym import spaces
import numpy as np
from stable_baselines3 import PPO
from stable_baselines3.common.policies import ActorCriticPolicy

from stable_baselines3 import DDPG
from stable_baselines3.common.noise import NormalActionNoise


'''
定义学习环境
状态空间 = 超参数组合+当前性能指标
动作空间 = 超参数组合
'''
class HPLEnv(gym.Env):
    
    def __init__(self):
        # 定义参数范围
        param_ranges = get_HPL_params()
        param_ranges['Q'] = [min(param_ranges['Q']), max(param_ranges['Q'])] # 应为factor
        super(HPLEnv, self).__init__()
        self.hyperparameter_ranges = param_ranges
        self.current_hyperparameters = {}

         # 定义状态空间
        self.observation_space = spaces.Box(low=np.array([param_ranges[param][0] for param in param_ranges]),
                                           high=np.array([param_ranges[param][1] for param in param_ranges]),
                                           dtype=np.int32)

        # 定义动作空间
        self.action_space = spaces.Box(low=np.array([param_ranges[param][0] for param in param_ranges]),
                                        high=np.array([param_ranges[param][1] for param in param_ranges]),
                                        dtype=np.int32)

        self.current_state = self.generate_random_params(param_ranges)
        
    # 生成随机初始参数
    def generate_random_params(self, param_ranges):
        random_params = []
        for param, (min_val, max_val) in param_ranges.items():
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
        # print('action:', action)
        # reward = get_HPL_data(self.list2dic(action))
        reward = -np.sum(action)+5000
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


if __name__ == '__main__':
    # Create the environment
    env = HPLEnv()
    '''
    # PPO智能体
    agent = PPO(ActorCriticPolicy, env, verbose=1, clip_range=0.9)

    # 训练智能体
    for episode in range(10):
        observation = env.reset()
        print(f"Episode: {episode}, Initial state: {observation}")
        total_reward = 0
        for step in range(100):
            action, _ = agent.predict(observation)
            action = np.array(action, dtype=int)
            print(f"Step: {step}, State: {env.current_state}")
            print(f"Step: {step}, Action: {action}")
            observation, reward, done, info = env.step(action)
            total_reward += reward
            if done:
                break
        # if (episode+1) % 100 == 0:
        print(f"Episode: {episode}, Total reward: {total_reward}, Last state: {observation}")
    
    # 训练结束后，保存智能体
    agent.save("ppo_agent.pkl")
    '''

    # 创建动作噪声
    n_actions = env.action_space.shape[-1]
    action_noise = NormalActionNoise(mean=np.zeros(n_actions), sigma=0.1 * np.ones(n_actions))

    # 创建DDPG智能体
    agent = DDPG('MlpPolicy', env, action_noise=action_noise, verbose=1)

    # 训练智能体
    for episode in range(10):
        observation = env.reset()
        print(f"Episode: {episode}, Initial state: {observation}")
        total_reward = 0
        for step in range(100):
            action, _ = agent.predict(observation)
            action = np.array(action, dtype=int)
            print(f"Step: {step}, State: {env.current_state}")
            print(f"Step: {step}, Action: {action}")
            observation, reward, done, info = env.step(action)
            total_reward += reward
            if done:
                break
        print(f"Episode: {episode}, Total reward: {total_reward}, Last state: {observation}")
    