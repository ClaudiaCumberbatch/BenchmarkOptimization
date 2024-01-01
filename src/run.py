from provider import *
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

    p = LSFProvider()
    cmd = "python main.py -f {}".format(config_filepath)
    # print(command+cmd)
    p.submit(command+cmd)