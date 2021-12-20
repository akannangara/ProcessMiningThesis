import logging
import os
import pandas as pd
from pydantic import BaseModel

import pm4py as pm4py

class ModelEvaluator(BaseModel):

    def FitnessAlignment(log, model, initial, final):
        return pm4py.fitness_alignments(log, model, initial, final)

    def FitnessTokenBasedReply(log, model, inital, final):
        return pm4py.fitness_token_based_replay(log, model, inital, final)

    def PrecisionAlignment(log, model, initial, final):
        return pm4py.precision_alignments(log, model, inital, final)

    def PrecisionTokenBasedReplay(log, model, initial, final):
        return pm4py.precision_token_based_replay(log, model, inital, final)

    def Generalization(log, model, initial, final):
        return pm4py.algo.evaluation.generalization.algorithm.apply(log, model, inital, final)

    def Simplicity(model):
        return pm4py.algo.evaluation.simplicity.algorithm.apply(model)