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
from PredictiveTechniques import PredictiveTechniques
from DbContext import DbContext

from skopt import gp_minimize
from skopt.space import Integer, Categorical, Real
import numpy as np

class ProcessMining(BaseModel):
    __Settings = None
    __EventLog = None
    __ConformantEventLogLocation = None
    __OnlyDone = False
    __DbContext = None
    __HeuristicsHyperParameters = [Real(0.0,1.0, name='dependency_threshold'),
                                   Real(0.0,1.0, name='and_threshold'),
                                   Real(0.0,1.0, name='loop_two_threshold'),
                                   Categorical([False], name='save')]

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

    def SaveSurfaceMultiDMap(self, ignoreSimplicity : bool = False):
        logging.info("Storing multi d surface graph")
        try:
            from mpl_toolkits.mplot3d import Axes3D
            import matplotlib.pyplot as plt
            from matplotlib import cm
            from matplotlib.ticker import LinearLocator, FormatStrFormatter
            import numpy as np

            repsoitoryLocation = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../Domain/Repositories")
            imagesSink = os.path.join(repsoitoryLocation,  ProcessMining.__Settings.ImageStorage["ImagesSinkProcessDiscovery"])

            #Get data
            fileManager = CsvFileManager(ProcessMining.__DbContext, ProcessMining.__Settings)
            df = fileManager.ReadFileToDataFrame(ProcessMining.__Settings.CsvStorageManager["MultiDimensionalHeuristicConformanceEvaluation"])
            
            #TODO finish statistical test using r value
            columnsToDrop = ['df_index', 'MinerName', 'AverageFitness','PercentageOfFittingTraces','LogFitness','Precision','Generalization','Simplicity','AverageScore', 'AverageScoreIgnoringSimplicity']
            x_train = df.drop(columnsToDrop, axis='columns')
            x_train = x_train *10000
            y_train = df['AverageScoreIgnoringSimplicity'].copy()
            for i in range(len(y_train)):
                y_train[i] = y_train[i]*100000
            y_train = y_train.astype(int)
            from sklearn.feature_selection import chi2
            q=chi2(x_train,y_train)


            X = df['dependency_threshold'].tolist()
            Y = df['and_threshold'].tolist()
            C = np.array(df['loop_two_threshold'].tolist())
            if ignoreSimplicity:
                Z = np.array(df['AverageScore'].tolist())
            else:
                Z = np.array(df['AverageScoreIgnoringSimplicity'].tolist())
            scamap = plt.cm.ScalarMappable(cmap='inferno')
            
            plt.figure(figsize=(48,36), dpi=160)
            fig, axis = plt.subplots(subplot_kw={'projection': '3d'})
            fcolors = scamap.to_rgba(C)
            axis.plot_trisurf(X, Y, Z, facecolors=fcolors, cmap='inferno')
            axis.set_xlabel('Dependency threshold')
            axis.set_ylabel("And threshold")
            axis.set_zlabel("Quality Score")
            axis.set_title("Heuristics miner average quality score for varrying thresholds")
            axis.view_init(30,210)
            cbar = fig.colorbar(scamap)
            cbar.set_label("Loop two threshold")
            filePrefix = "matplotsurfaceAverage"
            if ignoreSimplicity:
                filePrefix = "IgnoreSimplicity"+filePrefix
            plt.savefig(os.path.join(imagesSink, filePrefix+ProcessMining.__Settings.ImageStorage['4d_heuristicsPlot']))
        except Exception as e:
            logging.error("Error occurred storing multi d surface graphs", exc_info=True)

    def Save4DPlotWithMatplotlib(self):
        logging.info("storing 4d plot with matplotlib")
        try:
            import matplotlib.pyplot as plt
            import seaborn as sns

            #Get data
            fileManager = CsvFileManager(ProcessMining.__DbContext, ProcessMining.__Settings)
            df = fileManager.ReadFileToDataFrame(ProcessMining.__Settings.CsvStorageManager["MultiDimensionalHeuristicConformanceEvaluation"])
            X = df['dependency_threshold'].tolist()
            Y = df['and_threshold'].tolist()
            Z = df['loop_two_threshold'].tolist()
            c_avarageScore = df['AverageScore'].tolist()
            c_averageScoreWithoutSimplicty = df['AverageScoreIgnoringSimplicity'].tolist()
            fig = plt.figure(figsize=(16,12), dpi=160)
            axis = fig.add_subplot(111, projection='3d')

            p = axis.scatter(X, Y, Z, c=c_avarageScore, cmap=plt.get_cmap("winter"), marker="x", label="Average score", s=10)
            axis.scatter(X, Y, Z, c=c_averageScoreWithoutSimplicty, cmap=plt.get_cmap("winter"), marker="v", label="Average score ignoring simplicity", s=10)

            axis.set_xlabel('Dependency threshold')
            axis.set_ylabel("And threshold")
            axis.set_zlabel("Loop two threshold")
            axis.set_title("3D scatter plot of varrying threshold values and quality average score ")

            axis.legend()
            axis.view_init(15,10)
            fig.colorbar(p, ax=axis)

            repsoitoryLocation = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../Domain/Repositories")
            imagesSink = os.path.join(repsoitoryLocation,  ProcessMining.__Settings.ImageStorage["ImagesSinkProcessDiscovery"])
            plt.savefig(os.path.join(imagesSink, "matplotlib"+ProcessMining.__Settings.ImageStorage['4d_heuristicsPlot']))
        except Exception as e:
            logging.error("Error occurred while making matplotlib 3d graph", exc_info=True)

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

            conformanceChecker.SaveConformanceCollection(ProcessMining.__OnlyDone, ProcessMining.__Settings.CsvStorageManager["MinerConformanceEvaluation"], deleteExistingFile=True)
            del conformanceChecker
            del processDiscovery

            #heuristics miner with varrying threshold values
            self.RunGPHeuristicsDiscovery()

        except Exception as e:
            logging.error("Exception occurred when running all discovery algorithms", exc_info=True)

    def __f(self, params):
        processDiscovery = ProcessDiscovery(ProcessMining.__Settings, ProcessMining.__EventLog, ProcessMining.__OnlyDone)
        conformanceChecker = ConformanceChecking(ProcessMining.__Settings, ProcessMining.__DbContext)
        net, initial, final = processDiscovery.PetriNetHeuristicsMiner(**{dim.name: val for dim, val in zip(ProcessMining.__HeuristicsHyperParameters, params) if dim.name != 'dummy'})
        score = conformanceChecker.Add4DHeuristicsConformanceCheckToCollection('Heuristics miner', params[0], params[1], params[2], ProcessMining.__EventLog, net, initial, final)
        conformanceChecker.SaveConformanceCollection(ProcessMining.__OnlyDone, ProcessMining.__Settings.CsvStorageManager["MultiDimensionalHeuristicConformanceEvaluation"], deleteExistingFile=False)
        logging.info(f"Ran heuristics miner gp and score is {score}")
        return 1/score

    def RunGPHeuristicsDiscovery(self):
        logging.info("Running GP heuristics discovery")
        try:
            fileManager = CsvFileManager(ProcessMining.__DbContext, ProcessMining.__Settings)
            fileName = ProcessMining.__Settings.CsvStorageManager["MultiDimensionalHeuristicConformanceEvaluation"]
            if ProcessMining.__OnlyDone:
                fileName = "OnlyDone_"+fileName
            fileManager.DeleteFileIfExists(fileName)
            del fileManager
            clf = gp_minimize(self.__f,
                              ProcessMining.__HeuristicsHyperParameters,
                              acq_func=ProcessMining.__Settings.GaussianProcess['acq_func'],
                              n_calls=ProcessMining.__Settings.GaussianProcess['n_calls'],
                              n_initial_points=ProcessMining.__Settings.GaussianProcess['n_initial_points'],
                              noise=ProcessMining.__Settings.GaussianProcess['noise'],
                              random_state=None,
                              n_jobs=-1)
        except Exception as e:
            logging.error(f"Error occurred while running GP optimization for heuristics discovery", exc_info=True)

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
        if eventLogTokenBasedReplayConfromance:
            processEnhancement.AddFitnessToIssues(eventLogTokenBasedReplayConfromance, ProcessMining.__EventLog)
        processEnhancement.AddTeamMemberTypeToDbFromCsv()
        processEnhancement.CreateMLDataSet()