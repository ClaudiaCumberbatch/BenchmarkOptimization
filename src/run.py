from provider import *
from file_utils import *
import argparse

command = '''
#-------------intelmpi+ifort------------------------------------------
source /share/intel/2018u4/compilers_and_libraries/linux/bin/compilervars.sh -arch intel64 -platform linux
source /share/intel/2018u4/impi/2018.4.274/intel64/bin/mpivars.sh
module load intel/2018.3
module load mpi/intel/2018.3

#---------------------------------------------------------------------
source activate /work/cse-zhousc/.conda/envs/HPL_env
'''

if __name__=="__main__":
    parser = argparse.ArgumentParser(description="specify the config file")
    parser.add_argument("-f", type=str, default="../config/config.yaml", help="config file")
    args = parser.parse_args()
    config_filepath = args.f

    config = file_interactor.parse_config(config_filepath)

    p = LSFProvider(config)
    main_cmd = "python main.py -f {}".format(config_filepath)
    activate_cmd = "source activate {}".format(config['path_to_env'])
    print(command + activate_cmd + main_cmd)
    p.submit(command+main_cmd)