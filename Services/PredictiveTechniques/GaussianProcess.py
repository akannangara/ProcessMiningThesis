import logging
import os
import pandas as pd
from pydantic import BaseModel
from typing import List

import datetime

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.svm import SVR
from skopt import gp_minimize
from skopt.space import Integer, Categorical, Real
import time


class GaussianProcess(BaseModel):
    __Classifier = None
    __HyperparameterSpace = None
    __GaussianSettings = None
    __X = None
    __Y = None

    def __init__(self, classifier, hyperparameterSpace : List, settings):
        GaussianProcess.__GaussianSettings = settings.GaussianProcess
        GaussianProcess.__Classifier = classifier
        GaussianProcess.__HyperparameterSpace = hyperparameterSpace

    def __f(self, params):
        X_train, X_test, Y_train, Y_test = train_test_split(GaussianProcess.__X, GaussianProcess.__Y, test_size=0.2)
        classifier = GaussianProcess.__Classifier(**{dim.name: val for dim, val in zip(GaussianProcess.__HyperparameterSpace, params) if dim.name != 'dummy'})
        classifier.fit(X_train, Y_train)
        r_squared = classifier.score(X_test, Y_test)
        logging.info(f"GP__f score is {r_squared}")
        return 1/r_squared

    def RunGp(self, X, Y):
        logging.info("Running GP optimization")
        GaussianProcess.__X = X
        GaussianProcess.__Y = Y
        try:
            clf = gp_minimize(self.__f,
                                GaussianProcess.__HyperparameterSpace,
                                acq_func=GaussianProcess.__GaussianSettings['acq_func'],
                                n_calls=GaussianProcess.__GaussianSettings['n_calls'],
                                n_initial_points=GaussianProcess.__GaussianSettings['n_initial_points'],
                                noise=GaussianProcess.__GaussianSettings['noise'],
                                random_state=None,
                                n_jobs=-1)
            bestScore = clf.fun
            bestParameters = clf.x
            scoresPerRun = clf.func_vals
            return bestScore, bestParameters, scoresPerRun
        except Exception as e:
            logging.info("Error occurred while running GP optimization")
            raise e