import os
import sys
from dataclasses import dataclass
from src.exceptions import CustomException
from src.logger import logging


import pandas as pd 
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import OneHotEncoder


@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifact', 'processor.pkl')


class Datatransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_processor(self):
        try:
            cat_cols = ['Type']
            num_col = ['Air temperature [K]', 'Process temperature [K]',
       'Rotational speed [rpm]', 'Torque [Nm]', 'Tool wear [min]']    

            num_pipeline = Pipeline(
                steps= 
                ("scaling", MinMaxScaler)
                )        

            cat_pipeline = Pipeline(
                ("Encoding", OneHotEncoder),
                ("Scaling", MinMaxScaler)

            )

            processors = ColumnTransformer(

                [
                    ("num_pipeline", num_pipeline, num_col),
                    ('Cat_pipeline', cat_pipeline, cat_cols)

                ]
            )
            logging.info('Transformation done')

        except Exception as e:
            raise CustomException(e, sys)
        

    def inititate_transformation(self, train_path, test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)        

            logging.info("Read train and test data")

            logging.info('Obtaining preprocessor object')

            pre_obj = self.get_processor()
            
            target_col = 'Target'
            
            train_input = train_df.drop(target_col, axis = 1)
            train_target = train_df[target_col]

            test_input = test_df.drop(target_col, axis = 1)
            test_target = test_df[target_col]


            train_array = pre_obj.fit_transform(train_input)
            test_array = pre_obj.fit_transform(test_input)

        except:
            pass