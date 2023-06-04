
import os
import click
import pickle
import mlflow

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

import warnings
# Ignore all warnings
# warnings.filterwarnings("ignore")

# Filter the specific warning message
warnings.filterwarnings("ignore", category=UserWarning, module="setuptools")
warnings.filterwarnings("ignore", category=UserWarning, message="Setuptools is replacing distutils.")


def load_pickle(filename: str):
    with open(filename, "rb") as f_in:
        return pickle.load(f_in)


@click.command()
@click.option(
    "--data_path",
    default="./output",
    help="Location where the processed NYC taxi trip data was saved"
)


def run_train(data_path: str):
    
    mlflow.set_tracking_uri("sqlite:///mlflow.db")
    mlflow.set_experiment("nyc-taxi-experiment")
    
    # before your training code to enable automatic logging of sklearn metrics, params, and models
    mlflow.sklearn.autolog()
    
    with mlflow.start_run():
        mlflow.set_tag("developer", "muce")
        mlflow.log_param("train-data-path", './output/train.pkl')
        mlflow.log_param("valid-data-path", './output/val.pkl')
        mlflow.log_param("test-data-path",  './output/test.pkl')
        

        X_train, y_train = load_pickle(os.path.join(data_path, "train.pkl"))
        X_val, y_val     = load_pickle(os.path.join(data_path, "val.pkl"))
        
        params = {"max_depth": 10, "random_state": 0}
        mlflow.log_params(params)
        
        rf     = RandomForestRegressor(**params)
        rf.fit(X_train, y_train)
        y_pred = rf.predict(X_val)
        # autolog_run = mlflow.last_active_run()


        rmse = mean_squared_error(y_val, y_pred, squared=False)
        mlflow.log_metric("rmse", rmse)
        
        folder_path = 'models'
        os.makedirs(folder_path, exist_ok=True)
        
        # Log Model two options
        # save model, preprocessor or pipeline
        with open('models/ride_duration_rf_model.bin', 'wb') as f_out:
            pickle.dump(rf, f_out)
        
        # as artifact, save model, preprocessor or pipeline
        mlflow.log_artifact(local_path="models/ride_duration_rf_model.bin", artifact_path="models_pickle")
        
        # as model, save model
        mlflow.sklearn.log_model(sk_model = rf, artifact_path = "models_mlflow")
        
        print(f"default artifacts URI: '{mlflow.get_artifact_uri()}'")


if __name__ == '__main__':
    run_train()
