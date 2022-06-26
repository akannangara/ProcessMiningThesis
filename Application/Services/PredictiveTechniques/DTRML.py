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
        

    def Run(self, x, y, name : str):
        logging.info(f"Running {name}")
        try:
            start = timeit.default_timer()
            bestScore, bestParameters, scorePerRun = super().RunGp(x, y, f"{name}")
            took = timeit.default_timer() - start
            f = open(name+".txt", 'w')
            f.write(f"{name} gp took {took}\n\n")
            f.write(f"{name} GP bestScore:{bestScore}\n\n")
            f.write(', '.join([str(elem) for elem in bestParameters])+"\n\n")
            f.write(', '.join([str(elem) for elem in scorePerRun])+"\n\n")
            f.close()

            import matplotlib.pyplot as plt
            plt.clf()
            plt.plot(np.arange(1, len(scorePerRun) +1), scorePerRun)
            plt.title(f"DTR score per GP run")
            plt.xlabel("Run count")
            plt.ylabel("Mean absolute error")
            repsoitoryLocation = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../Domain/Repositories")
            imagesSink = os.path.join(repsoitoryLocation,  DTRML.__Settings.ImageStorage["ImagesSinkProcessDiscovery"])
            plt.grid(visible=True, axis='both', which='both')
            plt.xlim(xmin=0)
            plt.savefig(os.path.join(imagesSink, f"{name}_score_per_gp_run.png"))
            del plt

            logging.info(f"{name} GP bestScore:{bestScore}")
            start = timeit.default_timer()
            dtrStandard = DecisionTreeRegressor(criterion=bestParameters[0], splitter=bestParameters[1], max_depth=bestParameters[2],
                                                min_samples_split=bestParameters[3],min_samples_leaf=bestParameters[4],
                                                min_weight_fraction_leaf=bestParameters[5],max_features=bestParameters[6],
                                                max_leaf_nodes=bestParameters[7],min_impurity_decrease=bestParameters[8])
            x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
            dtrStandard.fit(x_train, y_train)
            testScore = dtrStandard.score(x_test, y_test)
            took = timeit.default_timer() - start
            DTRML.__TrainedClassifier = dtrStandard
            logging.info(f"{name} standard run score:{testScore}")
            f = open(f"{name}.txt", 'a')
            f.write(f"{name} standard run score:{testScore}\n\n")
            f.write(f"{name} took {took}\n\n")
            f.write(', '.join([str(elem) for elem in DTRML.__TrainedClassifier.feature_importances_])+"\n\n")
            f.close()

            return scorePerRun
        except Exception as e:
            logging.error(f"Error occurred while running {name}", exc_info=True)