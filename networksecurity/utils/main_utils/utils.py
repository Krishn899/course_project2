import dill 
import pickle
import os
import sys
import numpy as np
import pandas as pd
import yaml
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score
def read_yaml_file(file_path:str)->dict:
    try:
        with open(file_path,'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def write_yaml_file(file_path:str,content:object,replace:bool=False)->None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,'w') as file_obj:
            yaml.dump(content,file_obj)
    except Exception as e:
        raise NetworkSecurityException(e,sys)

def save_numpy_array_data(file_path:str,array:np.array):
    try:
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        
        # Remove existing file if it exists to avoid permission errors
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception:
                pass  # If removal fails, attempt to overwrite
        
        with open(file_path,'wb') as file_obj:
            np.save(file_obj,array)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def save_obj(file_path:str,obj:object)->None:
    try:
        logging.info("saving the object.....")
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        
        # Remove existing file if it exists to avoid permission errors
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception:
                pass  # If removal fails, attempt to overwrite
        
        with open(file_path,"wb") as file_obj:
            pickle.dump(obj=obj,file=file_obj)
        logging.info("object saved sucessfully")
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def load_obj(file_path:str):
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file path:{file_path} doesn't exists")
        with open(file_path,"rb") as file_obj:
            print(file_obj)
            return pickle.load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def load_numpy_array_data(file_path:str):
    try:
        with open(file_path,"rb") as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def evaluate_models(x_train,y_train,x_test,y_test,models:dict,params)->dict:
    try:
        report:dict={}
        for i in range(len(list(models))):
            model=list(models.values())[i]
            para=params[list(models.keys())[i]]

            rs=GridSearchCV(model,para,cv=3)
            rs.fit(x_train,y_train)

            model.set_params(**rs.best_params_)
            model.fit(x_train,y_train)

            y_train_pred=model.predict(x_train)
            y_test_pred=model.predict(x_test)

            train_model_score=r2_score(y_pred=y_train_pred,y_true=y_train)
            test_model_score=r2_score(y_pred=y_test_pred,y_true=y_test)

            report[list(models.keys())[i]]=test_model_score
        return report
    except Exception as e:
        raise NetworkSecurityException(e,sys)