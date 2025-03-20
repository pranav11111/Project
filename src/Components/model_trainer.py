import os
import sys
from src.exceptions import CustomException
from src.logger import logging
from src.utils import save_obj
from dataclasses import dataclass

import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score, confusion_matrix


@dataclass
class ModelTrainerConfig:
    trainer_obj_file_path = os.path.join('artifact','trainer.pkl')

class ModelTrainer:
    def __init__(self):
        self.modeltrainerconfig = ModelTrainerConfig()

    def initate_model_trainer(self, train_array, test_array):
        try:
            x_train, y_train, x_test, y_test = (
                train_array[:, :-1],
                train_array[:, -1],
                test_array[:, :-1],
                test_array[:, -1],
            )

            logging.info("Training started")

            model =  RandomForestClassifier(n_estimators = 100, min_samples_split = 2,  max_depth = 17, criterion = 'entropy' )
            model.fit(x_train, y_train)
            train_pred = model.predict(x_train)
            test_pred  = model.predict(x_test)
            

            print('Train f1 score is: {}'.format(f1_score(y_train, train_pred)))
            print('Test f1 score is: {}'.format(f1_score(y_test, test_pred)))
            
            print(confusion_matrix(y_test, test_pred))
            
            logging.info("f1_score{}".format(f1_score(y_test, test_pred)))

            save_obj(self.modeltrainerconfig.trainer_obj_file_path, model)
        
        except Exception as e:
            raise CustomException(e, sys)
            