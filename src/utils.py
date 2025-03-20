import os
import sys
from src.exceptions import CustomException

import pandas as pd
import numpy as np
import pickle


def save_obj(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path, exist_ok= True)

        with open(file_path, 'wb') as fileobj:
            pickle.dump(obj, fileobj)

    except Exception as e:
        raise CustomException(e, sys)