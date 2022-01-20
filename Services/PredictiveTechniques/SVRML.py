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
from sklearn.svm import LinearSVR
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
        classifierSpaceLinear = [Categorical(['epsilon_insensitive', 'squared_epsilon_insensitive'], name='loss'),
                                 Categorical([True, False], name='fit_intercept'),
                                 Categorical([False], name='dual')]
        super().__init__(SVR, classifierSpace, SVRML.__Settings)

    def Run(self, x, y, name : str):
        logging.info(f"Running {name}")
        try:
            start = timeit.default_timer()
            bestScore, bestParameters, scorePerRun = super().RunGp(x, y, "SVRML")
            took = timeit.default_timer() - start
            f = open(name+".txt", 'w')
            f.write(f"{name} gp took {took}\n\n")
            f.write(f"{name} GP bestScore:{bestScore}\n\n\n")
            f.write(', '.join([str(elem) for elem in bestParameters])+"\n\n")
            f.write(', '.join([str(elem) for elem in scorePerRun]))
            f.close()
            logging.info(f"{name} GP bestScore:{bestScore}")
            start = timeit.default_timer()
            svrStandard = SVR(kernel=bestParameters[0], degree=bestParameters[1],
                              gamma=bestParameters[2],C=bestParameters[3],
                              epsilon=bestParameters[4],shrinking=bestParameters[5])
            #svrStandard = LinearSVR(loss=bestParameters[0], fit_intercept=bestParameters[1], dual=False)
            x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
            svrStandard.fit(x_train, y_train)
            testScore = svrStandard.score(x_test, y_test)
            #testScore = (abs(y_test - svrStandard.predict(x_test)).sum()) / x_test.size
            took = timeit.default_timer() - start
            SVRML.__TrainedClassifier = svrStandard
            logging.info(f"{name} standard run score:{testScore}")
            f = open(name+".txt", 'a')
            f.write(f"{name} took {took}\n\n")
            f.write(f"{name} standard run score:{testScore}\n\n")
            f.write(', '.join([str(elem) for elem in SVRML.__TrainedClassifier.coef_])+"\n\n")
            f.close()
        except Exception as e:
            logging.error(f"Error occurred while running {name}", exc_info=True)