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