from file_utils import *
import random
from database import *

def random_search_HPL(node_count, core_count, iter_count):
    # 定义参数范围
    '''
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
    '''
    param_ranges = get_HPL_params()
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
        tempt_gflops = get_HPL_data(random_params)
        if tempt_gflops > best_gflops:
            best_gflops = tempt_gflops
            best_param = random_params
    return best_param, best_gflops

    
def random_search_HPCG(node_count, core_count, iter_count):
    param_ranges = get_HPCG_params()
    best_param = {}
    best_gflops = 0.0
    for i in range(iter_count):
        random_params = {}
        # for param, param_range in param_ranges.items():
        #     if len(param_range) > 2:
        #         random_value = random.choice(param_range)
        #     else:
        #         random_value = random.randint(param_range[0], param_range[1])
        #     random_params[param] = random_value
        # for param, param_range in param_ranges.items():
        #     random_value = random.choice(param_range)
        #     random_params[param] = random_value
        
        random_params['NX'] = random.choice(param_ranges['NX'])
        random_params['NY'] = random.choice(param_ranges['NY'])
        random_params['NZ'] = random.choice(param_ranges['NZ'])
        # random_params['NX'] = 32
        # random_params['NY'] = 16
        # random_params['NZ'] = 32
        
        # random_params['NX'] = random.randint(param_ranges['NX'][0], param_ranges['NX'][1])
        # random_params['NY'] = random.randint(param_ranges['NY'][0], param_ranges['NY'][1])
        # random_params['NZ'] = random.randint(param_ranges['NZ'][0], param_ranges['NZ'][1])
        
        
        # 256 + 256 + 96 = 608
        # while(random_params['NX'] + random_params['NY'] + random_params['NZ'] > 608):
        #     random_params['NX'] = random.choice(param_ranges['NX'])
        #     random_params['NY'] = random.choice(param_ranges['NY'])
        #     random_params['NZ'] = random.choice(param_ranges['NZ'])
        random_params['Time'] = param_ranges['Time']
        print(f"params of the {i+1} th iteration: ")
        print(random_params)
        tempt_gflops = get_HPCG_data(random_params)
        print(f"Gflops of this iteration: {tempt_gflops}")
        if tempt_gflops > best_gflops: 
            best_gflops = tempt_gflops
            best_param = random_params
        print(f"The currnet best Gflops:  {best_gflops}")
        print(f"The currnet best params:  {best_param}")
        print()
    return best_param, best_gflops
        


    