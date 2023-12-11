import optuna
from file_utils import *
from database import *
from optuna.visualization import plot_contour
from optuna.visualization import plot_edf
from optuna.visualization import plot_intermediate_values
from optuna.visualization import plot_optimization_history
from optuna.visualization import plot_parallel_coordinate
from optuna.visualization import plot_param_importances
from optuna.visualization import plot_rank
from optuna.visualization import plot_slice
from optuna.visualization import plot_timeline
import plotly.io as pio
import plotly.graph_objects as go

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

def HPCG_objective(trial):
    param_ranges = get_HPCG_params()
    param_values = {}
    param_values['NX'] = trial.suggest_categorical('NX', param_ranges['NX'])
    param_values['NY'] = trial.suggest_categorical('NY', param_ranges['NY'])
    param_values['NZ'] = trial.suggest_categorical('NZ', param_ranges['NZ'])
    param_values['Time'] = param_ranges['Time']
    Gflops = get_HPCG_data(param_values)
    return Gflops
    

def optuna_HPL(node_count, core_count, iter_count):
    study = optuna.create_study(direction='maximize')
    study.enqueue_trial(
        {
            "PMAP": 0,
            "SWAP": 0,
            "L1": 0,
            "U": 0,
            "EQUIL": 0,
            "DEPTH": 6,
            "BCAST": 4,
            "RFACT": 0,
            "NDIV": 8,
            "PFACT": 0,
            "NBMIN": 12,
            "N": 120000,
            "NB": 300,
            "Q": 10
        }
    )
    study.optimize(HPL_objective, n_trials=iter_count)
    visualize(study, "HPL", iter_count)
    return study.best_params, study.best_value

def optuna_HPCG(node_count, core_count, iter_count):
    study = optuna.create_study(direction='maximize')
    study.optimize(HPCG_objective, n_trials=iter_count)
    visualize(study, "HPCG", iter_count)
    return study.best_params, study.best_value

def visualize(study, benchmark, iter_count):
    figure = plot_optimization_history(study)
    pio.write_image(figure, f"../logs/optimization_history_{benchmark}_{iter_count}_.png")

    figure = plot_parallel_coordinate(study)
    pio.write_image(figure, f"../logs/parallel_coordinate_{benchmark}_{iter_count}_.png")

    param_names = list(study.best_params.keys())
    for i in range(len(param_names)):
        for j in range(i+1, len(param_names)):
            figure = plot_contour(study, params=[param_names[i], param_names[j]])
            pio.write_image(figure, f"../logs/contour_{benchmark}_{iter_count}_fig{i}_{j}.png")

    for i in range(len(param_names)):
            figure = plot_slice(study, params=[param_names[i]])
            pio.write_image(figure, f"../logs/slice_{benchmark}_{iter_count}_fig{i}.png")

    figure = plot_param_importances(study)
    pio.write_image(figure, f"../logs/param_importances_{benchmark}_{iter_count}_.png")

    figure = plot_param_importances(
        study, target=lambda t: t.duration.total_seconds(), target_name="duration"
    )
    pio.write_image(figure, f"../logs/param_importances_duration_{benchmark}_{iter_count}_.png")

    figure = plot_edf(study)
    pio.write_image(figure, f"../logs/edf_{benchmark}_{iter_count}_.png")

    for i in range(len(param_names)):
        for j in range(i+1, len(param_names)):
            figure = plot_rank(study, params=[param_names[i], param_names[j]])
            pio.write_image(figure, f"../logs/rank_{benchmark}_{iter_count}_fig{i}_{j}.png")

    figure = plot_timeline(study)
    pio.write_image(figure, f"../logs/timeline_{benchmark}_{iter_count}_.png")