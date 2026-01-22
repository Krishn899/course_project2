from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
from scipy.stats import ks_2samp
from networksecurity.constant.training_pipeline import SCHEMA_FILE_PATH
from networksecurity.utils.main_utils.utils import read_yaml_file,write_yaml_file
import os
import sys
import pandas as pd
import numpy as np

class DataValidation:
    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,
                 data_validation_config:DataValidationConfig):
        try:
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_validation_config=data_validation_config
            self.schema_config=read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def validate_number_of_coloumn(self,df:pd.DataFrame)->bool:
        try:
            number_of_coloumn=len(self.schema_config)
            logging.info(f"required numbe of column: {number_of_coloumn}")
            logging.info(f"data frame has column: {len(df.columns)}")
            return len(df.columns)==number_of_coloumn
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def detect_dataset_drift(self,base_df:pd.DataFrame,current_df:pd.DataFrame,threshold=0.05)->bool:
        try:
            status=True
            report={}
            for column in base_df.columns:
                d1=base_df[column]
                d2=current_df[column]
                is_sample_dist=ks_2samp(d1,d2)
                if threshold<=is_sample_dist.pvalue:
                    is_found=True
                else:
                    is_found=False
                    status=False
                report.update(
                    {column:{
                        "p_value":float(is_sample_dist.pvalue),
                        "drift_status":is_found
                    }}
                )

                #create directory
            dir_path=os.path.dirname(self.data_validation_config.drift_report_file_path)
            os.makedirs(dir_path,exist_ok=True)
            write_yaml_file(file_path=self.data_validation_config.drift_report_file_path,content=report)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
            
    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            train_file_path=self.data_ingestion_artifact.train_file_path
            test_file_path=self.data_ingestion_artifact.test_file_path

            #read the train and test
            train_df=DataValidation.read_data(train_file_path)
            test_df=DataValidation.read_data(test_file_path)

            #validate no. of column
            status=self.validate_number_of_coloumn(df=train_df)
            if not status:
                error_message=f"Train dataframe doesnt contain all column.\n"
            status=self.validate_number_of_coloumn(df=test_df)
            if not status:
                error_message=f"Test dataframe doesnt contain all column.\n"

            #check data drift
            status=self.detect_dataset_drift(base_df=train_df,current_df=test_df)
            dir_path=os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path,exist_ok=True)

            train_df.to_csv(
                self.data_validation_config.valid_train_file_path,index=False,header=True
            )
            test_df.to_csv(
                self.data_validation_config.valid_test_file_path,index=False,header=True
            )

            data_validation_artifact=DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_ingestion_artifact.train_file_path,
                valid_test_file_path=self.data_ingestion_artifact.test_file_path,
                invalid_test_file_path=None,
                invalid_train_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )
            return data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)