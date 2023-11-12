#!/bin/bash
#SBATCH -o job.%j.out               
#SBATCH -e job.%j.err
#SBATCH --partition=gpulab02      # 作业提交的指定分区队列为titan
#SBATCH --qos=gpulab02            # 指定作业的QOS
#SBATCH -J HPL4       # 作业在调度系统中的作业名为myFirstJob;
#SBATCH --nodes=1              # 申请节点数为1,如果作业不能跨节点(MPI)运行, 申请的节点数应不超过1
#SBATCH --ntasks-per-node=4    # 每个节点上运行一个任务，默认一情况下也可理解为每个节点使用一个核心；
#SBATCH --gres=gpu:1           # 指定作业的需要的GPU卡数量，集群不一样，注意最大限制; 
#SBATCH --nodelist=gpu029

source /opt/intel/oneapi/setvars.sh
module load icc/2023.2.1
hostname
# mpiexec.hydra -np 4 ./xhpl

start_time=$(date +%s)

while true; do
    # 运行HPL
    mpiexec.hydra -np 4 ./xhpl
    # 改变参数配置
    python GenerateParameter.py 4


    # 获取当前时间
    current_time=$(date +%s)

    # 计算经过的时间（以秒为单位）
    elapsed_time=$((current_time - start_time))

    # 如果运行时间超过46小时（165600秒），跳出循环
    if [ "$elapsed_time" -ge 165600 ]; then
        echo "运行时间超过46小时，退出循环。"
        break
    fi
done