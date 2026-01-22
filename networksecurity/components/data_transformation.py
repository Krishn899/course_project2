import os,sys
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.artifact_entity import DataTransformationArtifact,DataValidationArtifact
from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.constant.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS,TARGET_COLUMN
from networksecurity.utils.main_utils.utils import save_numpy_array_data,save_obj

class DataTranformation:
    def __init__(self,data_tranformation_config:DataTransformationConfig,data_validation_artifact:DataValidationArtifact):
        try:
            self.data_validation_artifact:DataValidationArtifact=data_validation_artifact
            self.data_transformation_config:DataTransformationConfig=data_tranformation_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            logging.info("reading data...")
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def get_data_transformer_object(cls)->Pipeline:
        logging.info("entered get_data_transformer_object")
        try:
            imputer:KNNImputer=KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            processor:Pipeline=Pipeline([
                ("imputer",imputer)
            ])
            return processor
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def initiate_data_transformation(self)->DataTransformationArtifact:
        try:
            logging.info("initiating data transformation...")
            train_df=DataTranformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df=DataTranformation.read_data(self.data_validation_artifact.valid_test_file_path)

            #training df
            input_feature_train_df=train_df.drop(columns=[TARGET_COLUMN],axis=1)
            input_feature_test_df=test_df.drop(columns=[TARGET_COLUMN],axis=1)
            output_feature_train_df=train_df[TARGET_COLUMN]
            output_feature_train_df=output_feature_train_df.replace(-1,0)
            output_feature_test_df=test_df[TARGET_COLUMN]
            output_feature_test_df=output_feature_test_df.replace(-1,0)

            #transforming
            preprocessor=self.get_data_transformer_object()
            preprocessor_object=preprocessor.fit(input_feature_train_df)
            transformed_input_feature_train_df=preprocessor_object.transform(input_feature_train_df)
            transformed_input_feature_test_df=preprocessor_object.transform(input_feature_test_df)

            #train_arr,test_arr
            train_arr=np.c_[transformed_input_feature_train_df,np.array(output_feature_train_df)]
            test_arr=np.c_[transformed_input_feature_test_df,np.array(output_feature_test_df)]

            #saving numpy array data
            save_numpy_array_data(self.data_transformation_config.data_transformed_train_file_path,train_arr)
            save_numpy_array_data(self.data_transformation_config.data_transformed_test_file_path,test_arr)
            save_obj(self.data_transformation_config.data_transformed_object_file_path,preprocessor_object)

            data_transformation_artifact:DataTransformationArtifact=DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.data_transformed_object_file_path,
                transformed_test_file_path=self.data_transformation_config.data_transformed_test_file_path,
                transformed_train_file_path=self.data_transformation_config.data_transformed_train_file_path
            )
            logging.info("data transformation completed")
            return data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)