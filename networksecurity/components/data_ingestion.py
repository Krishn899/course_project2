from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact
import os
import sys
from sklearn.model_selection import train_test_split
import pymongo
from typing import List
from dotenv import load_dotenv
import pandas as pd
import numpy as np
load_dotenv()

MONGO_DB_URL=os.getenv("MONGO_DB_URL")

class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config=data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def export_collection_as_df(self):
        try:
            logging.info("ENTERED export_collection_as_df function")
            db_name=self.data_ingestion_config.database_name
            collection_name=self.data_ingestion_config.collection_name
            self.mongo_client=pymongo.MongoClient(MONGO_DB_URL)
            collection=self.mongo_client[db_name][collection_name]
            df=pd.DataFrame(list(collection.find()))
            if "_id" in df.columns.to_list():
                df=df.drop(columns=['_id'],axis=1)
            df.replace({"na":np.nan},inplace=True)
            logging.info("EXITING export_collection_as_df function")
            return df
        except Exception as e:
            raise NetworkSecurityException(e,sys)
         
    def export_data_to_feature_store(self,dataframe:pd.DataFrame):
        try:
            logging.info("ENTERED export_data_to_feature_store function")
            feature_store_file_path=self.data_ingestion_config.feature_store_file_path
            dir_path=os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            dataframe.to_csv(feature_store_file_path,index=False,header=True)
            logging.info("EXITING export_data_to_feature_store function")
            return dataframe
        except Exception as e:
            raise NetworkSecurityException(e,sys)
            
    def split_data_to_train_test(self,dataframe:pd.DataFrame):
        try:
            logging.info("ENTERED split_data_to_train_test function")
            train_set,test_set=train_test_split(
                dataframe,test_size=self.data_ingestion_config.train_test_split_ratio,random_state=42
            )
            logging.info("completed train test split")
            dir_path=os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path,exist_ok=True)
            logging.info("exporting train test file path")
            train_set.to_csv(
                self.data_ingestion_config.training_file_path,index=False,header=True
            )
            test_set.to_csv(
                self.data_ingestion_config.testing_file_path,index=False,header=True
            )
            logging.info("exported train and test file")
            logging.info("exiting split_data_to_train_test function")
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    
    def initiate_data_ingestion(self):
        try:
            logging.info("ENTERED initiate_data_ingestion function")
            df=self.export_collection_as_df()
            df=self.export_data_to_feature_store(df)
            self.split_data_to_train_test(df)
            data_ingestion_artifact=DataIngestionArtifact(
                train_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path
            )
            return data_ingestion_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
