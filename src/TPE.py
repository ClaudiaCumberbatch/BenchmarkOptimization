from optimizer import *
import time
import optuna
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

class TPEOptimizer(Optimizer):
    def __init__(self, database_interactor, file_interactor, iter_count, benchmark):
        super().__init__(database_interactor, file_interactor, iter_count, benchmark)
        self.name = "TPE"

    def objective(self, trial):
        tempt_param = {}
        for param_name, param_value in self.config_param.items():
            if param_value['type'] == 'int':
                tempt_param[param_name] = trial.suggest_int(param_name, param_value['range'][0], param_value['range'][1], param_value['step'])
            elif param_value['type'] == 'categorical':
                tempt_param[param_name] = trial.suggest_categorical(param_name, param_value['range'])
        print(tempt_param)
        Gflops = self.get_data(tempt_param)
        return Gflops
    
    def suggest_param(self):
        pass

    def optimize(self):
        start_time = time.time()
        self.study = optuna.create_study(direction='maximize')
        self.study.optimize(self.objective, n_trials=self.iter_count)
        self.best_params = self.study.best_params
        self.GFlops = self.study.best_value
        end_time = time.time()  # Get the current time
        self.time = end_time - start_time  # Calculate the elapsed time   

    def visualize(self):
        figure = plot_optimization_history(self.study)
        pio.write_image(figure, f"../logs/optimization_history_{self.benchmark}_{self.iter_count}_.png")

        figure = plot_parallel_coordinate(self.study)
        pio.write_image(figure, f"../logs/parallel_coordinate_{self.benchmark}_{self.iter_count}_.png")

        param_names = list(self.study.best_params.keys())
        for i in range(len(param_names)):
            for j in range(i+1, len(param_names)):
                figure = plot_contour(self.study, params=[param_names[i], param_names[j]])
                pio.write_image(figure, f"../logs/contour_{self.benchmark}_{self.iter_count}_fig{i}_{j}.png")

        for i in range(len(param_names)):
                figure = plot_slice(self.study, params=[param_names[i]])
                pio.write_image(figure, f"../logs/slice_{self.benchmark}_{self.iter_count}_fig{i}.png")

        figure = plot_param_importances(self.study)
        pio.write_image(figure, f"../logs/param_importances_{self.benchmark}_{self.iter_count}_.png")

        figure = plot_param_importances(
            self.study, target=lambda t: t.duration.total_seconds(), target_name="duration"
        )
        pio.write_image(figure, f"../logs/param_importances_duration_{self.benchmark}_{self.iter_count}_.png")

        figure = plot_edf(self.study)
        pio.write_image(figure, f"../logs/edf_{self.benchmark}_{self.iter_count}_.png")

        for i in range(len(param_names)):
            for j in range(i+1, len(param_names)):
                figure = plot_rank(self.study, params=[param_names[i], param_names[j]])
                pio.write_image(figure, f"../logs/rank_{self.benchmark}_{self.iter_count}_fig{i}_{j}.png")

        figure = plot_timeline(self.study)
        pio.write_image(figure, f"../logs/timeline_{self.benchmark}_{self.iter_count}_.png")

    