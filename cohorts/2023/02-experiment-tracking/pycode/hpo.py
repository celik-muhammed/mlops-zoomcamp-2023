
import os
import pickle
import click

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

import optuna
from optuna.samplers import TPESampler

import mlflow


def load_pickle(filename: str, data_path: str):
    file_path = os.path.join(data_path, filename)
    with open(file_path, "rb") as f_in:
        return pickle.load(f_in)


@click.command()
@click.option(
    "--data_path",
    default="./output",
    help="Location where the processed NYC taxi trip data was saved"
)
@click.option(
    "--num_trials",
    default=10,
    help="The number of parameter evaluations for the optimizer to explore"
)
def run_optimization(data_path: str, num_trials: int):
    """The main optimization pipeline"""
    # MLflow settings
    # Build or Connect Database Offline
    mlflow.set_tracking_uri("sqlite:///mlflow.db")
    # Connect Database Online
    # mlflow.set_tracking_uri("http://127.0.0.1:5000")
    
    # Build or Connect mlflow experiment
    HPO_EXPERIMENT_NAME = "random-forest-hyperopt"
    mlflow.set_experiment(HPO_EXPERIMENT_NAME)
    
    # before your training code to disable automatic logging of sklearn metrics, params, and models
    mlflow.sklearn.autolog(disable=True)
    
    # Optional: Set some information about Model
    mlflow.set_tag("developer", "muce")
    mlflow.set_tag("algorithm", "Machine Learning")
    mlflow.set_tag("train-data-path", f'{data_path}/train.pkl')
    mlflow.set_tag("valid-data-path", f'{data_path}/val.pkl')
    mlflow.set_tag("test-data-path",  f'{data_path}/test.pkl') 
    
    # Load train and test Data
    X_train, y_train = load_pickle("train.pkl", data_path)
    X_val, y_val     = load_pickle("val.pkl", data_path)        

    
    def objective(trial):
        params = {
            'n_estimators'     : trial.suggest_int('n_estimators', 10, 50, 1),
            'max_depth'        : trial.suggest_int('max_depth', 1, 20, 1),
            'min_samples_split': trial.suggest_int('min_samples_split', 2, 10, 1),
            'min_samples_leaf' : trial.suggest_int('min_samples_leaf', 1, 4, 1),
            'random_state'     : 42,
            'n_jobs'           : -1
        }
        with mlflow.start_run(nested=True):
            
            # Log the model params to the tracking server
            mlflow.log_params(params)
            
            # Build Model   
            rf = RandomForestRegressor(**params)
            rf.fit(X_train, y_train)
            
            # Log the validation RMSE to the tracking server
            y_pred = rf.predict(X_val)
            rmse   = mean_squared_error(y_val, y_pred, squared=False)
            mlflow.log_metric("rmse", rmse)

        return rmse

    sampler = TPESampler(seed=42)
    study   = optuna.create_study(direction="minimize", sampler=sampler)
    study.optimize(func = objective, n_trials=num_trials, n_jobs=-1)
    
    print(f"default artifacts URI: '{mlflow.get_artifact_uri()}'")


if __name__ == '__main__':
    run_optimization()
