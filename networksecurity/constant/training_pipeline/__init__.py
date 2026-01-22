import os
import sys
import numpy as np
import pandas as pd

DATA_INGESTION_COLLECTION_NAME:str="NETWORK_DATA"
DATA_INGESTION_DATABASE_NAME:str="NETWORK_SECURITY_DB"
DATA_INGESTION_DIR_NAME:str="data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR_NAME:str="feature_store"
DATA_INGESTION_INGESTED_DIR_NAME:str="ingested"
DATA_INGESTION_TRAIN_TEST_RATIO:float=0.25

TARGET_COLUMN="Result"
PIPELINE_NAME:str="NetworkSecurity"
ARTIFACT_DIR:str="Artifacts"
FILE_NAME:str="uci-ml-phishing-dataset.csv"
SCHEMA_FILE_PATH=os.path.join("data_schema","schema.yaml")

TRAIN_FILE_NAME:str="train.csv"
TEST_FILE_NAME:str='test.csv'

DATA_VALIDATION_DIR_NAME:str="data_validation"
DATA_VALIDATION_VALID_DIR_NAME:str="valid"
DATA_VALIDATION_INVALID_DIR_NAME:str="invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR_NAME:str="drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME:str="report.yml"