import sys
from networksecurity.logging import logger
class NetworkSecurityException(Exception):
    def __init__(self, error_message,error_details:sys):
        self.error_message=error_message
        _,_,exc_tb=error_details.exc_info()
        self.lineno=exc_tb.tb_lineno
        self.file_name=exc_tb.tb_frame.f_code.co_filename
    
    def __str__(self):
        return "ERROR OCCURED IN PYTHON SCRIPT NAME [{0}] LINE NUMBER [{1}] ERROR MESSAGE [{2}]".format(
            self.file_name,self.lineno,str(self.error_message)
        )
    