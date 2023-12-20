import argparse
from file_utils import *
from optimizer import *
from database import *
from random_search import *
from TPE import *
from reinforcement_learning import *

parser = argparse.ArgumentParser(description="specify the config file")
parser.add_argument("-f", type=str, default="../config/config.yaml", help="config file")
args = parser.parse_args()
config_filepath = args.f

config = parse_config_yaml(config_filepath)
print("config", config)

# 现在，config是一个包含配置的字典
core_count = config['core_count']
node_count = config['node_count']
algorithm_preference = config['algorithm_preference']
iter_count = config['iter_count']
benchmark = config['benchmark']


# 根据benchmark指定database_interactor和config_param
database_interactor = None
config_param = {}
if benchmark == "HPL":
    database_interactor = HPL_interactor()
    config_param = get_HPL_params()
elif benchmark == "HPCG":
    database_interactor = HPCG_interactor()
    config_param = get_HPCG_params()

# 根据algorithm_preference指定算法
optimzer = None
if algorithm_preference == "random_search":
    optimzer = RandomSearchOptimizer(database_interactor, iter_count, config_param, benchmark)
elif algorithm_preference == "TPE":
    optimzer = TPEOptimizer(database_interactor, iter_count, config_param, benchmark)
elif algorithm_preference == "RL":
    optimzer = RLOptimizer(database_interactor, iter_count, config_param, benchmark)

# 运行优化器
optimzer.optimize()
optimzer.visualize()
optimzer.output()
