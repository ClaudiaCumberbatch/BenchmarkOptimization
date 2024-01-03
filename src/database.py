import sqlite3
import numpy as np
import pandas as pd
import os
import traceback
from abc import ABC, abstractmethod
import sys
from datetime import datetime
from file_utils import *
from predictor import *
from multiprocessing import Process, Queue

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


# 定义抽象类
class database_interactor(ABC):
    def __init__(self, file_interactor):
        self.file_interactor = file_interactor
        config = file_interactor.get_global_config()
        self.table_name = config['queue']
        self.cores = config['core_count']
        path_to_HPL = config['path_to_HPL']
        self.path_to_HPL_exe = os.path.expanduser(path_to_HPL + "xhpl")
        path_to_HPCG = config['path_to_HPCG']
        self.path_to_HPCG_exe = os.path.expanduser(path_to_HPCG + "xhpcg")
        self.mpi = config['mpi']
        self.need_predict = config['need_predict']
        if config['split_pctg'] not in np.arange(0.10, 0.50, 0.05):
            print('split_pctg must be in range [0.1, 0.45], step 0.05, compulsory convert to 0.30')
            self.split_pctg = 0.3
        
        self.split_pctg = config['split_pctg']

    def __del__(self):
        self.close()

    @abstractmethod
    def query(self, param_list, table):
        pass

    @abstractmethod
    def get_data(self, new_param):
        pass

    # 具体方法
    def connect(self, database_name):
        try:
            conn = sqlite3.connect(database_name)
            return conn
        except Exception as e:
            print(f"连接数据库时发生错误: {str(e)}")
            traceback.print_exc()
            sys.exit(1)
            return None

    def store(self, data, table):
        try:
            # 如果data的值都是标量，需要提供一个索引
            if all(isinstance(value, (int, float, str)) for value in data.values()):
                data_df = pd.DataFrame(data, index=[0])
            else:
                data_df = pd.DataFrame(data)
            data_df.to_sql(table, self.conn, if_exists="append", index=False)
            return True
        except Exception as e:
            print(f"写入数据库时发生错误: {str(e)}")
            traceback.print_exc()
            return False
    
    def close(self):
        try:
            self.conn.cursor().close()
            self.conn.close()
            return True
        except Exception as e:
            print(f"关闭数据库连接时发生错误: {str(e)}")
            traceback.print_exc()  
            return False

