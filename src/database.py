import sqlite3
import numpy as np
import pandas as pd
import os
import traceback
from datetime import datetime
import file_utils

PMAP_dic = {
    0: "Row-major",
    1: "Column-major"
}

SWAP_dic = {
    0: "Binary-exchange",
    1: "Spread-roll",
    2: "Mix"
}

L1_dic = {
    0: "transposed",
    1: "no-transposed"
}

U_dic = {
    0: "transposed",
    1: "no-transposed"
}

EQUIL_dic = {
    0: "no",
    1: "yes"
}

RFACT_dic = {
    0: "Left",
    1: "Crout",
    2: "Right"
}

PFACT_dic = {
    0: "Left",
    1: "Crout",
    2: "Right"
}

BCAST_dic = {
    0: "1ring",
    1: "1ringM",
    2: "2ring",
    3: "2ringM",
    4: "Blong",
    5: "BlongM"
}

# 连接数据库
def connect(database_name):
    try:
        conn = sqlite3.connect(database_name)
        return conn
    except Exception as e:
        print(f"连接数据库时发生错误: {str(e)}")
        traceback.print_exc()
        return None

# 将dataframe格式的数据写入数据库
def store(conn, data, table_name):
    try:
        # 如果data的值都是标量，需要提供一个索引
        if all(isinstance(value, (int, float, str)) for value in data.values()):
            data_df = pd.DataFrame(data, index=[0])
        else:
            data_df = pd.DataFrame(data)
        
        data_df.to_sql(table_name, conn, if_exists="append", index=False)
        return True

    except Exception as e:
        print(f"写入数据库时发生错误: {str(e)}")
        traceback.print_exc()
        return False

# 从数据库中查询，可能为空  
def HPL_query(conn, table, cores, PMAP, SWAP, L1, U, EQUIL, DEPTH, BCAST, RFACT, NDIV, PFACT, NBMIN, N, NB, P, Q):
    try:
        cursor = conn.cursor()
        PMAP = PMAP_dic[PMAP]
        SWAP = SWAP_dic[SWAP]
        L1 = L1_dic[L1]
        U = U_dic[U]
        EQUIL = EQUIL_dic[EQUIL]
        RFACT = RFACT_dic[RFACT]
        PFACT = PFACT_dic[PFACT]
        BCAST = BCAST_dic[BCAST]
        sql = f"SELECT Gflops FROM {table} WHERE cores={cores} AND PMAP='{PMAP}' AND SWAP='{SWAP}' AND L1='{L1}' AND U='{U}' AND EQUIL='{EQUIL}' AND DEPTH={DEPTH} AND BCAST='{BCAST}' AND RFACT='{RFACT}' AND NDIV={NDIV} AND PFACT='{PFACT}' AND NBMIN={NBMIN} AND N={N} AND NB={NB} AND P={P} AND Q={Q}"
        cursor.execute(sql)
        result = cursor.fetchall()
        return result
    except Exception as e:
        print(f"查询数据库时发生错误: {str(e)}")
        traceback.print_exc()
        return None

def HPCG_query(conn, table, cores, NX, NY, NZ):
    try:
        cursor = conn.cursor()
        # print('get into HPCG_query')
        # print(table, cores, NX, NY, NZ)
        # print(f"SELECT Gflops FROM {table} WHERE cores={cores} AND NX={NX} AND NY={NY} AND NZ={NZ}")
        # print message about the path of the db file
        sql = f"SELECT Gflops FROM {table} WHERE cores={cores} AND NX={NX} AND NY={NY} AND NZ={NZ}"
        cursor.execute(sql)
        result = cursor.fetchall()
        return result
    except Exception as e:
        print(f"查询数据库时发生错误: {str(e)}")
        traceback.print_exc()
        return None
    
# 关闭数据库连接
def close(conn):
    try:
        conn.cursor().close()
        conn.close()
        return True
    except Exception as e:
        print(f"关闭数据库连接时发生错误: {str(e)}")
        traceback.print_exc()  
        return False

