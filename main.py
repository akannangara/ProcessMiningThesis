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
    projectsList = jiraImporter.GetProjectsList()
    for project in projectsList:
        issues = jiraImporter.GetProjectIssues(project)
        jiraImporter.StoreIssuesToDatabase(issues)

def CreateEventLogsFromDb():
    fileManager = CsvFileManager(DbContext(settings), settings)
    fileManager.CreateEventLogFromDb(onlyDone=False)
    fileManager.CreateStatusCollectionFromDb()
    fileManager.CreateTeamMemberCollectionFromDb()

def RunProcessDiscoveryAndConformance():
    processMiner = ProcessMining(settings, DbContext(settings))
    processMiner.RunAllDiscoveryAlgorithms()

def RunGPHeuristicsDiscovery():
    processMiner = ProcessMining(settings, DbContext(settings))
    processMiner.RunGPHeuristicsDiscovery()
    Create4dGrpah()

def Create4dGrpah():
    processMiner = ProcessMining(settings, DbContext(settings))
    processMiner.SaveSurfaceMultiDMap(ignoreSimplicity=True)
    
def RunProcessConformanceWithDesiredWorkflowAndModelEnhancement():
    processMiner = ProcessMining(settings, DbContext(settings))
    _, tokenBasedReplayConformance = processMiner.ConformanceCheckWithDesiredWorkflow()
    processMiner.ModelEnhancement(tokenBasedReplayConformance)

def RunPredictiveTechniques():
    processEnhancement = ProcessEnhancement(settings, DbContext(settings))
    processEnhancement.CreateMLDataSet()
    pt = PredictiveTechniques(settings, DbContext(settings))
    pt.RunWorkRatioEstimation()
    pt.RunFitnessEstimation()

if __name__ == "__main__":
    if settings.Debug:
        logging.basicConfig(format='%(asctime)s %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    else:
        logging.basicConfig(filename='app.log', filemode='w', format='%(asctime)s %(name)s - \
                                            %(levelname)s - %(message)s', level=logging.INFO)
    startTime = time.time()
    print(DbContext(settings).Query(TIssue, "", "")[0].Fitness)
    #ImportJiraIssues()
    #CreateEventLogsFromDb()
    #RunProcessDiscoveryAndConformance()
    #RunGPHeuristicsDiscovery()
    #Create4dGrpah()
    #RunProcessConformanceWithDesiredWorkflowAndModelEnhancement()
    RunPredictiveTechniques()
    logging.info("Execution time was "+str(time.time()-startTime)+" s")