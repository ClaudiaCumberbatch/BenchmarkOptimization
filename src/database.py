import sqlite3

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