import argparse
from random_search import *

# 创建命令行参数解析器
parser = argparse.ArgumentParser(description="Command line arguments parser")

# 添加命令行参数
parser.add_argument("--core_count", type=int, help="Number of CPU cores")
parser.add_argument("--node_count", type=int, help="Number of nodes")
parser.add_argument("--algorithm_preference", type=str, help="Algorithm preference", choices=["random_search"])
parser.add_argument("--iter_count", type=int, help="Number of iterations")
parser.add_argument("--benchmark", type=str, help="Benchmark name", choices=["HPL", "HPCG"])

# 解析命令行参数
args = parser.parse_args()

# 获取解析后的参数值
core_count = args.core_count
node_count = args.node_count
algorithm_preference = args.algorithm_preference
iter_count = args.iter_count
benchmark = args.benchmark

# 根据benchmark参数调用不同的函数
function_key = algorithm_preference + "_" + benchmark
switcher = {
    "random_search_HPL": random_search_HPL
}
func = switcher.get(function_key, "Invalid choice of algorithm preference and benchmark")
func(node_count, core_count, iter_count)