# 子类实现抽象方法和继承/重写具体方法
class HPL_interactor(database_interactor):
    def __init__(self, file_interactor):
        super().__init__(file_interactor)
        self.name = 'HPL'
        self.predict_table = self.table_name + '_predict'
        self.conn = self.connect('../db/HPL.db')

    def __del__(self):
        super().__del__()

    def query(self, param_list, table):
        '''
        返回最大的Gflops
        原方法声明
        def HPL_query(conn, table, cores, PMAP, SWAP, L1, U, EQUIL, DEPTH, BCAST, RFACT, NDIV, PFACT, NBMIN, N, NB, P, Q):
        '''
        try:
            cursor = self.conn.cursor()
            # 检查表是否存在
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
            table_exists = cursor.fetchone()
            if not table_exists: 
                return []
            cores = param_list[0]
            PMAP = param_list[1]
            SWAP = param_list[2]
            L1 = param_list[3]
            U = param_list[4]
            EQUIL = param_list[5]
            DEPTH = param_list[6]
            BCAST = param_list[7]
            RFACT = param_list[8]
            NDIV = param_list[9]
            PFACT = param_list[10]
            NBMIN = param_list[11]
            N = param_list[12]
            NB = param_list[13]
            P = param_list[14]
            Q = param_list[15]

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

    def get_data(self, new_param):
        def task_HPL(date):
            command = f"{self.mpi} -np {self.cores} {self.path_to_HPL_exe}"
            os.system(f"{command} > ../logs/{date}.out 2> ../logs/{date}.err")
            
        def task_predict(date, q, split_pctg):
            p = predictor()
            # TODO: pctg
            res = p.control(f'../logs/{date}.out', f'../logs/{date}.err', split_pctg)
            q.put(res[0])

        try:
            param_list = [self.cores, new_param["PMAP"], new_param["SWAP"], new_param["L1"], new_param["U"], new_param["EQUIL"], new_param["DEPTH"], new_param["BCAST"], new_param["RFACT"], new_param["NDIV"], new_param["PFACT"], new_param["NBMIN"], new_param["N"], new_param["NB"], self.cores // new_param['Q'], new_param["Q"]]
            result = self.query(param_list, self.table_name)
            # 如果查询结果为空，执行搜索程序，将新结果写入数据库
            if len(result) == 0:
                print(self.file_interactor.write_to_dat('HPL.dat', new_param))
                date = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
                if self.need_predict:
                    result = self.query(param_list, self.predict_table)
                    if len(result) != 0:
                        return result
                    q = Queue() # 用来传递预测结果
                    process_HPL = Process(target=task_HPL, args=(date,))
                    process_HPL.start()
                    process_predict = Process(target=task_predict, args=(date, q, self.split_pctg,))
                    process_predict.start()
                    process_predict.join()
                    result = q.get()
                    data = self.file_interactor.parse_log(f"../logs/{date}.out")
                    data["Time"] = -1
                    data["Gflops"] = result
                    self.store(data, self.predict_table)
                    return result
                else:
                    os.system(f"{self.mpi} -np {self.cores} {self.path_to_HPL_exe} > ../logs/{date}.out 2> ../logs/{date}.err")
                    data = self.file_interactor.parse_log(f"../logs/{date}.out")
                    self.store(data, self.table_name)
                    result = data["Gflops"]
            result = np.max(result)
            return result
        except Exception as e:
            print(f"获取数据时发生错误: {str(e)}")
            traceback.print_exc()  # 打印异常的详细信息，包括行数
            # sys.exit(1)
            return None
        
    
class HPCG_interactor(database_interactor):
    def __init__(self, file_interactor):
        super().__init__(file_interactor)
        self.name = 'HPCG'
        self.conn = self.connect('../db/HPCG.db')

    def __del__(self):
        super().__del__()

    def query(self, param_list, table):
        '''
        原方法声明
        def HPCG_query(conn, table, cores, NX, NY, NZ)
        '''
        try:
            cursor = self.conn.cursor()
            # print('get into HPCG_query')
            # print(table, cores, NX, NY, NZ)
            # print(f"SELECT Gflops FROM {table} WHERE cores={cores} AND NX={NX} AND NY={NY} AND NZ={NZ}")
            # print message about the path of the db file
            NX = param_list[0]
            NY = param_list[1]
            NZ = param_list[2]
            sql = f"SELECT Gflops FROM {self.table_name} WHERE cores={self.cores} AND NX={NX} AND NY={NY} AND NZ={NZ}"
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
        except Exception as e:
            print(f"查询数据库时发生错误: {str(e)}")
            traceback.print_exc()
            return None
        
    def get_data(self, new_param):
        try:
            param_list = [new_param['NX'], new_param['NY'], new_param['NZ'], new_param['Time']]
            result = self.query(param_list, self.table_name)
            # 如果查询结果为空，执行搜索程序，将新结果写入数据库
            if len(result) == 0: # type: ignore
                # print('did not find the result in the database')
                print(self.file_interactor.write_to_dat('hpcg.dat', new_param))
                date = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
                os.system(f"{self.mpi} -np {self.cores} {self.path_to_HPCG_exe} > ../logs/{date}.out 2> ../logs/{date}.err" )
                out_file_path = f"../logs/{date}.out"
                err_file_path = f"../logs/{date}.err"
                
                # check if HPCG runs successfully
                # If params out of range, the .out file will not be empty
                # If the params are invalid, that is the ratio of min(NX, NY, NZ) to max(NX, NY, NZ) is less than 1/8,
                # the .err file will not be empty
                if os.path.getsize(out_file_path) == 0 and os.path.getsize(err_file_path) == 0:
                    print("HPCG runs successfully")
                    # HPCG output file name is like: HPCG-Benchmark_3.1_2023-11-11_15-55-20.txt result
                    # the time in the output .txt file is the end time 
                    HPCG_file_names = [file for file in os.listdir(".") if file.startswith("HPCG-Benchmark") and file.endswith(".txt")]
                    HPCG_file_names.sort(reverse=True)
                    # As all HPCG output .txt files are sorted by descending order of time,
                    # the first file is the latest one
                    HPCG_file_name = HPCG_file_names[0]
                    data = self.file_interactor.parse_log(HPCG_file_name)
                elif os.path.getsize(out_file_path) != 0:
                    print("HPCG failed to run: problem sizes out of range")
                    data = {
                        "cores": self.cores,
                        "NX": new_param["NX"],
                        "NY": new_param["NY"],
                        "NZ": new_param["NZ"],
                        "Time": new_param["Time"],
                        "Gflops": -1
                    }
                else:
                    print("HPCG failed to run: invalid params")
                    data = {
                        "cores": self.cores,
                        "NX": new_param["NX"],
                        "NY": new_param["NY"],
                        "NZ": new_param["NZ"],
                        "Time": new_param["Time"],
                        "Gflops": -1
                    }
                self.store(data, self.table_name)
                result = data["Gflops"]       
            result = np.max(result)
            return result
        except Exception as e:
            print(f"获取数据时发生错误: {str(e)}")
            traceback.print_exc()  
            return None
