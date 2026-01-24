import os,sys
import pandas as pd
import numpy as np

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.artifact_entity import ModelTrainerArtifact,DataTransformationArtifact
from networksecurity.entity.config_entity import ModelTrainerConfig
from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from networksecurity.utils.ml_utils.metrics.classification_metric import get_classifaction_score
from networksecurity.utils.main_utils.utils import save_obj,load_obj,load_numpy_array_data,evaluate_models

from sklearn.tree import DecisionTreeClassifier,ExtraTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import AdaBoostClassifier,GradientBoostingClassifier,RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import r2_score


class ModelTrainer:
    def __init__(self,model_trainer_config:ModelTrainerConfig,data_transformation_artifact:DataTransformationArtifact):
        try:
            self.model_trainer_config=model_trainer_config
            self.data_transformation_artifact=data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def train_model(self,x_train,y_train,x_test,y_test):
        try:
            models={
                "Random forest":RandomForestClassifier(verbose=1),
                "decision tree":DecisionTreeClassifier(),
                "logistic Regression":LogisticRegression(verbose=1),
                "adaboost":AdaBoostClassifier(),
                "gradient boost":GradientBoostingClassifier(verbose=1),
                "k neighbors":KNeighborsClassifier(),
                "extra tree":ExtraTreeClassifier()
            }
            params={
                "Random forest":{
                    'criterion':['gini','entropy','log_loss'],
                    'n_estimators':[8,16,32,64,128,256]
                },
                "decision tree":{
                    'criterion':['gini','entropy','log_loss']
                },
                "logistic Regression":{
                    "max_iter":[100,200,300,400,500]
                },
                "adaboost":{
                    'learning_rate':[.001,.01,.05,0.1],
                    'n_estimators':[8,16,32,64,128,256]
                },
                "gradient boost":{
                    'learning_rate':[.001,.01,.05,0.1],
                    'subsample':[0.6,0.7,0.75,0.8,0.85,0.9]
                },
                "k neighbors":{
                    'n_neighbors':[3,5,7,9,10]
                },
                "extra tree":{}
            }
            model_report:dict=evaluate_models(x_train=x_train,y_train=y_train,x_test=x_test,y_test=y_test,models=models,params=params)

            best_model_score=max(sorted(model_report.values()))
            best_model_name=list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]

            best_model=models[best_model_name]

            y_train_pred=best_model.predict(x_train)
            classification_train_metric=get_classifaction_score(y_pred=y_train_pred,y_true=y_train)
            
            ##to track the mlflow


            y_test_pred=best_model.predict(x_test)
            classification_test_metric=get_classifaction_score(y_pred=y_test_pred,y_true=y_test)

            preprocessor=load_obj(file_path=self.data_transformation_artifact.transformed_object_file_path)

            model_dir_path=os.path.dirname(self.model_trainer_config.trained_model_file_path)
            os.makedirs(model_dir_path,exist_ok=True)

            network_model_obj=NetworkModel(preprocessor=preprocessor,model=best_model)
            save_obj(self.model_trainer_config.trained_model_file_path,obj=network_model_obj)

            #model trainer artifact
            model_trainer_artifact:ModelTrainerArtifact=ModelTrainerArtifact(
                trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                training_metric_artifact=classification_train_metric,
                test_metric_artifact=classification_test_metric
            )
            logging.info
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def initiate_model_trainer(self)->ModelTrainerArtifact:
        try:
            train_file_path=self.data_transformation_artifact.transformed_train_file_path
            test_file_path=self.data_transformation_artifact.transformed_test_file_path

            #reading train and test data
            train_arr=load_numpy_array_data(train_file_path)
            test_arr=load_numpy_array_data(test_file_path)

            x_train,y_train,x_test,y_test=(
                train_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,:-1],
                test_arr[:,-1]
            )
            model=self.train_model(x_train=x_train,y_train=y_train,x_test=x_test,y_test=y_test)
            return model
        except Exception as e:
            raise NetworkSecurityException(e,sys)