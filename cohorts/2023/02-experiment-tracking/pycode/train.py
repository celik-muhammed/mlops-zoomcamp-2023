
import os
import click
import pickle

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

import mlflow

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


@click.command()
@click.option(
    "--data_path",
    default="./output",
    help="Location where the processed NYC taxi trip data was saved"
)
@click.option(
    "--dest_path",
    default="./models",
    help="Location where the resulting files will be saved"
)
def run_train(data_path: str, dest_path: str):
    """The main training pipeline"""
    # MLflow settings
    # Build or Connect Database Offline
    mlflow.set_tracking_uri("sqlite:///mlflow.db")
    # Connect Database Online
    # mlflow.set_tracking_uri("http://127.0.0.1:5000")
    
    # Build or Connect mlflow experiment
    EXPERIMENT_NAME = "random-forest-train"
    mlflow.set_experiment(EXPERIMENT_NAME)
            
    # before your training code to enable automatic logging of sklearn metrics, params, and models
    mlflow.sklearn.autolog()    
    
    # Load train and test Data
    X_train, y_train = load_pickle("train.pkl", data_path)
    X_val, y_val     = load_pickle("val.pkl", data_path)
    
    with mlflow.start_run():
        # Optional: Set some information about Model
        mlflow.set_tag("developer", "muce")
        mlflow.set_tag("algorithm", "Machine Learning")
        mlflow.set_tag("train-data-path", f'{data_path}/train.pkl')
        mlflow.set_tag("valid-data-path", f'{data_path}/val.pkl')
        mlflow.set_tag("test-data-path",  f'{data_path}/test.pkl')        
        
        # Set Model params information
        params = {"max_depth": 10, "random_state": 0}
        mlflow.log_params(params)
        
        # Build Model        
        rf     = RandomForestRegressor(**params)
        rf.fit(X_train, y_train)
        
        # autolog_run = mlflow.last_active_run()

        # Set Model Evaluation Metric
        y_pred = rf.predict(X_val)
        rmse   = mean_squared_error(y_val, y_pred, squared=False)
        mlflow.log_metric("rmse", rmse)
        # print("rmse", rmse)
                        
        # Log Model two options
        # Option1: Just log model
        mlflow.sklearn.log_model(sk_model = rf, artifact_path = "models_mlflow")
                
        # Option 2: save Model, Optional: Preprocessor or Pipeline        
        # Create dest_path folder unless it already exists
        # pathlib.Path(dest_path).mkdir(exist_ok=True) 
        os.makedirs(dest_path, exist_ok=True)
        local_path = os.path.join(dest_path, "ride_duration_rf_model.bin")
        with open(local_path, 'wb') as f_out:
            pickle.dump(rf, f_out)
            
        # whole proccess like pickle, saved Model, Optional: Preprocessor or Pipeline
        mlflow.log_artifact(local_path = local_path, artifact_path="models_pickle")        
        
        print(f"default artifacts URI: '{mlflow.get_artifact_uri()}'")


if __name__ == '__main__':
    run_train()
