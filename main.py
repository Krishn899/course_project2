from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig
from networksecurity.logging.logger import logging
import sys
if __name__=='__main__':
    try:
        traingpipelineconfig_obj=TrainingPipelineConfig()
        dataingestionconfig_obj=DataIngestionConfig(traingpipelineconfig_obj)
        dataingestion_obj=DataIngestion(dataingestionconfig_obj)
        logging.info("initiating data ingestion")
        print(dataingestion_obj.initiate_data_ingestion())
    except Exception as e:
        raise NetworkSecurityException(e,sys)
