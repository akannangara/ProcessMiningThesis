﻿import logging
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
    __Name = None

    def __init__(self, classifier, hyperparameterSpace : List, settings):
        GaussianProcess.__GaussianSettings = settings.GaussianProcess
        GaussianProcess.__Classifier = classifier
        GaussianProcess.__HyperparameterSpace = hyperparameterSpace

    def __f(self, params):
        X_Use, X_Unused, Y_Use, Y_Unused = train_test_split(GaussianProcess.__X, GaussianProcess.__Y, test_size=0.1)
        X_train, X_test, Y_train, Y_test = train_test_split(X_Use, Y_Use, test_size = 0.8)
        classifier = GaussianProcess.__Classifier(**{dim.name: val for dim, val in zip(GaussianProcess.__HyperparameterSpace, params) if dim.name != 'dummy'})
        classifier.fit(X_train.to_numpy(), Y_train.to_numpy())
        score = abs(Y_test - classifier.predict(X_test)).sum()
        logging.info(f"{GaussianProcess.__Name} GP__f score is {score}")
        return score

    def RunGp(self, X, Y, name : str):
        logging.info(f"Running GP optimization for {name}")
        GaussianProcess.__X = X
        GaussianProcess.__Y = Y
        GaussianProcess.__Name = name
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
            logging.info(f"Error occurred while running GP optimization { GaussianProcess.__Name}", exc_info=True)
            raise e