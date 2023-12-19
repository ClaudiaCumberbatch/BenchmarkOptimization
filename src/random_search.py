import random
from optimizer import Optimizer


class RandomSearchOptimizer(Optimizer):
    def __init__(self, database_interactor, iter_count, config_param, benchmark):
        super().__init__(database_interactor, iter_count, config_param, benchmark)
        self.name = "Random_search"
    
    def suggest_param(self):
        random_params = {}
        for param_name, param_value in self.config_param.items():
            if param_value['type'] == 'int':
                random_params[param_name] = random.randrange(param_value['range'][0], param_value['range'][1] + 1, param_value['step'])
            elif param_value['type'] == 'categorical':
                random_params[param_name] = random.choice(param_value['range'])
        return random_params

    def visualize(self):
        pass