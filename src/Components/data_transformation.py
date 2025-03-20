import os
import sys
from dataclasses import dataclass
from src.exceptions import CustomException
from src.logger import logging
from src.utils import save_obj


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
               [ ("scaling", MinMaxScaler())]
                )        

            cat_pipeline = Pipeline(
                steps=
                [("Encoding", OneHotEncoder(sparse_output=False)),
                ("Scaling", MinMaxScaler())]

            )

            processors = ColumnTransformer(

                [
                    ("num_pipeline", num_pipeline, num_col),
                    ('Cat_pipeline', cat_pipeline, cat_cols)

                ]
            )
            logging.info('Transformation done')

            return processors

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


            train_input_array = pre_obj.fit_transform(train_input)
            test_input_array = pre_obj.transform(test_input)

            train_array = np.c_[
                train_input_array, np.array(train_target)
            ]
            test_array = np.c_[
                test_input_array, np.array(test_target)
            ]

            logging.info('Saving preprocesser object')

            save_obj(
                file_path = self.data_transformation_config.preprocessor_obj_file_path,
                obj = pre_obj
            )

            return (train_array, test_array, self.data_transformation_config.preprocessor_obj_file_path)
        except Exception as e:
            raise CustomException(e, sys)