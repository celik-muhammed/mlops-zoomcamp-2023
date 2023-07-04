
# Source: https://github.com/DataTalksClub/mlops-zoomcamp/blob/main/cohorts/2023/02-experiment-tracking/homework/preprocess_data.py

import os
import click
import pickle

# import pathlib
# import argparse
import requests
# import urllib.request
from glob import glob
# from datetime import date, timedelta

import numpy as np
import pandas as pd
from sklearn.feature_extraction import DictVectorizer


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


def download_data(raw_data_path: str, years: list, months: list, colors: list) -> None:
    try:
        # Download the data from the NYC Taxi dataset
        for year in years:
            for month in months:
                for color in colors:
                    fetch_data(raw_data_path, year, month, color)
    except:
        pass
    return None


def read_data(filename: str) -> pd.DataFrame:
    """Read data into DataFrame"""
    df = pd.read_parquet(filename)

    df['lpep_dropoff_datetime'] = pd.to_datetime(df['lpep_dropoff_datetime'])
    df['lpep_pickup_datetime']  = pd.to_datetime(df['lpep_pickup_datetime'])

    df["duration"] = df['lpep_dropoff_datetime'] - df['lpep_pickup_datetime']
    df.duration    = df.duration.apply(lambda td: td.total_seconds() / 60)

    df = df[(df.duration >= 1) & (df.duration <= 60)]

    categorical     = ["PULocationID", "DOLocationID"]
    df[categorical] = df[categorical].astype(str)

    return df


def preprocess(df: pd.DataFrame, dv: DictVectorizer = None, fit_dv: bool = False):
    """Add features to the model"""
    df['PU_DO'] = df['PULocationID'] + '_' + df['DOLocationID']
    categorical = ["PU_DO"]
    numerical   = ['trip_distance']
    dicts       = df[categorical + numerical].to_dict(orient='records')

    if fit_dv:
        # return sparse matrix
        dv = DictVectorizer()
        X = dv.fit_transform(dicts)
    else:
        X = dv.transform(dicts)
        
    # Convert X the sparse matrix  to pandas DataFrame, but too slow
    # X = pd.DataFrame(X.toarray(), columns=dv.get_feature_names_out())
    # X = pd.DataFrame.sparse.from_spmatrix(X, columns=dv.get_feature_names_out())

    try:
        # Extract the target
        target = 'tip_amount'
        y = df[target].values
    except:
        pass

    return (X, y), dv


def dump_pickle(obj, filename: str, dest_path: str):    
    # Create dest_path folder unless it already exists
    os.makedirs(dest_path, exist_ok=True)
    file_path = os.path.join(dest_path, filename)
    
    with open(file_path, "wb") as f_out:
        return pickle.dump(obj, f_out)
                
                
@click.command()
@click.option(
    "--raw_data_path",
    default="./data",
    help="Location where the raw NYC taxi trip data was saved"
)
@click.option(
    "--dest_path",
    default="./output",
    help="Location where the resulting model files will be saved"
)
@click.option(
    "--years",
    default="2022",
    help="Years where the raw NYC taxi trip data was saved (space-separated)"
)
@click.option(
    "--months",
    default="1 2 3",
    help="Months where the raw NYC taxi trip data was saved (space-separated)"
)
@click.option(
    "--colors",
    default="green yellow",
    help="Colors where the raw NYC taxi trip data was saved"
)
def run_data_prep(raw_data_path: str, dest_path: str, years: str, months: str, colors: str) -> None:
    # Download data    
    years  = [int(year) for year in years.split()]
    months = [int(month) for month in months.split()]
    colors = colors.split()[:1]
    download_data(raw_data_path, years, months, colors)
    # print(sorted(glob(f'./data/*')))
    
    # Load parquet files
    df_train = read_data(
        os.path.join(raw_data_path, f"{colors[0]}_tripdata_2022-01.parquet")
    )
    df_val = read_data(
        os.path.join(raw_data_path, f"{colors[0]}_tripdata_2022-02.parquet")
    )
    df_test = read_data(
        os.path.join(raw_data_path, f"{colors[0]}_tripdata_2022-03.parquet")
    )

    # Fit the DictVectorizer and preprocess data
    (X_train, y_train), dv = preprocess(df_train, fit_dv=True)
    (X_val, y_val)    , _  = preprocess(df_val, dv, fit_dv=False)
    (X_test, y_test)  , _  = preprocess(df_test, dv, fit_dv=False)
    
#     print((X_train, y_train))
#     print((X_val, y_val))
#     print((X_test, y_test))


    # Save DictVectorizer and datasets
    dump_pickle(dv, "dv.pkl", dest_path)
    dump_pickle((X_train, y_train), "train.pkl", dest_path)
    dump_pickle((X_val, y_val), "val.pkl", dest_path)
    dump_pickle((X_test, y_test), "test.pkl", dest_path)


if __name__ == '__main__':
    run_data_prep()
