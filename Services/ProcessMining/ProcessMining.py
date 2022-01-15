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

    def Save4DPlot(self):
        logging.info("Storing 4d plot")
        try:
            #import matplotlib.pyplot as plt
            import plotly.graph_objs as go

            #Get data
            fileManager = CsvFileManager(ProcessMining.__DbContext, ProcessMining.__Settings)
            df = fileManager.ReadFileToDataFrame(ProcessMining.__Settings.CsvStorageManager["MultiDimensionalHeuristicConformanceEvaluation"])
            X = df['dependency_threshold'].tolist()
            Y = df['and_threshold'].tolist()
            Z = df['loop_two_threshold'].tolist()
            c_avarageScore = df['AverageScore'].tolist()
            c_averageScoreWithoutSimplicty = df['AverageScoreIgnoringSimplicity'].tolist()

            averageScoreData = go.Scatter3d(x=X, y=Y, z=Z,
                                            marker=dict(color=c_avarageScore,
                                                        opacity=1,
                                                        reversescale=True,
                                                        colorscale='Blues',
                                                        size=2),
                                            line=dict(width=0.2),
                                            mode='markers',
                                            name="Average score")
            averageScoreWithoutSimplictyDate = go.Scattter3d(x=X, y=Y, z=Z,
                                                             marker=dict(color=c_averageScoreWithoutSimplicty,
                                                                         opacity=1,
                                                                         reversescale=True,
                                                                         colorscale='Reds',
                                                                         size=2),
                                                             line=dict(width=0.2),
                                                             mode='markers',
                                                             name="Aaverage score ignoring simplicity")

            #fig = go.Figure(data=[averageScoreData, averageScoreWithoutSimplictyDate])

            #fig.update_layout()

            layout = go.Layout(scene=dict(xaxis=dict(title="dependency threshold"),
                                          yaxis=dict(title="and threshold"),
                                          zaxis=dict(title="two loop threshold")),)

            plotly.offline.plot({"data": [averageScoreData, averageScoreWithoutSimplictyDate],
                                 "layout": layout},
                                 auto_open=False,
                                 filename=("4dplot.png"))

            #fig = plt.figure()
            #axis = fig.add_subplot(111, projection='3d')

            #axis.scatter(X, Y, Z, c=c_avarageScore, cmap=plt.hot(), marker="s", label="Average score")
            #axis.scatter(X, Y, Z, c=c_averageScoreWithoutSimplicty, cmap=plt.hot(), maker="o", label="Average score ignoring simplicity")

            #repsoitoryLocation = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../Domain/Repositories")
            #imagesSink = os.path.join(repsoitoryLocation, settings.ImageStorage["ImagesSinkProcessDiscovery"])
            #plt.savefig(os.path.join(imageSink, ProcessMining.__Settings.ImageStorage['4d_heuristicsPlot']))
        except Exception as e:
            logging.error("Error occurred when storing 4d plot", exc_info=True)

    def __4DThresholdHeuristicsMinerDiscovery(self):
        logging.info("Running multi-dimensional threshold values for heuristics discovery")
        try:
            thresholdValues = [1.0, 0.99, 0.97, 0.95, 0.92, 0.90, 0.85, 0.8, 0.75, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]
            for dependency_threshold in thresholdValues:
                for and_threshold in thresholdValues:
                    processDiscovery = ProcessDiscovery(ProcessMining.__Settings, ProcessMining.__EventLog, ProcessMining.__OnlyDone)
                    conformanceChecker = ConformanceChecking(ProcessMining.__Settings, ProcessMining.__DbContext)

                    for loop_two_threshold in thresholdValues:
                        net, initial, final = processDiscovery.PetriNetHeuristicsMiner(dependency_threshold, and_threshold, loop_two_threshold)
                        conformanceChecker.Add4DHeuristicsConformanceCheckToCollection('Heuristics miner', dependency_threshold, and_threshold, loop_two_threshold, ProcessMining.__EventLog, net, initial, final)
                        conformanceChecker.SaveConformanceCollection(ProcessMining.__OnlyDone, ProcessMining.__Settings.CsvStorageManager["MultiDimensionalHeuristicConformanceEvaluation"])

                    del conformanceChecker
                    del processDiscovery

            self.Save4DPlot()
        except Exception as e:
            logging.error("Error occurred when running multi-dimensional threshold conformance checks for heuristics discovery.", exc_info=True)

    def __RunProcessTreeInductiveDiscovery(self, processDiscovery : ProcessDiscovery):
        logging.info("Running inductive process tree discovery")
        try:
            thresholdValues = [0.0, 0.05, 0.1, 0.25, 0.5]
            for threshold in thresholdValues:
                processTree005 = processDiscovery.ProcessTreeInductive(noiseThreshold=threshold)
        except Exception as e:
            logging.error("Error occurred when running inductive process tree discovery", exc_info=True)

    def __RunInductiveMinerDiscoveryTests(self, processDiscovery : ProcessDiscovery, conformanceChecker : ConformanceChecking):
        logging.info("Running Inductive miner discovery")
        try:
            thresholdValues = [0.0, 0.01, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
            for threshold in thresholdValues:
                net, initial, final = processDiscovery.PetriNetInductiveMiner(threshold, ProcessMining.__Settings.ImageStorage['inductiveMiner'])
                conformanceChecker.AddToConfromanceCheckCollection('Inductive miner w threshold '+str(threshold), ProcessMining.__EventLog, net, initial, final)
        except Exception as e:
            logging.error("Error occurred while running inductive miner discovery.", exc_info=True)

    def __RunSingleThresholdHeuristicsMinerDiscovery(self, processDiscovery : ProcessDiscovery, conformanceChecker : ConformanceChecking):
        logging.info("Running single threshold heuristics miner discovery")
        try:
            thresholdValues = [1.0, 0.99, 0.97, 0.95, 0.92, 0.90, 0.85, 0.8, 0.75, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]
            for threshold in thresholdValues:
                net, initial, final = processDiscovery.PetriNetHeuristicsMiner(threshold, threshold, threshold)
                conformanceChecker.AddToConfromanceCheckCollection('Heuristics miner w threshold '+str(threshold), ProcessMining.__EventLog, net, initial, final)
        except Exception as e:
            logging.error("Error occurred while running single threshold heuristics discovery.", exc_info=True)

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
            self.__RunProcessTreeInductiveDiscovery(processDiscovery)

            #Discovery Miners
            #Alpha miners
            net, initial, final = processDiscovery.PetriNetAlphaMiner()
            conformanceChecker.AddToConfromanceCheckCollection('AlphaMiner', eventLog, net, initial, final)
            net, initial, final = processDiscovery.PetriNetAlphaPlusMiner()
            conformanceChecker.AddToConfromanceCheckCollection('AlphaPlusMiner', eventLog, net, initial, final)

            #Inductive miner
            self.__RunInductiveMinerDiscoveryTests(processDiscovery, conformanceChecker)

            #heuristics miner
            self.__RunSingleThresholdHeuristicsMinerDiscovery(processDiscovery, conformanceChecker)

            conformanceChecker.SaveConformanceCollection(ProcessMining.__OnlyDone, ProcessMining.__Settings.CsvStorageManager["MinerConformanceEvaluation"])
            del conformanceChecker
            del processDiscovery

            #multidimensional threshold heuristics miner
            self.__4DThresholdHeuristicsMinerDiscovery()

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
        #processEnhancement.AddTeamMemberTypeToDbFromCsv()
        #processEnhancement.CreateMLDataSet()