# 和数据库交互的全流程
def get_HPL_data(new_param):
    config = file_utils.parse_config_yaml()
    database_name = '../db/HPL.db'
    table_name = 'table1'
    cores = config['core_count']
    path_to_HPL = config['path_to_HPL']
    path_to_HPL_exe = os.path.expanduser(path_to_HPL + "xhpl")
    try:
        conn = connect(database_name)
        if conn is None:
            raise Exception("数据库连接失败")
        result = HPL_query(conn, table_name, cores, new_param["PMAP"], new_param["SWAP"], new_param["L1"], new_param["U"], new_param["EQUIL"], new_param["DEPTH"], new_param["BCAST"], new_param["RFACT"], new_param["NDIV"], new_param["PFACT"], new_param["NBMIN"], new_param["N"], new_param["NB"], cores // new_param['Q'], new_param["Q"])
        # 如果查询结果为空，执行搜索程序，将新结果写入数据库
        if len(result) == 0:
            print(file_utils.write_to_HPL_dat('HPL.dat', new_param, cores))
            date = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            # print("executing HPL...")
            # close(conn)
            # return
            os.system(f"mpiexec.hydra -np {cores} {path_to_HPL_exe} > ../logs/{date}.out 2> ../logs/{date}.err")
            data = file_utils.parse_HPL_dat(f"../logs/{date}.out")
            store(conn, data, table_name)
            result = data["Gflops"]
        close(conn)
        result = np.mean(result)
        return result
    except Exception as e:
        print(f"获取数据时发生错误: {str(e)}")
        traceback.print_exc()  # 打印异常的详细信息，包括行数
        return None

def get_HPCG_data(new_param):
    # print('get into function get_HPCG_data')
    # for test
    config = file_utils.parse_config_yaml()
    database_name = '../db/HPCG.db'
    table_name = 'hpcg'
    cores = config['core_count']
    path_to_HPCG = config['path_to_HPCG']
    path_to_HPCG_exe = os.path.expanduser(path_to_HPCG+"xhpcg")
    try:
        conn = connect(database_name)
        if conn is None:
            raise Exception("数据库连接失败")
        result = HPCG_query(conn, table_name, cores, new_param["NX"], new_param["NY"], new_param["NZ"])
        # 如果查询结果为空，执行搜索程序，将新结果写入数据库
        if len(result) == 0: # type: ignore
            # print('did not find the result in the database')
            print(file_utils.write_to_HPCG_dat('hpcg.dat', new_param))
            date = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            os.system(f"mpiexec.hydra -np {cores} {path_to_HPCG_exe} > ../logs/{date}.out 2> ../logs/{date}.err" )
            out_file_path = f"../logs/{date}.out"
            err_file_path = f"../logs/{date}.err"
            # not necessary because the .out file cannot show the benchmark
            # HPCG output file name is like: HPCG-Benchmark_3.1_2023-11-11_15-55-20.txt result
            # the time in the output .txt file is the end time 
            HPCG_file_names = [file for file in os.listdir(".") if file.startswith("HPCG-Benchmark") and file.endswith(".txt")]
            HPCG_file_names.sort(reverse=True)
            # As all hpcg output .txt files are sorted by descending order of time,
            # the first file is the latest one
            HPCG_file_name = HPCG_file_names[0]
            if os.path.getsize(out_file_path) == 0 and os.path.getsize(err_file_path) == 0:
                print("HPCG runs successfully")
                data  = file_utils.parse_HPCG_txt(HPCG_file_name)
            elif os.path.getsize(out_file_path) != 0:
                print("HPCG failed to run: problem sizes out of range")
                data = {
                    "cores": cores,
                    "NX": new_param["NX"],
                    "NY": new_param["NY"],
                    "NZ": new_param["NZ"],
                    "Time": new_param["Time"],
                    "Gflops": -1
                }
            else:
                print("HPCG failed to run: invalid params")
                data = {
                    "cores": cores,
                    "NX": new_param["NX"],
                    "NY": new_param["NY"],
                    "NZ": new_param["NZ"],
                    "Time": new_param["Time"],
                    "Gflops": -1
                }
            
            
            # hpcg output file name is like: hpcg20231126T023554.txt
            # hpcg_file_names = [file for file in os.listdir(".") if file.startswith("hpcg") and file.endswith(".txt")]
            # hpcg_file_names.sort(reverse=True)
            # hpcg_file_name = hpcg_file_names[0]
            # with open(hpcg_file_name, 'r') as file:
            #     first_line = file.readline()
            # If the first line of the hpcg output file is empty or invalid, it means that the benchmark failed
            # hpcg file of invalid params is like (the below 2 lines):
            # The local problem sizes (16,232,176) are invalid because the ratio min(x,y,z)/max(x,y,z)=0.0689655 is too small (at least 0.125 is required).
            # The shape should resemble a 3D cube. Please adjust and try again.
            # if first_line == "" :
            #     print("HPCG failed to run: problem sizes out of range")
            #     data = {
            #         "cores": cores,
            #         "NX": new_param["NX"],
            #         "NY": new_param["NY"],
            #         "NZ": new_param["NZ"],
            #         "Time": new_param["Time"],
            #         "Gflops": -1
            #     }
            # elif "invalid" in first_line:
            #     print("HPCG failed to run: invalid params")
            #     data = {
            #         "cores": cores,
            #         "NX": new_param["NX"],
            #         "NY": new_param["NY"],
            #         "NZ": new_param["NZ"],
            #         "Time": new_param["Time"],
            #         "Gflops": -1
            #     }
            # else:
            #     data  = file_utils.parse_HPCG_txt(HPCG_file_name)
                
                
            # check if the file name is generated in this iteration
            # if not, it means that it was generated before, and the params in this iteration are not valid, write gflops=-1 into the database
            # time_string = file_name.split("_")[2] + "_" + file_name.split("_")[3].split(".")[0]
            # file_time = datetime.strptime(time_string, "%Y-%m-%d_%H-%M-%S")
            # current_time = datetime.now()
            # time_difference = current_time - file_time
            # # if dif is less than 10 minutes, valid
            # if time_difference.seconds < 600:
            #     data  = file_utils.parse_HPCG_txt(file_name)
            # else:
            #     print("invalid params")
            #     data = {
            #         "cores": cores,
            #         "NX": new_param["NX"],
            #         "NY": new_param["NY"],
            #         "NZ": new_param["NZ"],
            #         "Time": new_param["Time"],
            #         "Gflops": -1
            #     }
            store(conn, data, table_name)
            result = data["Gflops"]       
        close(conn)
        result = np.mean(result)
        return result
    except Exception as e:
        print(f"获取数据时发生错误: {str(e)}")
        traceback.print_exc()  
        return None
