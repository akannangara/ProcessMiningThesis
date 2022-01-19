import logging
import os
import pandas as pd
from pydantic import BaseModel
from typing import List

from GaussianProcess import GaussianProcess

import datetime

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR
#from sklearn.pipline import make_pipeline
from sklearn.preprocessing import StandardScaler
from skopt.space import Integer, Categorical, Real
import numpy as np
import time

from CsvFileManager import CsvFileManager

from DbContext import DbContext


class SVRML(GaussianProcess):
    __Settings = None
    __DbContext = None
    __TrainedClassifier = None

    def __init__(self, settings, dbContext : DbContext):
        SVRML.__Settings = settings
        SVRML.__DbContext = dbContext
        classifierSpace = [Categorical(['linear', 'poly', 'rbf', 'sigmoid'], name='kernel'),
                           Integer(1, 5, name='degree'),
                           Categorical(['scale', 'auto'], name='gamma'),
                           Real(0.5, 1.5, name='C'),
                           Real(0.0, 0.5, name='epsilon'),
                           Categorical([True, False], name='shrinking')]
        super().__init__(SVR, classifierSpace, SVRML.__Settings)

    def Run(self, x, y):
        logging.info("Running SVRML")
        try:
            bestScore, bestParameters, scorePerRun = super().RunGp(x, y)
            logging.info(f"SVRML GP bestScore:{bestScore}")
            svrStandard = SVR(bestParameters)
            x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
            svrStandard.fit(x_train, y_train)
            testScore = svrStandard.score(x_test, y_test)
            SVRML.__TrainedClassifier = svrStandard
            logging.info(f"SVRML standard run score:{testScore}")
            f = open("SVRML.txt", 'w')
            f.write(f"SVRML standard run score:{testScore}\n")
            f.write(f"SVRML GP bestScore:{bestScore}\n")
            import json
            f.write(json.dumps(bestParameters))
            f.write(json.dumps(scorePerRun))
        except Exception as e:
            logging.error("Error occurred while running SVRML", exc_info=True)