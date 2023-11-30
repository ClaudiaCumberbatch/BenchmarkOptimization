from calendar import c
import traceback
import yaml

    # new_param = {
    #     "N": N,
    #     "NB": NB,
    #     "PMAP": PMAP,
    #     "Q": Q,  
    #     "PFACT": PFACT,
    #     "NBMIN": NBMIN,
    #     "NDIV": NDIV,
    #     "RFACT": RFACT,
    #     "BCAST": BCAST,
    #     "DEPTH": DEPTH,
    #     "SWAP": SWAP,
    #     "L1": L1,
    #     "U": U,
    #     "EQUIL": EQUIL,
    #     "Time": Time,
    #     "Gflops": Gflops
    # }  
def write_to_HPL_dat(file_name, new_param, core_count):
    try:
        with open(file_name, 'w') as file:
            file.write("HPLinpack benchmark input file\n")
            file.write("In  novative Computing Laboratory, University of Tennessee\n")
            file.write("{:<30} {}\n".format("HPL.out", "output file name (if any)"))
            file.write("{:<30} {}\n".format("6", "device out (6=stdout,7=stderr,file)"))
            file.write("{:<30} {}\n".format("1", "# of problems sizes (N)"))
            file.write("{:<30} {}\n".format(f"{new_param['N']}", "Ns"))
            file.write("{:<30} {}\n".format("1", "# of NBs"))
            file.write("{:<30} {}\n".format(f"{new_param['NB']}", "NBs"))
            file.write("{:<30} {}\n".format(f"{new_param['PMAP']}", "PMAP process mapping (0=Row-,1=Column-major)"))
            file.write("{:<30} {}\n".format("1", "# of process grids (P x Q)"))
            file.write("{:<30} {}\n".format(f"{core_count//new_param['Q']}", "Ps"))
            file.write("{:<30} {}\n".format(f"{new_param['Q']}", "Qs"))
            file.write("{:<30} {}\n".format("-1", "threshold"))
            file.write("{:<30} {}\n".format("1", "# of panel fact"))
            file.write("{:<30} {}\n".format(f"{new_param['PFACT']}", "PFACTs (0=Left, 1=Crout, 2=Right)"))
            file.write("{:<30} {}\n".format("1", "# of recursive stopping criterium"))
            file.write("{:<30} {}\n".format(f"{new_param['NBMIN']}", "NBMINs"))
            file.write("{:<30} {}\n".format("1", "# of panels in recursion"))
            file.write("{:<30} {}\n".format(f"{new_param['NDIV']}", "NDIVs"))
            file.write("{:<30} {}\n".format("1", "# of recursive panel fact."))
            file.write("{:<30} {}\n".format(f"{new_param['RFACT']}", "RFACTs (0=Left, 1=Crout, 2=Right)"))
            file.write("{:<30} {}\n".format("1", "# of broadcast"))
            file.write("{:<30} {}\n".format(f"{new_param['BCAST']}", "BCASTs (0=1rg,1=1rM,2=2rg,3=2rM,4=Lng,5=LnM)"))
            file.write("{:<30} {}\n".format("1", "# of lookahead depth"))
            file.write("{:<30} {}\n".format(f"{new_param['DEPTH']}", "DEPTHs (>=0)"))
            file.write("{:<30} {}\n".format(f"{new_param['SWAP']}", "SWAP (0=bin-exch,1=long,2=mix)"))
            file.write("{:<30} {}\n".format("64", "swapping threshold"))
            file.write("{:<30} {}\n".format(f"{new_param['L1']}", "L1 in (0=transposed,1=no-transposed) form"))
            file.write("{:<30} {}\n".format(f"{new_param['U']}", "U  in (0=transposed,1=no-transposed) form"))
            file.write("{:<30} {}\n".format(f"{new_param['EQUIL']}", "Equilibration (0=no,1=yes)"))
            file.write("{:<30} {}\n".format("8", "memory alignment in double (> 0)"))
        return "文件写入成功"
    except Exception as e:
        traceback.print_exc()
        return f"写入文件时发生错误: {str(e)}"


