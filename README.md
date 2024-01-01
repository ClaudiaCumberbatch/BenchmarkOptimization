# BenchmarkOptimization

## Setup the Environement

```shell
pip install -r requirements.txt
```

## Run the Program

1. Start a screen session, so that the job provider will run even if you quit.

```shell
screen
```

2. Start provider.

```shell
cd src
python run.py
```

tips: useful commands of screen

```shell
screen -ls //显示已创建的screen终端 
screen -r 2276 //连接 screen_id 为 2276 的 screen终端
```

ctrl+a d 离开当前screen终端

## Modify Settings

1. Modify `config/config.yaml`, or write your own config file and use `-f path/to/your/own/config/file` in the `command` string in `run.py`.

2. Modify `command` in `run.py`.

