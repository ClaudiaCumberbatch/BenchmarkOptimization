from optimizer import *
from skopt import gp_minimize
from skopt.space import Integer, Categorical
from skopt.plots import plot_convergence
from skopt.plots import plot_gaussian_process
import matplotlib.pyplot as plt

class GPOptimizer(Optimizer):
    def __init__(self, database_interactor, file_interactor, iter_count, benchmark):
        super().__init__(database_interactor, file_interactor, iter_count, benchmark)
        self.name = "GP"
        self.space = []
        for param_name, param_value in self.config_param.items():
            if param_value['type'] == 'int':
                self.space.append(Integer(param_value['range'][0] / param_value['step'], param_value['range'][1] / param_value['step'], name=param_name))
            elif param_value['type'] == 'categorical':
                self.space.append(Categorical(param_value['range'], name=param_name))

    def objective(self, params):
        tempt_param = {}
        for i in range(len(self.space)):
            if self.config_param[self.space[i].name]['type'] == 'int':
                tempt_param[self.space[i].name] = params[i] * self.config_param[self.space[i].name]['step']
            elif self.config_param[self.space[i].name]['type'] == 'categorical':
                tempt_param[self.space[i].name] = params[i]
        Gflops = self.get_data(tempt_param)
        print(tempt_param, Gflops)
        return -Gflops
    
    def suggest_param(self):
        pass

    def optimize(self):
        start_time = time.time()
        self.res = gp_minimize(self.objective, self.space, n_calls=self.iter_count)
        self.best_params = {}
        for i in range(len(self.space)):
            self.best_params[self.space[i].name] = self.res.x[i]
        self.GFlops = -self.res.fun
        end_time = time.time()
        self.time = end_time - start_time

    def visualize(self):
        plot_convergence(self.res)
        plt.savefig(f'../logs/convergence_plot_{self.benchmark}_{self.iter_count}.png')
    