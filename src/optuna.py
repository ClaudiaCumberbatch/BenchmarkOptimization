import optuna
from file_utils import *
from database import *

def HPL_objective(trial):  
    param_ranges = get_HPL_params()
    param_values = {}
    for param, param_range in param_ranges.items():
        if len(param_range) > 2:
            param_values[param] = trial.suggest_categorical(param, param_range)
        else:
            param_values[param] = trial.suggest_int(param, param_range[0], param_range[1])
    Gflops = get_HPL_data(param_values)
    return Gflops

def optuna_HPL(node_count, core_count, iter_count):
    study = optuna.create_study(direction='maximize')
    study.optimize(HPL_objective, n_trials=iter_count)
    return study.best_params, study.best_value