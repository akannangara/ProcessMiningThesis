import logging
import os
import pandas as pd
from pydantic import BaseModel

import pm4py as pm4py

class ModelEvaluator(BaseModel):
    __Settings = None

    def __init__(self, settings):
        ModelEvaluator.__Settings = settings

    def FitnessAlignment(self, log, model, initial, final):
        return pm4py.fitness_alignments(log, model, initial, final)

    def FitnessTokenBasedReply(self, log, model, inital, final):
        return pm4py.fitness_token_based_replay(log, model, inital, final)

    def PrecisionAlignment(self, log, model, initial, final):
        return pm4py.precision_alignments(log, model, inital, final)

    def PrecisionTokenBasedReplay(self, log, model, initial, final):
        return pm4py.precision_token_based_replay(log, model, inital, final)

    def Generalization(self, log, model, initial, final):
        return pm4py.algo.evaluation.generalization.algorithm.apply(log, model, inital, final)

    def Simplicity(self, model):
        return pm4py.algo.evaluation.simplicity.algorithm.apply(model)