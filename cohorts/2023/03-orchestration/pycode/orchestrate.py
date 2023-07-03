
# Source: https://github.com/DataTalksClub/mlops-zoomcamp/blob/main/03-orchestration/3.4/orchestrate.py

import os
import click
import pickle
import pathlib
import argparse
import requests
import urllib.request
from glob import glob
from datetime import date
from datetime import timedelta

import pandas as pd
import numpy as np
import scipy
import sklearn
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics import mean_squared_error
import xgboost as xgb

import mlflow
import prefect
from prefect import task, flow
from prefect.tasks import task_input_hash
from prefect.artifacts import create_markdown_artifact

# from prefect_aws import S3Bucket
# from prefect_email import EmailServerCredentials, email_send_message

import warnings
# Ignore all warnings
# warnings.filterwarnings("ignore")
# Filter the specific warning message, MLflow autologging encountered a warning
# warnings.filterwarnings("ignore", category=UserWarning, module="setuptools")
warnings.filterwarnings("ignore", category=UserWarning, message="Setuptools is replacing distutils.")


@task(name="Fetch Data", cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1),
      retries=3, log_prints=True, )
def fetch_data(raw_data_path: str, year: int, month: int, color: str) -> None:
    """Fetches data from the NYC Taxi dataset and saves it locally"""
    os.makedirs(raw_data_path, exist_ok=True)  

    # Download the data from the NYC Taxi dataset
    url      = f'https://d37ci6vzurychx.cloudfront.net/trip-data/{color}_tripdata_{year}-{month:0>2}.parquet'
    filename = os.path.join(raw_data_path, f'{color}_tripdata_{year}-{month:0>2}.parquet')
    # urllib.request.urlretrieve(url, filename)
    # os.system(f"wget -q -N -P {raw_data_path} {url}")
    
    response = requests.get(url)
    with open(filename, "wb") as f:
        f.write(response.content)
    return None
    
    
@task(name="Read Taxi Data", retries=3, retry_delay_seconds=2, log_prints=None)
def read_data(filename: str) -> pd.DataFrame:
    """Read data into DataFrame"""
    df = pd.read_parquet(filename)

    df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)
    df.lpep_pickup_datetime  = pd.to_datetime(df.lpep_pickup_datetime)

    df["duration"] = df.lpep_dropoff_datetime - df.lpep_pickup_datetime
    df.duration    = df.duration.apply(lambda td: td.total_seconds() / 60)

    df = df[(df.duration >= 1) & (df.duration <= 60)]

    categorical     = ["PULocationID", "DOLocationID"]
    df[categorical] = df[categorical].astype(str)

    return df


@task(name="Add Features Taxi Data", log_prints=True)
def add_features(
    df_train: pd.DataFrame, df_val: pd.DataFrame, df_test: pd.DataFrame
) -> tuple(
    [
        scipy.sparse._csr.csr_matrix,
        scipy.sparse._csr.csr_matrix,
        np.ndarray,
        np.ndarray,
        sklearn.feature_extraction.DictVectorizer,
    ]
):
    """Add features to the model"""
    df_train["PU_DO"] = df_train["PULocationID"] + "_" + df_train["DOLocationID"]
    df_val["PU_DO"]   = df_val["PULocationID"]   + "_" + df_val["DOLocationID"]
    df_test["PU_DO"]  = df_test["PULocationID"]  + "_" + df_test["DOLocationID"]

    categorical = ["PU_DO"]  #'PULocationID', 'DOLocationID']
    numerical   = ["trip_distance"]

    dv = DictVectorizer()

    train_dicts = df_train[categorical + numerical].to_dict(orient="records")
    X_train     = dv.fit_transform(train_dicts)
    y_train     = df_train["duration"].values

    val_dicts   = df_val[categorical + numerical].to_dict(orient="records")
    X_val       = dv.transform(val_dicts)
    y_val       = df_val["duration"].values
    
    test_dicts  = df_test[categorical + numerical].to_dict(orient="records")
    X_test      = dv.transform(test_dicts)
    y_test      = df_test["duration"].values

    return (X_train, y_train), (X_val, y_val), (X_test, y_test), dv


