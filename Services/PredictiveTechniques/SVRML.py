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
from sklearn.preprocessing import StandardScaler
from skopt.space import Integer, Categorical, Real
import numpy as np
import time

import timeit

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
            start = timeit.default_timer()
            bestScore, bestParameters, scorePerRun = super().RunGp(x, y, "SVRML")
            took = timeit.default_timer() - start
            f = open("SVRML.txt", 'w')
            f.write(f"dtrml gp took {took}\n\n")
            f.write(f"SVRML GP bestScore:{bestScore}\n\n\n")
            f.write(', '.join([str(elem) for elem in bestParameters])+"\n\n")
            f.write(', '.join([str(elem) for elem in scorePerRun]))
            f.close()
            logging.info(f"SVRML GP bestScore:{bestScore}")
            start = timeit.default_timer()
            svrStandard = SVR(kernel=bestParameters[0], degree=bestParameters[1],
                              gamma=bestParameters[2],C=bestParameters[3],
                              epsilon=bestParameters[4],shrinking=bestParameters[5])
            x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
            svrStandard.fit(x_train.to_numpy(), y_train.to_numpy())
            testScore = svrStandard.score(x_test, y_test)
            took = timeit.default_timer() - start
            SVRML.__TrainedClassifier = svrStandard
            logging.info(f"SVRML standard run score:{testScore}")
            f = open("SVRML.txt", 'a')
            f.write(f"SVRML took {took}\n\n")
            f.write(f"SVRML standard run score:{testScore}\n\n")
            f.write(', '.join([str(elem) for elem in SVRML.__TrainedClassifier.coef_])+"\n\n")
            f.close()
        except Exception as e:
            logging.error("Error occurred while running SVRML", exc_info=True)