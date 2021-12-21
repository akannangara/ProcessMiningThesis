import logging
import os
import pandas as pd
from pydantic import BaseModel
from typing import List

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

from CsvFileManager import CsvFileManager

from ProcessDiscovery import ProcessDiscovery
from ConformanceChecking import ConformanceChecking
from ProcessMinerConformance import ProcessMinerConformance
from DbContext import DbContext

class ProcessMining(BaseModel):
    __Settings = None
    __EventLog = None
    __ConformantEventLogLocation = None
    __OnlyDone = False
    __DbContext = None

    def __init__(self, settings, dbContext : DbContext, onlyDone=False):
        ProcessMining.__Settings = settings
        ProcessMining.__DbContext = dbContext
        csvRepository = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../Domain/Repositories/CsvCollection")
        if settings.Debug:
            self.__AddGraphVizLocation(settings)
        ProcessMining.__OnlyDone = onlyDone
        if onlyDone:
            csvLocation = os.path.join(csvRepository, ProcessMining.__Settings.CsvStorageManager["OnlyDoneEventLogFileName"])
        else:
            csvLocation = os.path.join(csvRepository, ProcessMining.__Settings.CsvStorageManager["EventLogFileName"])
        ProcessMining.__EventLog = self.__ReadCsvEventLogAsEventLog(csvLocation)
        ProcessMining.__ConformantEventLogLocation = os.path.join(csvRepository, "ConformantEventLog.csv")

    def __ReadCsvEventLogAsEventLog(self, csvLocation):
        log = pd.read_csv(csvLocation, sep=';')
        log.rename(columns={'IssueId' : 'case:clientId',
                            'To':'concept:name',
                            'IssueKey':'case:concept:name',
                            'TimeStamp':'time:timestamp'}, inplace=True)
        log = dataframe_utils.convert_timestamp_columns_in_df(log)
        return log_converter.apply(log)

    def __AddGraphVizLocation(self, settings):
        os.environ["PATH"] += os.pathsep + settings.GraphViz["binLocation"]
        os.environ["PATH"] += os.pathsep + settings.GraphViz["exeLocation"]

    def GetEventLog(self):
        return ProcessMining.__EventLog

    def RunAllDiscoveryAlgorithms(self):
        logging.info("Running all discovery algorithms")
        try:
            eventLog = ProcessMining.__EventLog
            processDiscovery = ProcessDiscovery(ProcessMining.__Settings, eventLog, ProcessMining.__OnlyDone)
            conformanceCollection = []

            #dfg, egf and fps
            dfg = processDiscovery.DFG()
            efg = processDiscovery.EFG()
            fps = processDiscovery.FPS()

            #processTrees
            processTree = processDiscovery.ProcessTreeInductive()
            processTree005 = processDiscovery.ProcessTreeInductive(noiseThreshold=0.05)
            processTree010 = processDiscovery.ProcessTreeInductive(noiseThreshold=0.1)
            processTree025 = processDiscovery.ProcessTreeInductive(noiseThreshold=0.25)
            processTree025 = processDiscovery.ProcessTreeInductive(noiseThreshold=0.5)

            #Discovery Miners
            net, initial, final = processDiscovery.PetriNetAlphaMiner()
            conformanceCollection.append(self.__EventLogModelConformance('AlphaMiner', eventLog, net, initial, final))
            net, initial, final = processDiscovery.PetriNetAlphaPlusMiner()
            conformanceCollection.append(self.__EventLogModelConformance('AlphaPlusMiner', eventLog, net, initial, final))

            net, initial, final = processDiscovery.PetriNetInductiveMiner()
            conformanceCollection.append(self.__EventLogModelConformance('InductiveMiner', eventLog, net, initial, final))

            net, initial, final = processDiscovery.PetriNetHeuristicsMiner()
            conformanceCollection.append(self.__EventLogModelConformance('Heuristics0.99Miner', eventLog, net, initial, final))
            net, initial, final = processDiscovery.PetriNetHeuristicsMiner(threshold=0.95)
            conformanceCollection.append(self.__EventLogModelConformance('Heuristics0.95Miner', eventLog, net, initial, final))
            net, initial, final = processDiscovery.PetriNetHeuristicsMiner(threshold=0.90)
            conformanceCollection.append(self.__EventLogModelConformance('Heuristics0.90Miner', eventLog, net, initial, final))
            net, initial, final = processDiscovery.PetriNetHeuristicsMiner(threshold=0.85)
            conformanceCollection.append(self.__EventLogModelConformance('Heuristics0.85Miner', eventLog, net, initial, final))
            net, initial, final = processDiscovery.PetriNetHeuristicsMiner(threshold=0.75)
            conformanceCollection.append(self.__EventLogModelConformance('Heuristics0.75Miner', eventLog, net, initial, final))
            net, initial, final = processDiscovery.PetriNetHeuristicsMiner(threshold=0.60)
            conformanceCollection.append(self.__EventLogModelConformance('Heuristics0.60Miner', eventLog, net, initial, final))
            net, initial, final = processDiscovery.PetriNetHeuristicsMiner(threshold=0.50)
            conformanceCollection.append(self.__EventLogModelConformance('Heuristics0.50Miner', eventLog, net, initial, final))
            net, initial, final = processDiscovery.PetriNetHeuristicsMiner(threshold=1.00)
            conformanceCollection.append(self.__EventLogModelConformance('Heuristics1.00Miner', eventLog, net, initial, final))

            self.__SaveConformanceCollection(conformanceCollection)
        except Exception as e:
            logging.error("Exception occurred when running all discovery algorithms", exc_info=True)

    def __EventLogModelConformance(self, minerName, eventLog, petrinet, initial, final):
        conformanceChecker = ConformanceChecking(ProcessMining.__Settings)
        fitness = conformanceChecker.FitnessAlignment(eventLog, petrinet, initial, final)
        precision = conformanceChecker.PrecisionAlignment(eventLog, petrinet, initial, final)
        gerneralization = conformanceChecker.Generalization(eventLog, petrinet, initial, final)
        simplicity = conformanceChecker.Simplicity(petrinet)
        conformance = ProcessMinerConformance(minerName, fitness, precision, gerneralization, simplicity)
        return conformance

    def __SaveConformanceCollection(self, conformanceCollection : List[ProcessMinerConformance]):
        fileManager = CsvFileManager(ProcessMining.__DbContext, ProcessMining.__Settings)
        fileName = ProcessMining.__Settings.CsvStorageManager["MinerConformanceEvaluation"]
        if ProcessMining.__OnlyDone:
            fileName = "OnlyDone_"+fileName
        fileManager.StoreMinerConformanceEvaluation(conformanceCollection, fileName)