@task(name="Train Best Model", log_prints=True)
def train_best_model(
    X_train  : scipy.sparse._csr.csr_matrix,
    X_val    : scipy.sparse._csr.csr_matrix,
    y_train  : np.ndarray,
    y_val    : np.ndarray,
    dv       : sklearn.feature_extraction.DictVectorizer,
    dest_path: str,
) -> None:
    """train a model with best hyperparams and write everything out"""        
    # Load train and test Data
    train = xgb.DMatrix(X_train, label=y_train)
    valid = xgb.DMatrix(X_val, label=y_val)

    # before your training code to enable automatic logging of sklearn metrics, params, and models
    # mlflow.xgboost.autolog()
    
    with mlflow.start_run():
        # Optional: Set some information about Model
        mlflow.set_tag("developer", "muce")
        mlflow.set_tag("algorithm", "Machine Learning")
        mlflow.set_tag("train-data-path", f'./data/green_tripdata_2023-01.parquet')
        mlflow.set_tag("valid-data-path", f'./data/green_tripdata_2023-02.parquet')
        mlflow.set_tag("test-data-path",  f'./data/green_tripdata_2023-03.parquet')

        # Set Model params information
        best_params = {
            "learning_rate": 0.09585355369315604,
            "max_depth": 30,
            "min_child_weight": 1.060597050922164,
#             'objective': 'reg:squarederror',          # deprecated  "reg:linear"
            'objective': "reg:linear",
            "reg_alpha": 0.018060244040060163,
            "reg_lambda": 0.011658731377413597,
            "seed": 42,
        }
        mlflow.log_params(best_params)

        # Build Model   
        booster = xgb.train(
            params               = best_params,
            dtrain               = train,
            num_boost_round      = 100,
            evals                = [(valid, "validation")],
            early_stopping_rounds=20,
        )   
        
        # Set Model Evaluation Metric
        y_pred = booster.predict(valid)
        rmse   = mean_squared_error(y_val, y_pred, squared=False)
        mlflow.log_metric("rmse", rmse)       

        # Log Model two options
        # Option1: Just log model
        mlflow.xgboost.log_model(booster, artifact_path="models_mlflow")        
        
        # Option 2: save Model, Optional: Preprocessor or Pipeline         
        # Create dest_path folder unless it already exists
        # pathlib.Path(dest_path).mkdir(exist_ok=True) 
        os.makedirs(dest_path, exist_ok=True)       
        local_file = os.path.join(dest_path, "preprocessor.b")
        with open(local_file, "wb") as f_out:
            pickle.dump(dv, f_out)
            
        # whole proccess like pickle, saved Model, Optional: Preprocessor or Pipeline
        mlflow.log_artifact(local_path = local_file, artifact_path="preprocessor")        
        
        # print(f"default artifacts URI: '{mlflow.get_artifact_uri()}'")

        # Create markdown artifact with RMSE value
        markdown__rmse_report = f"""
# RMSE Report

## Summary

Duration Prediction 

## RMSE XGBoost Model

| Region    | RMSE |
|:----------|-------:|
| {date.today()} | {rmse:.2f} |
"""

        create_markdown_artifact(
            key="duration-model-report", 
            markdown=markdown__rmse_report,
            description="RMSE for Validation Data Report",
        )
    return None


@flow(name="Subflow Download Data", log_prints=True)
def download_data(raw_data_path: str, years: list, months: list, colors: list):
    # Download the data from the NYC Taxi dataset
    for year in years:
        for month in months:
            for color in colors:
                fetch_data(raw_data_path, year, month, color)


# @flow(name="Email Server Crenditals", log_prints=True)
# def example_email_send_message_flow(email_addresses: list[str]):
#     email_server_credentials = EmailServerCredentials.load("email-server-credentials")
    
#     for email_address in email_addresses:
#         subject = email_send_message.with_options(name=f"email {email_address}").submit(
#             email_server_credentials=email_server_credentials,
#             subject="Example Flow Notification using Gmail",
#             msg="This proves email_send_message works!",
#             email_to=email_address,
#         )
                

@flow(name="Main Flow")
def main_flow(raw_data_path="./data", dest_path="./models", years="2023", months="1 2 3 4", colors="green yellow") -> None:
    """The main training pipeline"""
    # MLflow settings
    # Build or Connect Database Offline
    mlflow.set_tracking_uri("sqlite:///mlflow.db")
    # Build or Connect mlflow experiment
    mlflow.set_experiment("nyc-taxi-experiment")
    
    # Download data    
    years  = [int(year) for year in years.split()]
    months = [int(month) for month in months.split()]
    colors = colors.split()[:1]
    download_data(raw_data_path, years, months, colors)
    # print(glob(f'*'))
    
    # # Download the data from AWS S3 Bucket
    # s3_bucket_block = S3Bucket.load("s3-bucket-block")
    # s3_bucket_block.download_folder_to_path(from_folder="data", to_folder="data")
    
    # list parquet files
    # print(sorted(glob(f'{raw_data_path}/green*.parquet')))
    train_path, val_path, test_path = sorted(glob(f'{raw_data_path}/*.parquet'))[-3::]

    # Read parquet files
    df_train = read_data(train_path)
    df_val   = read_data(val_path)
    df_test  = read_data(test_path)
    # print(df_train.shape, df_val.shape, df_test.shape, )

    # Transform
    (X_train, y_train), (X_val, y_val), (X_test, y_test), dv = add_features(df_train, df_val, df_test)

    # Train
    train_best_model(X_train, X_val, y_train, y_val, dv, dest_path)

    # example_email_send_message_flow(['@gmail.com'])

if __name__ == "__main__":
    main_flow()
