def output(param, Gflops):
    print("The best parameter is: ")
    for key, value in param.items():
        print("{:<10} : {}".format(key, value))
    print("The best Gflops is: ", Gflops)