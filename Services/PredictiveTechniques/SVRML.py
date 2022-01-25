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
    __Space = None

    def __init__(self, settings, dbContext : DbContext):
        SVRML.__Settings = settings
        SVRML.__DbContext = dbContext
        classifierSpace = [Categorical(['linear', 'poly', 'rbf', 'sigmoid'], name='kernel'),
                           Integer(1, 5, name='degree'),
                           Categorical(['scale', 'auto'], name='gamma'),
                           Real(0.5, 1.5, name='C'),
                           Real(0.0, 0.5, name='epsilon'),
                           Categorical([True, False], name='shrinking')]
        classifierSpaceLinear = [Real(0.00005, 0.00015, name='tol'),
                                 Real(0.1,1.0, name='C'),
                                 Categorical([True, False], name='fit_intercept'),
                                 Real(0.5,1.0, name='intercept_scaling'),
                                 Integer(1000,5000, name='max_iter')]
        super().__init__(LinearSVR, classifierSpaceLinear, SVRML.__Settings)

    def Run(self, x, y, name : str):
        logging.info(f"Running {name}")
        try:
            start = timeit.default_timer()
            bestScore, bestParameters, scorePerRun = super().RunGp(x, y, name)
            took = timeit.default_timer() - start
            f = open(name+".txt", 'w')
            f.write(f"{name} gp took {took}\n\n")
            f.write(f"{name} GP bestScore:{bestScore}\n\n\n")
            f.write(', '.join([str(elem) for elem in bestParameters])+"\n\n")
            f.write(', '.join([str(elem) for elem in scorePerRun]))
            f.close()

            import matplotlib.pyplot as plt
            plt.clf()
            plt.plot(np.arange(1, len(scorePerRun) +1), scorePerRun)
            plt.title(f"SVR score per GP run")
            plt.xlabel("Run count")
            plt.ylabel("Mean absolute error")
            plt.grid(visible=True, axis='both', which='both')
            plt.xlim(xmin=0)
            repsoitoryLocation = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../Domain/Repositories")
            imagesSink = os.path.join(repsoitoryLocation,  SVRML.__Settings.ImageStorage["ImagesSinkProcessDiscovery"])
            plt.savefig(os.path.join(imagesSink, f"{name}_score_per_gp_run.png"))

            logging.info(f"{name} GP bestScore:{bestScore}\n\n")
            start = timeit.default_timer()
            svrStandard = LinearSVR(tol=bestParameters[0], C=bestParameters[1], loss='epsilon_insensitive', fit_intercept=bestParameters[2], intercept_scaling=bestParameters[3], max_iter=bestParameters[4])
            x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
            svrStandard.fit(x_train, y_train)
            testScore = svrStandard.score(x_test, y_test)
            took = timeit.default_timer() - start
            SVRML.__TrainedClassifier = svrStandard
            logging.info(f"{name} standard run score:{testScore}")
            y_pred = svrStandard.predict(x_test)
            u = ((y_test - y_pred)**2).sum()
            v = ((y_test - y_test.mean())**2).sum()
            logging.info(f"{name} u:{u}")
            logging.info(f"{name} v:{v}")
            r2 = 1-(u/v)
            logging.info(f"{name} r2:{r2}")

            f = open(name+".txt", 'a')
            f.write(f"{name} took {took}\n\n")
            f.write(f"{name} standard run score:{testScore}\n\n")
            f.write(', '.join([str(elem) for elem in SVRML.__TrainedClassifier.coef_])+"\n\n")
            f.close()

            return scorePerRun
        except Exception as e:
            logging.error(f"Error occurred while running {name}", exc_info=True)