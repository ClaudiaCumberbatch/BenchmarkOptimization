import sys

# 文件读取
def read_file(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()
        return lines

# 文件写入
def write_file(file_name, new_parameters):
    try:
        with open(file_name, 'w') as file:
            file.write("HPLinpack benchmark input file\n"+
                        "Innovative Computing Laboratory, University of Tennessee\n"+
                        "HPL.out      output file name (if any)\n"+"6\n")
            for index in range(4,30):
                if index in [4,6,9,13,15,17,19,21,23]:
                    file.write("1\n")
                elif index == 10:
                    file.write(str(int(core) // new_parameters[0]) + "\n")
                elif index == 12:
                    file.write("-1\n")
                elif index == 26:
                    file.write("64\n")
                else:
                    file.write(str(new_parameters.pop(0))+"\n")
            file.write("8")
        return "文件写入成功"
    except Exception as e:
        return f"写入文件时发生错误: {str(e)}"

def parse_lines(content, parameters):
    for index, line in enumerate(lines):
        if index in [0,1,2,3,4,6,9,10,12,13,15,17,19,21,23,26,30]:
            continue
        parts = line.split()
        parameters.append(int(parts[0]))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Invalid argument")
        sys.exit(1)
    else:
        core = sys.argv[1]
    # 读取文件
    input_file_name = "HPL.dat"
    lines = read_file(input_file_name)

    parameters = []
    parse_lines(lines, parameters)

    Ns=[80000,90000,1000] #6
    NBs=[120,360,4] #8
    PMAP=[0,1,1] #9
    Qs=[1,core,1] #12
    PFACTs=[0,2,1] #15
    NBMINs=[2,16,2] #17
    NDIVs=[2,8,1] #19
    RFACTs=[0,2,1] #21
    BCASTs=[0,5,1] #23
    DEPTHs=[0,6,1] #25
    SWAP=[0,2,1] #26
    L1=[0,1,1] #28
    U=[0,1,1] #29
    Equilibration=[0,1,1] #30
    lower_threshold = [Ns[0],NBs[0],PMAP[0],Qs[0],PFACTs[0],NBMINs[0],NDIVs[0],RFACTs[0],BCASTs[0],DEPTHs[0],SWAP[0],L1[0],U[0],Equilibration[0]]
    upper_threshold = [Ns[1],NBs[1],PMAP[1],Qs[1],PFACTs[1],NBMINs[1],NDIVs[1],RFACTs[1],BCASTs[1],DEPTHs[1],SWAP[1],L1[1],U[1],Equilibration[1]]
    interval = [Ns[2],NBs[2],PMAP[2],Qs[2],PFACTs[2],NBMINs[2],NDIVs[2],RFACTs[2],BCASTs[2],DEPTHs[2],SWAP[2],L1[2],U[2],Equilibration[2]]
    
    new_parameters = []
    flag = True
    for i in range(13, -1, -1):
        if flag:
            tempt_param = parameters[i] + interval[i]
            if tempt_param > upper_threshold[i]:
                tempt_param = lower_threshold[i]
            else:
                flag = False
            if i == 3:
                while core % tempt_param != 0:
                    tempt_param += interval[i]
        else:
            tempt_param = parameters[i]
        new_parameters.insert(0,tempt_param)


    # 写入文件
    output_file_name = "HPL.dat"
    write_result = write_file(output_file_name, new_parameters)
    print(write_result)