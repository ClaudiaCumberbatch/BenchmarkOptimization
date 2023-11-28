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
    for param, param_range in param_ranges.items():
        param_values[param] = trial.suggest_categorical(param, param_range)
    

def optuna_HPL(node_count, core_count, iter_count):
    study = optuna.create_study(direction='maximize')
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

    figure = plot_contour(study)
    pio.write_image(figure, f"../logs/contour_{benchmark}_{iter_count}_.png")

    figure = plot_slice(study)
    pio.write_image(figure, f"../logs/slice_{benchmark}_{iter_count}_.png")

    figure = plot_param_importances(study)
    pio.write_image(figure, f"../logs/param_importances_{benchmark}_{iter_count}_.png")

    figure = plot_param_importances(
        study, target=lambda t: t.duration.total_seconds(), target_name="duration"
    )
    pio.write_image(figure, f"../logs/param_importances_duration_{benchmark}_{iter_count}_.png")

    figure = plot_edf(study)
    pio.write_image(figure, f"../logs/edf_{benchmark}_{iter_count}_.png")

    figure = plot_rank(study)
    pio.write_image(figure, f"../logs/rank_{benchmark}_{iter_count}_.png")

    figure = plot_timeline(study)
    pio.write_image(figure, f"../logs/timeline_{benchmark}_{iter_count}_.png")