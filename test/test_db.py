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
    config_filepath = "../config/config.yaml"
    param = get_param()
    print(param)

    config = file_interactor.parse_config(config_filepath)
    print(config)

    file_int = HPL_file_interactor(config_filepath)
    hpl_int = HPL_interactor(file_int)
    
    res = hpl_int.get_data(param)
    print(res)