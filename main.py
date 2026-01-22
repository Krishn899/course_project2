from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTranformation
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.entity.config_entity import DataIngestionConfig,DataValidationConfig,DataTransformationConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig
from networksecurity.logging.logger import logging
import sys
if __name__=='__main__':
    try:
        traingpipelineconfig_obj=TrainingPipelineConfig()
        dataingestionconfig_obj=DataIngestionConfig(traingpipelineconfig_obj)
        dataingestion_obj=DataIngestion(dataingestionconfig_obj)
        logging.info("initiating data ingestion")
        dataingestion_artifact=dataingestion_obj.initiate_data_ingestion()
        logging.info("data validation initiated")
        data_validation_config_obj=DataValidationConfig(training_pipeline_config=traingpipelineconfig_obj)
        data_validation_obj=DataValidation(data_validation_config=data_validation_config_obj,data_ingestion_artifact=dataingestion_artifact)
        data_validation_artifact=data_validation_obj.initiate_data_validation()
        logging.info("data validation completed")
        data_transformation_config_obj=DataTransformationConfig(training_pipeline_config=traingpipelineconfig_obj)
        data_transformation_obj=DataTranformation(data_validation_artifact=data_validation_artifact,data_tranformation_config=data_transformation_config_obj)
        data_transformation_obj.initiate_data_transformation()
    except Exception as e:
        raise NetworkSecurityException(e,sys)
