from abc import ABC, abstractmethod
from database import database_interactor
from file_utils import file_interactor
import time

class Optimizer(ABC):
    def __init__(self, database_interactor: database_interactor, file_int: file_interactor, iter_count: int, benchmark: str):
        self.database_interactor = database_interactor  
        self.file_interactor = file_int
        self.config_param = self.file_interactor.get_config_param()
        self.iter_count = iter_count   
        self.benchmark = benchmark
        self.time = 0
        self.GFlops = 0
        self.best_params = {}
        self.name = ""

    def get_data(self, params: dict) -> float:
        return self.database_interactor.get_data(params)

    @abstractmethod
    def suggest_param(self) -> dict:
        pass

    def optimize(self):
        start_time = time.time()
        for i in range(self.iter_count):
            tempt_param = self.suggest_param()
            tempt_gflops = self.get_data(tempt_param)
            print("iter: ", i, "\nparams: ", tempt_param, "\nGFlops: ", tempt_gflops)
            if tempt_gflops > self.GFlops:
                self.GFlops = tempt_gflops
                self.best_params = tempt_param
        end_time = time.time()  # Get the current time
        self.time = end_time - start_time  # Calculate the elapsed time

    @abstractmethod
    def visualize(self):
        pass

    def output(self):
        print(f"Optimizer Name: {self.name}")
        print(f"Benchmark Name: {self.benchmark}")
        print(f"iter_count: {self.iter_count}")
        for key, value in self.best_params.items():
            print("{:<10} : {}".format(key, value))
        print(f"The total duration: {self.time}")
        print(f"GFlops: {self.GFlops}")
        print("--------------------------------------------------")
        print("config parameters:")
        for key, value in self.config_param.items():
            print("{:<10} : {}".format(key, value))
