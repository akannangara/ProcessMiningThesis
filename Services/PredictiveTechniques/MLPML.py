import logging
import os
import pandas as pd
from pydantic import BaseModel
from typing import List

from GaussianProcess import GaussianProcess

import datetime

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
#from sklearn.pipline import make_pipeline
from sklearn.preprocessing import StandardScaler
from skopt.space import Integer, Categorical, Real
import numpy as np
import time

import timeit

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
        super().__init__(MLPRegressor, classifierSpace, MLPML.__Settings)

    def Run(self, x, y):
        logging.info("Running MLPML")
        try:
            start = timeit.default_timer()
            bestScore, bestParameters, scorePerRun = super().RunGp(x, y, "MLPML")
            took = timeit.default_timer() - start
            f = open("MLPML.txt", 'w')
            f.write(f"mlpml gp took {took}\n\n")
            f.write(f"MLPML GP bestScore:{bestScore}\n\n\n")
            f.write(', '.join([str(elem) for elem in bestParameters])+ "\n\n")
            f.write(', '.join([str(elem) for elem in scorePerRun])+ "\n\n")
            f.close()
            
            start = timeit.default_timer()
            mlpStandard = MLPRegressor(activation=bestParameters[0],solver=bestParameters[1],alpha=bestParameters[2],
                                       learning_rate=bestParameters[3],learning_rate_init=bestParameters[4],
                                       momentum=bestParameters[5])
            x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
            mlpStandard.fit(x_train.to_numpy(), y_train.to_numpy())
            testScore = mlpStandard.score(x_test, y_test)
            took = timeit.default_timer() - start
            f = open("MLPML.txt", 'a')
            f.write(f"mlpml took {took}\n\n")
            f.write(f"MLPML standard run score:{testScore}\n")
            f.close()
            MLPML.__TrainedClassifier = mlpStandard
            logging.info(f"MLPML standard run score:{testScore}")

        except Exception as e:
            logging.error("Error occurred while running MLPML", exc_info=True)