
import os
import sys
import pickle
from tqdm.auto import tqdm
tqdm._instances.clear()

import numpy as np
import pandas as pd

import boto3  # Import the boto3 library for S3


def read_data(filename: str) -> pd.DataFrame:
    """Read data into DataFrame"""
    df = pd.read_parquet(filename)

    df["tpep_dropoff_datetime"] = pd.to_datetime(df.tpep_dropoff_datetime)
    df["tpep_pickup_datetime"] = pd.to_datetime(df.tpep_pickup_datetime)

    df["duration"] = df["tpep_dropoff_datetime"] - df["tpep_pickup_datetime"]
    df['duration'] = df['duration'].dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    # df[categorical] = df[categorical].astype(str)
    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')

    return df


def predict_duration(df: pd.DataFrame, dv, lr) -> np.ndarray:
    """Predict the duration using the trained model"""
    dicts  = df[categorical].to_dict(orient='records')
    X_val  = dv.transform(dicts)
    y_pred = lr.predict(X_val)
    return y_pred


def save_results(df: pd.DataFrame, y_pred: np.ndarray, output_file: str) -> None:
    """Save the predicted results to a parquet file"""
    os.makedirs('output', exist_ok=True)
    
    df_result = pd.DataFrame()
    df_result['ride_id'] = df['ride_id']
    df_result['predicted_duration'] = y_pred
    df_result.to_parquet(        
        output_file,
        engine='pyarrow',
        compression=None,
        index=False
    )
    return None


def upload_to_s3(file_path: str, s3_bucket: str, s3_key: str):
    """Upload a file to S3 bucket"""
    s3_client = boto3.client('s3')
    s3_client.upload_file(file_path, s3_bucket, s3_key)
    
    print(f"Uploaded file to S3: s3://{s3_bucket}/{s3_key}")
    

def main():    
    steps = ["Reading data", "Loading model"]
    with tqdm(total=len(steps), desc="Running steps", leave=True) as pbar:
        # Step 1: Reading data
        pbar.set_description(steps[0])
        df = read_data(input_file)
        df['ride_id'] = f'{year:04d}/{month:02d}_' + df.index.astype('str')
        pbar.update(1)

        # Step 2: Loading model
        pbar.set_description(steps[1])
        with open('model.bin', 'rb') as f_in:
            dv, lr = pickle.load(f_in)
        pbar.update(1)
        pbar.close()    


    # Prediction
    y_pred = predict_duration(df, dv, lr)
    print('predicted mean duration:', y_pred.mean().round(2))

    # save_results
    save_results(df, y_pred, output_file)
    
    # Upload the Parquet file to S3
    s3_bucket = 'your-s3-bucket-name'  # Replace with your S3 bucket name 
    upload_to_s3(output_file, s3_bucket, s3_key=output_file)

    
if __name__ == '__main__':
    # Global Parameters
    year        = int(sys.argv[1]) # 2022
    month       = int(sys.argv[2]) # 2
    input_file  = f'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year:04d}-{month:02d}.parquet'
    output_file = f'output/yellow_tripdata_{year:04d}-{month:02d}.parquet'
    categorical = ['PULocationID', 'DOLocationID']    

    main()