def parse_HPL_dat(filename):
    '''
    解析HPL_dat文件
    返回类型为map
    如果改组参数运行错误，Time和Gflops均会被设置成-1;对于数值参数，Time和Gflops转成float，其余转成int;非数值参数为字符串类型
    '''
    with open(filename, 'r') as file:
        lines = file.readlines()

    # 遍历每一行并解析数据
    # N      :   80000 
    # NB     :     120 
    # PMAP   : Row-major process mapping
    # P      :       4 
    # Q      :       1 
    # PFACT  :    Left 
    # NBMIN  :       1 
    # NDIV   :       2 
    # RFACT  :    Left 
    # BCAST  :   1ring 
    # DEPTH  :       0 
    # SWAP   : Binary-exchange
    # L1     : transposed form
    # U      : transposed form
    # EQUIL  : yes
    # ALIGN  : 8 double precision words
    Time = -1
    Gflops = -1
    for i in range(len(lines)):
        line = lines[i]
        if "The following parameter values will be used:" in line: 
            i += 2
            N = int(lines[i].split()[2])
            NB = int(lines[i + 1].split()[2])
            PMAP = lines[i + 2].split()[2]
            P = int(lines[i + 3].split()[2])
            Q = int(lines[i + 4].split()[2])
            PFACT = lines[i + 5].split()[2]
            NBMIN = int(lines[i + 6].split()[2])
            NDIV = int(lines[i + 7].split()[2])
            RFACT = lines[i + 8].split()[2]
            BCAST = lines[i + 9].split()[2]
            DEPTH = int(lines[i + 10].split()[2])
            SWAP = lines[i + 11].split()[2]
            L1 = lines[i + 12].split()[2]
            U = lines[i + 13].split()[2]
            EQUIL = lines[i + 14].split()[2]

        elif "T/V                N    NB     P     Q               Time                 Gflops" in line:
            line = lines[i + 2]
            parts = line.split()
            Time = float(parts[-2])
            Gflops = float(parts[-1])

    param = {
        "cores": P * Q,
        "N": N,
        "NB": NB,
        "PMAP": PMAP,
        "P": P,
        "Q": Q,  # 请将core_count替换为实际的核心数
        "PFACT": PFACT,
        "NBMIN": NBMIN,
        "NDIV": NDIV,
        "RFACT": RFACT,
        "BCAST": BCAST,
        "DEPTH": DEPTH,
        "SWAP": SWAP,
        "L1": L1,
        "U": U,
        "EQUIL": EQUIL,
        "Time": Time,
        "Gflops": Gflops
    }  
    return param

def write_to_HPCG_dat(file_name, new_param):
    try:
        with open(file_name, 'w') as file:
            file.write("HPCG benchmark input file\n")
            file.write("Sandia National Laboratories; University of Tennessee, Knoxville\n")
            file.write(f"{new_param['NX']} {new_param['NY']} {new_param['NZ']}\n")
            file.write(f"{new_param['Time']}")
        return "hpcg.dat write successfully"
    except Exception as e:
        traceback.print_exc()
        return f"Error in hpcg.dat write: {str(e)}" 


def parse_HPCG_txt(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        
    PD_index = 11
    # the index of the line Processor Dimensions::npx=
    npx = int(lines[PD_index].split("=")[1])
    npy = int(lines[PD_index + 1].split("=")[1])
    npz = int(lines[PD_index + 2].split("=")[1])
    
    NX_index = 15
    NX = int(lines[NX_index].split("=")[1])
    NY = int(lines[NX_index + 1].split("=")[1])
    NZ = int(lines[NX_index + 4].split("=")[1])

    Gflops_index = 118
    Gflops = float(lines[Gflops_index].split("=")[1])

    # the total benchmark time in sec
    Time_index = 89
    Time = float(lines[Time_index].split("=")[1]) 

    param = {
        "cores": npx * npy * npz,
        "NX": NX,
        "NY": NY,
        "NZ": NZ,
        "Time": Time,
        "Gflops": Gflops
    }
    return param

    
def parse_config_yaml():
    with open('../config/config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    # 定义P、Q范围
    factors = []
    core_count = config['core_count']
    for i in range(1, core_count + 1):
        if core_count % i == 0:
            factors.append(i)
    config['Q'] = factors
    
    # get HPCG NX NY NZ range
    N = []
    for i in range(config['N'][0], config['N'][1] + 1):
        if i % 8 == 0:
            N.append(i)
    config['NX'] = N
    config['NY'] = N
    config['NZ'] = N
    return config

def get_HPL_params():
    config = parse_config_yaml()
    param_ranges = {
        "N": config['N'],
        "NB": config['NB'],
        "PMAP": config['PMAP'],
        "Q": config['Q'], 
        "PFACT": config['PFACT'],
        "NBMIN": config['NBMIN'],
        "NDIV": config['NDIV'],
        "RFACT": config['RFACT'],
        "BCAST": config['BCAST'],
        "DEPTH": config['DEPTH'],
        "SWAP": config['SWAP'],
        "L1": config['L1'],
        "U": config['U'],
        "EQUIL": config['EQUIL']
    }
    return param_ranges

def get_HPCG_params():
    config = parse_config_yaml()
    param_ranges = {
        "NX": config['NX'],
        "NY": config['NY'],
        "NZ": config['NZ'],
        "Time": config['Time']
    }
    return param_ranges
