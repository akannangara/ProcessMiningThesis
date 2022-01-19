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

import timeit

from CsvFileManager import CsvFileManager

from DbContext import DbContext


class DTRML(GaussianProcess):
    __Settings = None
    __DbContext = None
    __TrainedClassifier = None

    def __init__(self, settings, dbContext : DbContext, datasetSize : int):
        DTRML.__Settings = settings
        DTRML.__DbContext = dbContext
        classifierSpace = [Categorical(['mse', 'friedman_mse', 'mae'], name='criterion'),
			                    Categorical(['best','random'], name='splitter'),
			                    Integer(1, datasetSize, name='max_depth'),
			                    Integer(2, datasetSize, name='min_samples_split'),
			                    Integer(1, datasetSize, name='min_samples_leaf'),
			                    Real(0.0, 0.5, name='min_weight_fraction_leaf'),
			                    Categorical(['auto','sqrt','log2',None], name='max_features'),
			                    Integer(2, datasetSize, name='max_leaf_nodes'),
			                    Real(0.0, 1.0, name='min_impurity_decrease')]
        super().__init__(DecisionTreeRegressor, classifierSpace, DTRML.__Settings)
        

    def Run(self, x, y):
        logging.info("Running DTRML")
        try:
            start = timeit.default_timer()
            bestScore, bestParameters, scorePerRun = super().RunGp(x, y, "DTRML")
            took = timeit.default_timer() - start
            f = open("dtrml.txt", 'w')
            f.write(f"dtrml gp took {took}\n\n")
            f.write(f"DTRML GP bestScore:{bestScore}\n\n")
            f.write(', '.join([str(elem) for elem in bestParameters])+"\n\n")
            f.write(', '.join([str(elem) for elem in scorePerRun])+"\n\n")
            f.close()
            logging.info(f"DTRML GP bestScore:{bestScore}")
            start = timeit.default_timer()
            dtrStandard = DecisionTreeRegressor(criterion=bestParameters[0], splitter=bestParameters[1], max_depth=bestParameters[2],
                                                min_samples_split=bestParameters[3],min_samples_leaf=bestParameters[4],
                                                min_weight_fraction_leaf=bestParameters[5],max_features=bestParameters[6],
                                                max_leaf_nodes=bestParameters[7],min_impurity_decrease=bestParameters[8])
            x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
            dtrStandard.fit(x_train.to_numpy(), y_train.to_numpy())
            testScore = dtrStandard.score(x_test, y_test)
            took = timeit.default_timer() - start
            DTRML.__TrainedClassifier = dtrStandard
            logging.info(f"DTRML standard run score:{testScore}")
            f = open("dtrml.txt", 'a')
            f.write(f"DTRML standard run score:{testScore}\n\n")
            f.write(f"dtrml took {took}\n\n")
            f.write(', '.join([str(elem) for elem in DTRML.__TrainedClassifier.feature_importances_])+"\n\n")
            f.close()
        except Exception as e:
            logging.error("Error occurred while running DTRML", exc_info=True)