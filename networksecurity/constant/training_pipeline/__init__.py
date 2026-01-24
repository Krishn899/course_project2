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
MODEL_FILE_NAME:str="model.pkl"
SAVED_MODEL_DIR:str=os.path.join("saved_models")

TRAIN_FILE_NAME:str="train.csv"
TEST_FILE_NAME:str='test.csv'
PREPROCESSING_OBJECT_FILE_NAME:str="preprocessor.pkl"
MODEL_OBJECT_FILE_NAME:str="network.pkl"

DATA_VALIDATION_DIR_NAME:str="data_validation"
DATA_VALIDATION_VALID_DIR_NAME:str="valid"
DATA_VALIDATION_INVALID_DIR_NAME:str="invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR_NAME:str="drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME:str="report.yml"

DATA_TRANSFORMATION_DIR_NAME:str="data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR_NAME:str="transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR_NAME:str="transformed_object"
DATA_TRANSFORMATION_IMPUTER_PARAMS:dict={
    "missing_values": np.nan,
    "n_neighbors":3,
    "weights":"uniform"
}

MODEL_TRAINER_DIR_NAME:str="model_trainer"
MODEL_TRAINER_EXPECTED_SCORE:float=0.6
MODEL_TRAINER_OVERFITTING_UNDERFITTING_THRESHOLD:float=0.05
MODEL_TRAINER_TRAINED_MODEL_DIR:str="trained_model"