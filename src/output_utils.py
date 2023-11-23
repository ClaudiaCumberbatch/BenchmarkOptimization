def output(iter_count, param, Gflops):
    print("The number of iteration is: ", iter_count)
    print("The best parameter is: ")
    for key, value in param.items():
        print("{:<10} : {}".format(key, value))
    print("The best Gflops is: ", Gflops)