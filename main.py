import ImportAllLocations

import time
import logging

import ProgramSettings as settings

from Support.JiraConnectionModel import JiraConnectionModel
from JiraDataCollector.JiraDataImporter import JiraDataImporter

from DbContext import DbContext
from CsvFileManager import CsvFileManager
from ProcessMining import ProcessMining
from ProcessEnhancement import ProcessEnhancement
from PredictiveTechniques import PredictiveTechniques

from TIssue import TIssue

def ImportJiraIssues():
    jiraImporter = JiraDataImporter(settings, DbContext(settings))
    projectsList = ["CONBR"]#jiraImporter.GetProjectsList()
    for project in projectsList:
        issues = jiraImporter.GetProjectIssues(project)
        jiraImporter.StoreIssuesToDatabase(issues)

def CreateEventLogsFromDb():
    fileManager = CsvFileManager(DbContext(settings), settings)
    fileManager.CreateEventLogFromDb(onlyDone=False)
    fileManager.CreateEventLogFromDb(onlyDone=True)
    fileManager.CreateStatusCollectionFromDb()

def RunProcessDiscoveryAndConformance():
    processMiner = ProcessMining(settings, DbContext(settings))
    processMiner.RunAllDiscoveryAlgorithms()
    processMiner2 = ProcessMining(settings, DbContext(settings), onlyDone=True)
    processMiner2.RunAllDiscoveryAlgorithms()

def RunProcessConformanceWithDesiredWorkflowAndModelEnhancement():
    processMiner = ProcessMining(settings, DbContext(settings))
    _, tokenBasedReplayConformance = processMiner.ConformanceCheckWithDesiredWorkflow()
    processMiner.ModelEnhancement(tokenBasedReplayConformance)

def MakeMultiDPlot():
    processMiner = ProcessMining(settings, DbContext(settings))
    processMiner.Run4DHeuristicsDiscovery()
    #processMiner.Save4DPlot()
    processMiner.SaveSurfaceMultiDMap()

def RunPredictiveTechniques():
    processEnhancement = ProcessEnhancement(settings, DbContext(settings))
    processEnhancement.CreateMLDataSet()
    #pt = PredictiveTechniques(settings, DbContext(settings))
    #pt.RunWorkRatioEstimation()

if __name__ == "__main__":
    if settings.Debug:
        logging.basicConfig(format='%(asctime)s %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    else:
        logging.basicConfig(filename='app.log', filemode='w', format='%(asctime)s %(name)s - \
                                            %(levelname)s - %(message)s', level=logging.INFO)
    startTime = time.time()
    #ImportJiraIssues()
    #CreateEventLogsFromDb()
    #RunProcessDiscoveryAndConformance()
    #RunProcessConformanceWithDesiredWorkflowAndModelEnhancement()
    RunPredictiveTechniques()
    #MakeMultiDPlot()
    logging.info("Execution time was "+str(time.time()-startTime)+" s")