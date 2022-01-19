import logging
import os
import pandas as pd
from pydantic import BaseModel
from typing import List

from GaussianProcess import GaussianProcess

import datetime

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
#from sklearn.pipline import make_pipeline
from sklearn.preprocessing import StandardScaler
from skopt.space import Integer, Categorical, Real
import numpy as np
import time

from CsvFileManager import CsvFileManager

from DbContext import DbContext


class MLPML(GaussianProcess):
    __Settings = None
    __DbContext = None
    __TrainedClassifier = None
    

    def __init__(self, settings, dbContext : DbContext):
        MLPML.__Settings = settings
        MLPML.__DbContext = dbContext
        classifierSpace = [Categorical(['identity', 'logistic', 'tanh', 'relu'], name='activation'),
                          Categorical(['lbfgs', 'sgd', 'adam'], name='solver'),
                          Real(0.00005, 0.0005, name='alpha'),
                          Categorical(['constant', 'invscaling', 'adaptive'], name='learning_rate'),
                          Real(0.0005, 0.0015, name='learning_rate_init'),
                          Real(0.0001, 0.9999, name='momentum')]
        super().__init__(SVR, classifierSpace, MLPML.__Settings)

    def Run(self, x, y):
        logging.info("Running MLPML")
        try:
            bestScore, bestParameters, scorePerRun = super().RunGp(x, y)
            logging.info(f"MLPML GP bestScore:{bestScore}")
            mlpStandard = DecisionTreeRegressor(bestParameters)
            x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
            mlpStandard.fit(x_train, y_train)
            testScore = mlpStandard.score(x_test, y_test)
            MLPML.__TrainedClassifier = mlpStandard
            logging.info(f"MLPML standard run score:{testScore}")
            f = open("MLPML.txt", 'w')
            f.write(f"MLPML standard run score:{testScore}\n")
            f.write(f"MLPML GP bestScore:{bestScore}\n")
            import json
            f.write(json.dumps(bestParameters))
            f.write(json.dumps(scorePerRun))
        except Exception as e:
            logging.error("Error occurred while running MLPML", exc_info=True)