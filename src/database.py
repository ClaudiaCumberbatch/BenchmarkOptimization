import sqlite3
import os
import file_utils

# 连接数据库
def connect(database_name):
    try:
        conn = sqlite3.connect(database_name)
        return conn
    except Exception as e:
        print(f"连接数据库时发生错误: {str(e)}")
        return None

# 将dataframe格式的数据写入数据库
def store(conn, data_df, table_name):
    try:
        data_df.to_sql(table_name, conn, if_exists="append", index=False)
        return True
    except Exception as e:
        print(f"写入数据库时发生错误: {str(e)}")
        return False

# 从数据库中查询，可能为空  
def query(conn, cores, PMAP, SWAP, L1, U, EQUIL, DEPTH, BCAST, RFACT, NDIV, PFACT, NBMIN, N, NB, P, Q):
    try:
        cursor = conn.cursor()
        sql = f"SELECT * FROM HPL WHERE cores={cores} AND PMAP={PMAP} AND SWAP={SWAP} AND L1={L1} AND U={U} AND EQUIL={EQUIL} AND DEPTH={DEPTH} AND BCAST={BCAST} AND RFACT={RFACT} AND NDIV={NDIV} AND PFACT={PFACT} AND NBMIN={NBMIN} AND N={N} AND NB={NB} AND P={P} AND Q={Q}"
        cursor.execute(sql)
        result = cursor.fetchall()
        return result
    except Exception as e:
        print(f"查询数据库时发生错误: {str(e)}")
        return None
    
# 关闭数据库连接
def close(conn):
    try:
        conn.cursor().close()
        conn.close()
        return True
    except Exception as e:
        print(f"关闭数据库连接时发生错误: {str(e)}")
        return False

# 和数据库交互的全流程
def get_HPL_data(database_name, table_name, cores, new_param):
    try:
        conn = connect(database_name)
        if conn is None:
            return None
        result = query(conn, cores, new_param["PMAP"], new_param["SWAP"], new_param["L1"], new_param["U"], new_param["EQUIL"], new_param["DEPTH"], new_param["BCAST"], new_param["RFACT"], new_param["NDIV"], new_param["PFACT"], new_param["NBMIN"], new_param["N"], new_param["NB"], new_param["P"], new_param["Q"])
        # 如果查询结果为空，执行搜索程序，将新结果写入数据库
        if len(result) == 0:
            file_utils.write_to_HPL_dat('HPL.dat', new_param, cores)
            date = os.system("date")
            os.system(f"mpiexec.hydra -np {cores} ./xhpl > ../result/{cores}/{date}.out 2> ../result/{cores}/{date}.err")
            result = file_utils.parse_HPL_out(f"../result/{cores}/{date}.out")
            store(conn, result, table_name)
        close(conn)
        return result
    except Exception as e:
        print(f"获取数据时发生错误: {str(e)}")
        return None