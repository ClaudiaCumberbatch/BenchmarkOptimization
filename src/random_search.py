from file_utils import *
import random

def random_search_HPL(node_count, core_count, iter_count):
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
    best_param = {}
    for _ in range(iter_count):
        random_params = {}
        for param, param_range in param_ranges.items():
            random_value = random.randint(param_range[0], param_range[1])
            random_params[param] = random_value
        res = write_to_HPL_dat("HPL.dat", random_params, core_count)
        print(res)
    
    