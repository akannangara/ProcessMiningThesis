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

from sklearn.metrics import accuracy_score
from sklearn.feature_selection import chi2

from CsvFileManager import CsvFileManager

from DbContext import DbContext


class MLPML(GaussianProcess):
    __Settings = None
    __DbContext = None
    __TrainedClassifier = None
    

    def __init__(self, settings, dbContext : DbContext):
        MLPML.__Settings = settings
        MLPML.__DbContext = dbContext
        classifierSpace = [Categorical(['identity', 'logistic', 'tanh','relu'], name='activation'),
                          Categorical(['lbfgs', 'adam'], name='solver'),
                          Real(0.00005, 0.0005, name='alpha'),
                          Categorical(['constant', 'invscaling', 'adaptive'], name='learning_rate'),
                          Real(0.0000, 0.9999, name='momentum'),
                          Integer(200, 1000, name='max_iter')]
        super().__init__(MLPRegressor, classifierSpace, MLPML.__Settings)

    def Run(self, x, y, name : str):
        logging.info(f"Running {name}")
        try:
            start = timeit.default_timer()
            bestScore, bestParameters, scorePerRun = super().RunGp(x, y, name)
            took = timeit.default_timer() - start
            f = open(name+".txt", 'w')
            f.write(f"{name} gp took {took}\n\n")
            f.write(f"{name} GP bestScore:{bestScore}\n\n\n")
            f.write(', '.join([str(elem) for elem in bestParameters])+ "\n\n")
            f.write(', '.join([str(elem) for elem in scorePerRun])+ "\n\n")
            f.close()
            
            start = timeit.default_timer()
            mlpStandard = MLPRegressor(activation=bestParameters[0],
                                       solver=bestParameters[1],
                                       alpha=bestParameters[2],
                                       learning_rate=bestParameters[3],
                                       momentum=bestParameters[4],
                                       max_iter=bestParameters[5])
            x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
            mlpStandard.fit(x_train, y_train)
            testScore = mlpStandard.score(x_test.to_numpy(), y_test.to_numpy())
            logging.info(f"{name} test score is {testScore}")
            took = timeit.default_timer() - start

            chi_scores_all = chi2(x, y)
            chi_scores_ML = chi2(x_train, y_train)

            f = open(name+".txt", 'a')
            f.write(f"{name} took {took}\n\n")
            f.write(f"{name} standard run score:{testScore}\n\n")
            f.write(f"{name} feature importance is "+', '.join([str(elem) for elem in chi_scores_ML[0]])+ "\n\n")
            f.write(f"{name} feature importance over all is "+', '.join([str(elem) for elem in chi_scores_all[0]])+ "\n\n")
            f.close()
            MLPML.__TrainedClassifier = mlpStandard
            logging.info(f"{name} standard run score:{testScore}")

        except Exception as e:
            logging.error(f"Error occurred while running {name}", exc_info=True)