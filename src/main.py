import argparse
from random_search import *
import yaml
from file_utils import *
from output_utils import *
from bayesian_optuna import *
import time

parser = argparse.ArgumentParser(description="specify the config file")
parser.add_argument("-f", type=str, default="../config/config.yaml", help="config file")
args = parser.parse_args()
config_filepath = args.f

config = parse_config_yaml(config_filepath)
print(config)

# 现在，config是一个包含配置的字典
core_count = config['core_count']
node_count = config['node_count']
algorithm_preference = config['algorithm_preference']
iter_count = config['iter_count']
benchmark = config['benchmark']


# 根据benchmark参数调用不同的函数
function_key = algorithm_preference + "_" + benchmark
switcher = {
    "random_search_HPL": random_search_HPL,
    "random_search_HPCG": random_search_HPCG,
    "optuna_HPL": optuna_HPL,
    "optuna_HPCG": optuna_HPCG
}
func = switcher.get(function_key, "Invalid choice of algorithm preference and benchmark")

start_time = time.time()
best_param, best_gflops = func(node_count, core_count, iter_count)
end_time = time.time()

output(iter_count, best_param, best_gflops, end_time - start_time, function_key)
