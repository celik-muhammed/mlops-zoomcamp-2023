
import os
import click
import pickle

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

import mlflow
from mlflow.entities import ViewType
from mlflow.tracking import MlflowClient

import warnings
# Ignore all warnings
# warnings.filterwarnings("ignore")
# Filter the specific warning message, MLflow autologging encountered a warning
# warnings.filterwarnings("ignore", category=UserWarning, module="setuptools")
warnings.filterwarnings("ignore", category=UserWarning, message="Setuptools is replacing distutils.")


def load_pickle(filename: str, data_path: str):
    file_path = os.path.join(data_path, filename)
    with open(file_path, "rb") as f_in:
        return pickle.load(f_in)


def train_and_log_model(data_path, params):
    # Parameters
    RF_PARAMS = ['max_depth', 'n_estimators', 'min_samples_split', 'min_samples_leaf', 'random_state', 'n_jobs']
    
    # Load train, val and test Data
    X_train, y_train = load_pickle("train.pkl", data_path)
    X_val, y_val     = load_pickle("val.pkl", data_path)
    X_test, y_test   = load_pickle("test.pkl", data_path)

    with mlflow.start_run(nested=True):
        # Optional: Set some information about Model
        mlflow.set_tag("developer", "muce")
        mlflow.set_tag("algorithm", "Machine Learning")
        mlflow.set_tag("train-data-path", f'{data_path}/train.pkl')
        mlflow.set_tag("valid-data-path", f'{data_path}/val.pkl')
        mlflow.set_tag("test-data-path",  f'{data_path}/test.pkl') 
        
        for param in RF_PARAMS:
            params[param] = int(params[param])
            
        # Log the model params to the tracking server
        mlflow.log_params(params)

        # Build Model
        rf = RandomForestRegressor(**params)
        rf.fit(X_train, y_train)

        # Evaluate model on the validation and test sets
        val_rmse = mean_squared_error(y_val, rf.predict(X_val), squared=False)
        mlflow.log_metric("val_rmse", val_rmse)
        
        test_rmse = mean_squared_error(y_test, rf.predict(X_test), squared=False)
        mlflow.log_metric("test_rmse", test_rmse)

        # Log the model
        mlflow.sklearn.log_model(rf, "rf-model")
        
        # print(f"default artifacts URI: '{mlflow.get_artifact_uri()}'")


@click.command()
@click.option(
    "--data_path",
    default="./output",
    help="Location where the processed NYC taxi trip data was saved"
)
@click.option(
    "--top_n",
    default=5,
    type=int,
    help="Number of top models that need to be evaluated to decide which one to promote"
)
def run_register_model(data_path: str, top_n: int):
    """The main optimization pipeline"""
    # MLflow settings
    # Build or Connect Database Offline
    mlflow.set_tracking_uri("sqlite:///mlflow.db")
    # Connect Database Online
    # mlflow.set_tracking_uri("http://127.0.0.1:5000")
    
    # Build or Connect mlflow experiment
    EXPERIMENT_NAME = "random-forest-best-models"
    mlflow.set_experiment(EXPERIMENT_NAME)
    
    # before your training code to enable automatic logging of sklearn metrics, params, and models
    mlflow.sklearn.autolog()   
    
    # Optional: Set some information about Model
    mlflow.set_tag("developer", "muce")
    mlflow.set_tag("algorithm", "Machine Learning")
    mlflow.set_tag("train-data-path", f'{data_path}/train.pkl')
    mlflow.set_tag("valid-data-path", f'{data_path}/val.pkl')
    mlflow.set_tag("test-data-path",  f'{data_path}/test.pkl') 
            

    # Parameters
    HPO_EXPERIMENT_NAME = "random-forest-hyperopt"

    client = MlflowClient()

    # Retrieve the top_n model runs and log the models
    experiment = client.get_experiment_by_name(HPO_EXPERIMENT_NAME)
    runs = client.search_runs(
        experiment_ids=experiment.experiment_id,
        run_view_type=ViewType.ACTIVE_ONLY,
        max_results=top_n,
        order_by=["metrics.rmse ASC"]
    )
    for run in runs:
        train_and_log_model(data_path=data_path, params=run.data.params)

    # Select the model with the lowest test RMSE
    experiment = client.get_experiment_by_name(EXPERIMENT_NAME)
    best_run = client.search_runs(
        experiment_ids=experiment.experiment_id,
        run_view_type=ViewType.ACTIVE_ONLY,
        max_results=1,
        order_by=["metrics.test_rmse ASC"]
    )[0]

    # Register the best model
    run_id     = best_run.info.run_id
    model_uri  = f"runs:/{run_id}/model"
    model_name = "rf-best-model"
    mlflow.register_model(model_uri, name=model_name)

    print("Test RMSE of the best model: {:.4f}".format(best_run.data.metrics["test_rmse"]))


if __name__ == '__main__':
    run_register_model()
