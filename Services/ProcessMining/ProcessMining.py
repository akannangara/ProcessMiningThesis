import logging
import os
import pandas as pd
from pydantic import BaseModel
from typing import List, Dict

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
from ProcessEnhancement import ProcessEnhancement
from DbContext import DbContext

class ProcessMining(BaseModel):
    __Settings = None
    __EventLog = None
    __ConformantEventLogLocation = None
    __OnlyDone = False
    __DbContext = None

    def __init__(self, settings, dbContext : DbContext, onlyDone=False):
        ProcessMining.__Settings = settings
        csvRepository = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../Domain/Repositories/CsvCollection")
        if settings.Debug:
            self.__AddGraphVizLocation(settings)
        ProcessMining.__DbContext = dbContext
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
            conformanceChecker = ConformanceChecking(ProcessMining.__Settings, ProcessMining.__DbContext)

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
            conformanceChecker.AddToConfromanceCheckCollection('AlphaMiner', eventLog, net, initial, final)
            net, initial, final = processDiscovery.PetriNetAlphaPlusMiner()
            conformanceChecker.AddToConfromanceCheckCollection('AlphaPlusMiner', eventLog, net, initial, final)

            net, initial, final = processDiscovery.PetriNetInductiveMiner(0.0, ProcessMining.__Settings.ImageStorage['inductiveMiner'])
            conformanceChecker.AddToConfromanceCheckCollection('Inductive0.0Miner', eventLog, net, initial, final)

            net, initial, final = processDiscovery.PetriNetHeuristicsMiner()
            conformanceChecker.AddToConfromanceCheckCollection('Heuristics0.99Miner', eventLog, net, initial, final)
            net, initial, final = processDiscovery.PetriNetHeuristicsMiner(threshold=0.95)
            conformanceChecker.AddToConfromanceCheckCollection('Heuristics0.95Miner', eventLog, net, initial, final)
            net, initial, final = processDiscovery.PetriNetHeuristicsMiner(threshold=0.90)
            conformanceChecker.AddToConfromanceCheckCollection('Heuristics0.90Miner', eventLog, net, initial, final)
            net, initial, final = processDiscovery.PetriNetHeuristicsMiner(threshold=0.85)
            conformanceChecker.AddToConfromanceCheckCollection('Heuristics0.85Miner', eventLog, net, initial, final)
            net, initial, final = processDiscovery.PetriNetHeuristicsMiner(threshold=0.75)
            conformanceChecker.AddToConfromanceCheckCollection('Heuristics0.75Miner', eventLog, net, initial, final)
            net, initial, final = processDiscovery.PetriNetHeuristicsMiner(threshold=0.60)
            conformanceChecker.AddToConfromanceCheckCollection('Heuristics0.60Miner', eventLog, net, initial, final)
            net, initial, final = processDiscovery.PetriNetHeuristicsMiner(threshold=0.50)
            conformanceChecker.AddToConfromanceCheckCollection('Heuristics0.50Miner', eventLog, net, initial, final)
            net, initial, final = processDiscovery.PetriNetHeuristicsMiner(threshold=1.00)
            conformanceChecker.AddToConfromanceCheckCollection('Heuristics1.00Miner', eventLog, net, initial, final)

            conformanceChecker.SaveConformanceCollection(ProcessMining.__OnlyDone)
        except Exception as e:
            logging.error("Exception occurred when running all discovery algorithms", exc_info=True)

    def ConformanceCheckWithDesiredWorkflow(self) -> (Dict[str, float], List):
        logging.info("Running conformance check compared to desired workflow")
        conformanceChecker = ConformanceChecking(ProcessMining.__Settings, ProcessMining.__DbContext)
        #conformanceChecker.CreateDesiredEventLog("C:/Users/akann/Downloads/FormResponse.xlsx", 'workbook1')
        csvRepository = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../Domain/Repositories/CsvCollection")
        csvLocation = os.path.join(csvRepository, ProcessMining.__Settings.CsvStorageManager["DesiredEventLogFileName"])
        desiredEventLog = self.__ReadCsvEventLogAsEventLog(csvLocation)

        processDiscovery = ProcessDiscovery(ProcessMining.__Settings, desiredEventLog, ProcessMining.__OnlyDone)
        net, initial, final = processDiscovery.PetriNetInductiveMiner(0.0, ProcessMining.__Settings.ImageStorage['desiredInductiveMiner'])

        desiredEventLogTokenBasedReplayConformanceCheck = conformanceChecker.ConformanceCheckDiagnosticsTokenBasedReplay(ProcessMining.__EventLog, net, initial, final)

        fitness = conformanceChecker.FitnessTokenBasedReply(ProcessMining.__EventLog, net, initial, final)
        precision = conformanceChecker.PrecisionTokenBasedReplay(ProcessMining.__EventLog, net, initial, final)
        generalization = conformanceChecker.Generalization(ProcessMining.__EventLog, net, initial, final)
        simplicity = conformanceChecker.Simplicity(net)
        logging.info(f"Conformance of desired workflow f{fitness}, p{precision}, g{generalization}, s{simplicity}.")
        conformanceDictionary = {
            "Fitness_average": fitness['average_trace_fitness'],
            "Fitness_percentageFittingTraces": fitness['perc_fit_traces'],
            "Fintess_logFitness": fitness['log_fitness'],
            "Precision": precision,
            "Generalization": generalization,
            "Simplicity": simplicity
        }
        return conformanceDictionary, desiredEventLogTokenBasedReplayConformanceCheck

    def ModelEnhancement(self, eventLogTokenBasedReplayConfromance):
        processEnhancement = ProcessEnhancement(ProcessMining.__Settings, ProcessMining.__DbContext)
        processEnhancement.AddFitnessToIssues(eventLogTokenBasedReplayConfromance, ProcessMining.__EventLog)
        processEnhancement.AddTeamMemberTypToDbFromCsv()