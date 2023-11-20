from database import *
from file_utils import *

def get_param():
    params = {
        "N": 20352,
        "NB": 192,
        "PMAP": 0,
        "Q": 2,
        "PFACT": 0,
        "NBMIN": 3,
        "NDIV": 2,
        "RFACT": 2,
        "BCAST": 0,
        "DEPTH": 0,
        "SWAP": 2,
        "L1": 0,
        "U": 0,
        "EQUIL": 1
    }
    return params

if __name__ == "__main__":
    param = get_param()
    print(param)
    res = get_HPL_data(param)
    print(res)