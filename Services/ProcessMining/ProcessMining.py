import logging
import os
import pandas as pd
from pydantic import BaseModel

import pm4py as pm4py

#Dataframe conversions
from pm4py.objects.log.util import dataframe_utils
from pm4py.objects.conversion.log import converter as log_converter

#Process miners
from pm4py.algo.discovery.alpha import algorithm as alpha_miner
from pm4py.algo.discovery.inductive import algorithm as inductive_miner
from pm4py.algo.discovery.heuristics import algorithm as heuristics_miner

#directly follows graph
from pm4py.algo.discovery.dfg import algorithm as dfg_discovery

#visualization
from pm4py.visualization.petri_net import visualizer as pn_visualizer
from pm4py.visualization.dfg import visualizer as dfg_visualization
from pm4py.visualization.heuristics_net import visualizer as hn_visualizer
from pm4py.visualization.process_tree import visualizer as pt_visualizer
from pm4py.visualization.footprints import visualizer as fps_visualizer

#petrinets
from pm4py.objects.petri_net.obj import PetriNet, Marking

from ProcessDiscovery import ProcessDiscovery

class ProcessMining(BaseModel):
    __Settings = None
    __EventLog = ""

    def __init__(self, settings):
        ProcessMining.__Settings = settings
        csvRepository = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../Domain/Repositories/CsvCollection")
        ProcessMining.__EventLog = self.__ReadCsvEventLogAsEventLog(csvRepository)

    def __ReadCsvEventLogAsEventLog(self, csvRepositoryLocation):
        log = pd.read_csv(os.path.join(csvRepositoryLocation, ProcessMining.__Settings.CsvStorageManager["EventLogFileName"]))
        log.rename(columns={'IssueId' : 'case:clientId',
                            'To':'concept:name',
                            'IssueKey':'case:concept:name',
                            'TimeStamp':'time:timestamp'}, inplace=True)
        log = dataframe_utils.convert_timestamp_columns_in_df(log)
        return log_converter.apply(log)

    def GetEventLog(self):
        return ProcessMining.__EventLog

    def RunAllDiscoveryAlgorithms(self):
        processDiscovery = ProcessDiscovery(ProcessMining.__Settings, ProcessMining.__EventLog)
        alphaNet, alphaInitial, alphaFinal = processDiscovery.PetriNetAlphaMiner()
        processDiscovery.PetriNetAlphaPlusMiner()
        processDiscovery.PetriNetInductiveMiner()
        processDiscovery.PetriNetHeuristicsMiner()
        processDiscovery.PetriNetHeuristicsMiner(threshold=0.95)
        processDiscovery.PetriNetHeuristicsMiner(threshold=0.90)
        processDiscovery.PetriNetHeuristicsMiner(threshold=0.85)
        processDiscovery.PetriNetHeuristicsMiner(threshold=0.75)
        processDiscovery.PetriNetHeuristicsMiner(threshold=0.60)
        processDiscovery.PetriNetHeuristicsMiner(threshold=0.50)
        processDiscovery.PetriNetHeuristicsMiner(threshold=1.00)
