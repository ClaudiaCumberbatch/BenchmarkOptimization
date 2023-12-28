import pandas as pd
import numpy as np
import time
import joblib
import os

class predictor():
    def __init__(self):
        pass

    def read_log(self, log_path):
        def extract_data(lines):
            data = []
            for line in lines:
                Gflops = float(line.split()[-1].split("=")[-1])
                Fraction = float(line.split()[-2].split("=")[-1].strip("%"))/100
                data.append([Gflops, Fraction])
            df = pd.DataFrame(data, columns=["Gflops", "Fraction"])
            return df
        
        ex_input = []
        with open(log_path, 'r') as f:
            lines = f.readlines()
            for i in range(len(lines)):
                line = lines[i]
                if "BAD" in line:
                    return pd.DataFrame(), False
                if "Column=" in line:
                    ex_input.append(line)
        ex_output = extract_data(ex_input)
        return ex_output, True
    
    def predict(self, log_df, model_path):
        with open(model_path, 'rb') as file:
            model = joblib.load(file)
        if log_df.shape[0] < model.n_features_in_:
            log_df = log_df._append([log_df.iloc[-1]]*(model.n_features_in_-log_df.shape[0]), ignore_index=True)
        gflops = log_df['Gflops'].values
        gflops = np.reshape(gflops, (1, -1))
        return model.predict(gflops)


    def is_current_user(self, pid):
        # 获取当前用户的UID
        current_uid = os.getuid()
        # 构造进程的status文件路径
        status_file = f'/proc/{pid}/status'
        # 打开并读取status文件
        with open(status_file, 'r') as f:
            lines = f.readlines()
        # 查找'Uid:'字段
        for line in lines:
            if line.startswith('Uid:'):
                # 提取用户ID
                print(line)
                uid = int(line.split()[1])
                # 比较用户ID
                return uid == current_uid
        # 如果没有找到'Uid:'字段，返回False
        return False


    def control(self, log_path, err_path, pre_pctg, HPL_pids):
        '''
        读log文件, 判断是否达到要求, 终止HPL运行
        '''
        # 每5秒读取一次log文件
        while(True):
            time.sleep(5)
            log_df, success = self.read_log(log_path)
            with open(err_path, 'r') as f:
                lines = f.readlines()
                if len(lines) != 0:
                    success = False
            if not success:
                return [-1]
            if log_df.shape[0] == 0:
                continue
            # 终止HPL运行, 进行预测
            if (log_df.iloc[-1]['Fraction'] >= pre_pctg): 
                for HPL_pid in HPL_pids:
                    # if self.is_current_user(int(HPL_pid)):
                    # TODO: os.kill无法终止全部mpi运行
                    os.kill(int(HPL_pid), 9)
                res = self.predict(log_df, '../model/model_0.3.pkl')
                return res
                
