from predictor import *
from multiprocessing import Process, Queue
import subprocess

def task(HPL_pid, q):
    p = predictor()
    res = p.control('../logs/test.log', 0.3, HPL_pid)
    q.put(res)

def HPL_simu(q):
    command = "watch -n 1 bjobs"
    process = subprocess.Popen(command, shell=True)
    q.put(process.pid)

if __name__ == "__main__":
    q = Queue()
    q2 = Queue()
    process_HPL = Process(target=HPL_simu(q2))
    process_HPL.start()
    # print(f"HPL pid: {process_HPL.pid}")
    process_predict = Process(target=task(q2.get(), q))
    process_predict.start()
    process_predict.join()
   
    result = q.get()
    print(result)

