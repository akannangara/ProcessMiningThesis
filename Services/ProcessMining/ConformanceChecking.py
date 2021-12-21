import logging
import os
import pandas as pd
from pydantic import BaseModel

import pm4py as pm4py

#Create petri net
from pm4py.objects.petri_net.obj import PetriNet, Marking
from pm4py.objects.petri_net.utils import petri_utils

#visualize petrinet
from pm4py.visualization.petri_net import visualizer as pn_visualizer

class ConformanceChecking(BaseModel):
    __Settings = None
    __ImagesSink = None


    def __init__(self, settings):
        ConformanceChecking.__Settings = settings
        repsoitoryLocation = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../Domain/Repositories")
        ConformanceChecking.__ImagesSink = os.path.join(repsoitoryLocation, settings.ImageStorage["ImagesSinkProcessConformance"])

    def ConformanceCheckDiagnosticsAlignment(self, log, petrinet, initial, final):
        return pm4py.conformance_diagnostics_alignments(log, petrinet, initial, final)

    def FitnessAlignment(self, log, model, initial, final):
        return pm4py.fitness_alignments(log, model, initial, final)

    def FitnessTokenBasedReply(self, log, model, inital, final):
        return pm4py.fitness_token_based_replay(log, model, inital, final)

    def PrecisionAlignment(self, log, model, initial, final):
        return pm4py.precision_alignments(log, model, initial, final)

    def PrecisionTokenBasedReplay(self, log, model, initial, final):
        return pm4py.precision_token_based_replay(log, model, initial, final)

    def Generalization(self, log, model, initial, final):
        return pm4py.algo.evaluation.generalization.algorithm.apply(log, model, initial, final)

    def Simplicity(self, model):
        return pm4py.algo.evaluation.simplicity.algorithm.apply(model)