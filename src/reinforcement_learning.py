import gym
from gym import spaces
import numpy as np
from stable_baselines3 import PPO
from stable_baselines3.common.policies import ActorCriticPolicy

'''
定义学习环境
状态空间 = 超参数组合+当前性能指标
动作空间 = 超参数组合
'''
class HPLEnv(gym.Env):
    
    def __init__(self, core_count):
        # 定义参数范围
        param_ranges = {
            "N": [10, 100000],
            "NB": [10, 1000],
            "PMAP": [0, 1],
            "Q": [1, core_count],  # 请将core_count替换为实际的核心数
            "PFACT": [0, 2],
            "NBMIN": [2, 50],
            "NDIV": [2, 10],
            "RFACT": [0, 2],
            "BCAST": [0, 5],
            "DEPTH": [0, 6],
            "SWAP": [0, 2],
            "L1": [0, 1],
            "U": [0, 1],
            "EQUIL": [0, 1]
        }
        super(HPLEnv, self).__init__()
        self.hyperparameter_ranges = param_ranges
        self.current_hyperparameters = {}

         # 定义状态空间
        self.observation_space = spaces.Box(low=np.array([param_ranges[param][0] for param in param_ranges]),
                                           high=np.array([param_ranges[param][1] for param in param_ranges]),
                                           dtype=np.float32)

        # 定义动作空间
        self.action_space = spaces.Discrete(14)

        self.current_state = self.generate_random_params(param_ranges)
        
    # 生成随机初始参数
    def generate_random_params(self, param_ranges):
        random_params = []
        for param, (min_val, max_val) in param_ranges.items():
            random_params.append(np.random.uniform(low=min_val, high=max_val))
        # 现在是float, 需要转换为int
        return np.array(random_params)

    def step(self, action):
        # 根据动作更新超参数
        # hyperparameter_name = list(self.hyperparameter_ranges.keys())[action[0]]
        # new_value = np.random.uniform(low=self.hyperparameter_ranges[hyperparameter_name][0],
        #                               high=self.hyperparameter_ranges[hyperparameter_name][1])
        # self.current_state[hyperparameter_name] = new_value

        # 在这里，可以根据新的超参数配置运行机器学习模型，并返回性能指标
        # 这里只是一个示例，性能指标是一个随机值
        reward = np.random.rand()
        # print('step:', self.current_state)
        return self.current_state, reward, False, {}
    
    def reset(self):
        # 初始化超参数
        self.current_state = self.generate_random_params(self.hyperparameter_ranges)
        # 返回初始观察
        return self.current_state

    def evaluate(self, state):
        accuracy = 0.0  # 使用num_layers和learning_rate训练CNN并获取准确率
        return accuracy


if __name__ == '__main__':
    # Create the environment
    env = HPLEnv(10)

    # PPO智能体
    agent = PPO(ActorCriticPolicy, env, verbose=1)

    # 训练智能体
    for episode in range(100):
        observation = env.reset()
        total_reward = 0
        for step in range(100):
            action, _ = agent.predict(observation)
            observation, reward, done, info = env.step(action)
            total_reward += reward
            if done:
                break
        print(f"Episode: {episode}, Total reward: {total_reward}, Last state: {observation}")
    
    # 训练结束后，你可以保存智能体
    agent.save("ppo_agent.pkl")