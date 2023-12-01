import config

def output(iter_count, param, Gflops, time, function_key):
    print("Algorithm and benchmark:", function_key)
    print("The number of iteration is: ", iter_count)
    print("The best parameter is: ")
    for key, value in param.items():
        print("{:<10} : {}".format(key, value))
    print("The best Gflops is: ", Gflops)
    print("The total duration is ", time, "s")
    print("The config file content is: ")
    config_param = config.parse_config_yaml()
    for key, value in config.items():
        print("{:<10} : {}".format(key, value))