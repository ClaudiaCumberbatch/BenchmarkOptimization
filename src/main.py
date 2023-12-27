import argparse
from file_utils import *
from optimizer import *
from database import *
from random_search import *
from TPE import *
from GP import *
from GA import *


parser = argparse.ArgumentParser(description="specify the config file")
parser.add_argument("-f", type=str, default="../config/config.yaml", help="config file")
args = parser.parse_args()
config_filepath = args.f

config = file_interactor.parse_config(config_filepath)
print("config", config)

# 现在，config是一个包含配置的字典
core_count = config['core_count']
node_count = config['node_count']
algorithm_preference = config['algorithm_preference']
iter_count = config['iter_count']
benchmark = config['benchmark']


# 根据benchmark指定database_interactor和config_param
database_int = None
file_int = None
if benchmark == "HPL":
    file_int = HPL_file_interactor(config_filepath)
    database_int = HPL_interactor(file_int)
elif benchmark == "HPCG":
    file_int = HPCG_file_interactor(config_filepath)
    database_int = HPCG_interactor(file_int)

# 根据algorithm_preference指定算法
optimzer = None
if algorithm_preference == "random_search":
    optimzer = RandomSearchOptimizer(database_int, file_int, iter_count, benchmark)
elif algorithm_preference == "TPE":
    optimzer = TPEOptimizer(database_int, file_int, iter_count, benchmark)
elif algorithm_preference == "GP":
    optimzer = GPOptimizer(database_int, file_int, iter_count, benchmark)
elif algorithm_preference == "GA":
    optimzer = GAOptimizer(database_int, file_int, iter_count, benchmark)
elif algorithm_preference == "RL":
    from reinforcement_learning import *
    optimzer = RLOptimizer(database_int, file_int, iter_count, benchmark)

# 运行优化器
optimzer.optimize()
optimzer.visualize()
optimzer.output()
