
import warnings
from numba import NumbaDeprecationWarning
# Suppress NumbaDeprecationWarning in umap.distances module
warnings.filterwarnings("ignore", category=NumbaDeprecationWarning)

import os
# TensorFlow to only display error messages 
# and suppress warnings and informational messages.
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import datetime
import time
import random
import logging 
import uuid
import pytz
import pandas as pd
import io
import psycopg
import joblib

from prefect import task, flow

# Import Evidently for data drift and model performance monitoring
from evidently import ColumnMapping
from evidently.report import Report
from evidently.metrics import ColumnDriftMetric, ColumnQuantileMetric
from evidently.metrics import DatasetDriftMetric, DatasetMissingValuesMetric

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s")

SEND_TIMEOUT = 10
rand = random.Random()

create_table_statement = """
drop table if exists evidently_metrics_calculation;
create table evidently_metrics_calculation(
	timestamp timestamp,
	prediction_drift float,
	num_drifted_columns integer,
	share_missing_values float,
	column_quantile_values float
);
"""


with open('models/lin_reg.bin', 'rb') as f_in:
	model = joblib.load(f_in)	

begin = datetime.datetime(2023, 3, 1, 0, 0)
raw_data = pd.read_parquet('data/green_tripdata_2023-03.parquet')
reference_data = pd.read_parquet('data/reference.parquet')

# Define the column mapping for the Evidently report
num_features = ['passenger_count', 'trip_distance', 'fare_amount', 'total_amount']
cat_features = ['PULocationID', 'DOLocationID']
column_mapping = ColumnMapping(
    prediction='prediction',
    numerical_features=num_features,
    categorical_features=cat_features,
    target=None
)

# Create a list of metrics to include in the report
metrics = [
	ColumnDriftMetric(column_name='prediction'),
	DatasetDriftMetric(),
	DatasetMissingValuesMetric(),    
	# Add the ColumnQuantileMetric for the 'fare_amount' column
	ColumnQuantileMetric(column_name='fare_amount', quantile=0.5)
]

# Create the report with the metrics
report = Report(metrics=metrics)


@task(name="preprocces database", log_prints=None)
def prep_db():
	with psycopg.connect("host=localhost port=5432 user=postgres password=example", autocommit=True) as conn:
		res = conn.execute("SELECT 1 FROM pg_database WHERE datname='test'")
		if len(res.fetchall()) == 0:
			conn.execute("create database test;")
		with psycopg.connect("host=localhost port=5432 dbname=test user=postgres password=example") as conn:
			conn.execute(create_table_statement)


@task(name="calculate metrics", retries=2, retry_delay_seconds=5, log_prints=None)
def calculate_metrics_postgresql(curr, i):
	current_data = raw_data[(raw_data.lpep_pickup_datetime >= (begin + datetime.timedelta(i))) &
		(raw_data.lpep_pickup_datetime < (begin + datetime.timedelta(i + 1)))]

	#current_data.fillna(0, inplace=True)
	current_data['prediction'] = model.predict(current_data[num_features + cat_features].fillna(0))

	report.run(
		reference_data = reference_data, 
		current_data = current_data,
		column_mapping=column_mapping
	)
	result = report.as_dict()

	prediction_drift = result['metrics'][0]['result']['drift_score']
	num_drifted_columns = result['metrics'][1]['result']['number_of_drifted_columns']
	share_missing_values = result['metrics'][2]['result']['current']['share_of_missing_values']
	column_quantile_values = result['metrics'][3]['result']['current']['value']

	curr.execute(
		"insert into evidently_metrics_calculation(timestamp, prediction_drift, num_drifted_columns, share_missing_values, column_quantile_values) values (%s, %s, %s, %s, %s)",
		(begin + datetime.timedelta(i), prediction_drift, num_drifted_columns, share_missing_values, column_quantile_values)
	)


@flow(name="Batch Monitoring Backfill", log_prints=None)
def batch_monitoring_backfill():
	prep_db()
	last_send = datetime.datetime.now() - datetime.timedelta(seconds=10)
	with psycopg.connect("host=localhost port=5432 dbname=test user=postgres password=example", autocommit=True) as conn:
		for i in range(0, 27):
			with conn.cursor() as curr:
				calculate_metrics_postgresql(curr, i)

			new_send = datetime.datetime.now()
			seconds_elapsed = (new_send - last_send).total_seconds()
			if seconds_elapsed < SEND_TIMEOUT:
				time.sleep(SEND_TIMEOUT - seconds_elapsed)
			while last_send < new_send:
				last_send = last_send + datetime.timedelta(seconds=10)
			logging.info("data sent")


if __name__ == '__main__':
	batch_monitoring_backfill()
