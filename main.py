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
from TChangeLog import TChangeLog

def ImportJiraIssues():
    jiraImporter = JiraDataImporter(settings, DbContext(settings))
    projectsList = jiraImporter.GetProjectsList()
    for project in projectsList:
        issues = jiraImporter.GetProjectIssues(project)
        jiraImporter.StoreIssuesToDatabase(issues)

def ImportJiraSprints():
    db = DbContext(settings)
    jiraImporter = JiraDataImporter(settings, db)
    sprints = jiraImporter.GetSprints()
    jiraImporter.StoreSprintsToDatabase(sprints)
    jiraImporter.EnhanceSprintData()

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

def MakeDataset():
    ImportJiraSprints()
    pe = ProcessEnhancement(settings, DbContext(settings))
    pe.CreateMLDataSet()

def RunPredictiveTechniquesWR():
    pt = PredictiveTechniques(settings, DbContext(settings))
    pt.RunWorkRatioEstimation()
    del pt

def RunPredictiveTechniquesFitness():
    pt = PredictiveTechniques(settings, DbContext(settings))
    pt.RunFitnessEstimation()
    del pt

if __name__ == "__main__":
    if settings.Debug:
        logging.basicConfig(format='%(asctime)s %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    else:
        logging.basicConfig(filename='app.log', filemode='w', format='%(asctime)s %(name)s - \
                                            %(levelname)s - %(message)s', level=logging.INFO)
    startTime = time.time()
    #ImportJiraIssues()
    ImportJiraSprints()
    MakeDataset()
    #CreateEventLogsFromDb()
    #RunProcessDiscoveryAndConformance()
    #RunGPHeuristicsDiscovery()
    #Create4dGrpah()
    #RunProcessConformanceWithDesiredWorkflowAndModelEnhancement()
    RunPredictiveTechniquesWR()
    RunPredictiveTechniquesFitness()
    logging.info("Execution time was "+str(time.time()-startTime)+" s")