from file_utils import *
import random
from database import *

def random_search_HPL(node_count, core_count, iter_count):
    # 定义参数范围
    factors = []
    for i in range(1, core_count + 1):
        if core_count % i == 0:
            factors.append(i)
    param_ranges = {
        "N": [10, 100000],
        "NB": [10, 1000],
        "PMAP": [0, 1],
        "Q": factors,  # 请将core_count替换为实际的核心数
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
    best_gflops = 0
    for _ in range(iter_count):
        random_params = {}
        for param, param_range in param_ranges.items():
            if len(param_range) > 2:
                random_value = random.choice(param_range)
            else:
                random_value = random.randint(param_range[0], param_range[1])
            random_params[param] = random_value
        tempt_gflops = get_HPL_data(core_count, random_params)
        if tempt_gflops > best_gflops:
            best_gflops = tempt_gflops
            best_param = random_params
    return best_param, best_gflops

    
def random_search_HPCG(node_count, core_count, iter_count):
    # change the benchmark time
    Time = 1860
    # the bound of multiplier (both included)
    lower_bound = 2
    upper_bound = 30
    for _ in range(iter_count):
        # generate the multiplier to 8
        NX = random.randint(lower_bound, upper_bound)
        NY = random.randint(lower_bound, upper_bound)
        NZ = random.randint(lower_bound, upper_bound)
        random_params = {
            "NX": NX,
            "NY": NY,
            "NZ": NZ
        }
        res = write_to_HPCG_dat(random_params, Time)
        print(res)
        


    