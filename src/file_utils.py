import traceback

    # new_param = {
    #     "N": N,
    #     "NB": NB,
    #     "PMAP": PMAP,
    #     "Q": Q,  # 请将core_count替换为实际的核心数
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
        with open('HPL.dat', 'w') as file:
            file.write("HPLinpack benchmark input file\n")
            file.write("Innovative Computing Laboratory, University of Tennessee\n")
            file.write("HPL.out      output file name (if any)\n")
            file.write("6            device out (6=stdout,7=stderr,file)\n")
            file.write("1            # of problems sizes (N)\n")
            file.write(f"{new_param['N']}        Ns\n")
            file.write("1            # of NBs\n")
            file.write(f"{new_param['NB']}         NBs\n")
            file.write(f"{new_param['PMAP']}            PMAP process mapping (0=Row-,1=Column-major)\n")
            file.write("1            # of process grids (P x Q)\n")
            file.write(f"{core_count//new_param['Q']}           Ps\n")
            file.write(f"{new_param['Q']}           Qs\n")
            file.write("-1         threshold\n")
            file.write("1           # of panel fact\n")
            file.write(f"{new_param['PFACT']}            PFACTs (0=left, 1=Crout, 2=Right)\n")
            file.write("1            # of recursive stopping criterium\n")
            file.write(f"{new_param['NBMIN']}            NBMINs\n")
            file.write("1           # of panels in recursion\n")
            file.write(f"{new_param['NDIV']}            NDIVs\n")
            file.write("1            # of recursive panel fact.\n")
            file.write(f"{new_param['RFACT']}            RFACTs (0=left, 1=Crout, 2=Right)\n")
            file.write("1            # of broadcast\n")
            file.write(f"{new_param['BCAST']}            BCASTs (0=1rg,1=1rM,2=2rg,3=2rM,4=Lng,5=LnM)\n")
            file.write("1            # of lookahead depth\n")
            file.write(f"{new_param['DEPTH']}            DEPTHs (>=0)\n")
            file.write(f"{new_param['SWAP']}            SWAP (0=bin-exch,1=long,2=mix)\n")
            file.write("64           swapping threshold\n")
            file.write(f"{new_param['L1']}            L1 in (0=transposed,1=no-transposed) form\n")
            file.write(f"{new_param['U']}            U  in (0=transposed,1=no-transposed) form\n")
            file.write(f"{new_param['EQUIL']}            Equilibration (0=no,1=yes)\n")
            file.write("8            memory alignment in double (> 0)\n")
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
    GFLOPS = -1
    parameters = {}
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