import os
import sys
from src.exceptions import CustomException
from src.logger import logging
import pandas as pd

from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE
from dataclasses import dataclass

@dataclass
class DataIngesionConfig:
    train_data_path :str = os.path.join('artifact', 'train.csv')
    test_data_path :str = os.path.join('artifact', 'test.csv')
    raw_data_path :str = os.path.join('artifact', 'data.csv')


class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngesionConfig()

    def initiate_data_ingestion(self):
        logging.info("Entered Data Ingestion")
        try:
            df = pd.read_csv("notebook\data\predictive_maintenance.csv")
            logging.info('Read data')

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok = True)

            df.to_csv(self.ingestion_config.raw_data_path, index= False, header= True)

            logging.info('Train test split')

            train_set, test_set = train_test_split(df, test_size= 0.3, random_state=1000)

            train_set.to_csv(self.ingestion_config.train_data_path)
            test_set.to_csv(self.ingestion_config.test_data_path)

            logging.info("Ingestion completed")

            return (self.ingestion_config.test_data_path,
                    self.ingestion_config.test_data_path,
                    self.ingestion_config.raw_data_path)
        except Exception as e:
            raise CustomException(e,sys)
        
if __name__ == "__main__":
    obj = DataIngestion()
    obj.initiate_data_ingestion()