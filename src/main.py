import argparse
from random_search import *
import yaml
from file_utils import *
from output_utils import *

config = parse_config_yaml()

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
    "random_search_HPCG": random_search_HPCG
}
func = switcher.get(function_key, "Invalid choice of algorithm preference and benchmark")
best_param, best_gflops = func(node_count, core_count, iter_count)

output(best_param, best_gflops)
