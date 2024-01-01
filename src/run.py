from provider import *

command = '''
#-------------intelmpi+ifort------------------------------------------
source /share/intel/2018u4/compilers_and_libraries/linux/bin/compilervars.sh -arch intel64 -platform linux
source /share/intel/2018u4/impi/2018.4.274/intel64/bin/mpivars.sh
module load intel/2018.3
module load mpi/intel/2018.3

#---------------------------------------------------------------------
source activate /work/cse-zhousc/.conda/envs/HPL_env
python main.py
'''

if __name__=="__main__":
    p = LSFProvider()
    p.submit(command)