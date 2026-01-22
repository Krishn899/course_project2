from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.entity.config_entity import DataIngestionConfig,DataValidationConfig
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
        logging.info("initiating data validation")
        print(data_validation_obj.initiate_data_validation())
    except Exception as e:
        raise NetworkSecurityException(e,sys)
