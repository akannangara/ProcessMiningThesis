import sys
import os
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

COMMON_DIR = os.path.join(ROOT_DIR, 'Common')
COMMON_SUPPORT_DIR = os.path.join(COMMON_DIR, 'Support')
sys.path.append(COMMON_DIR)
sys.path.append(COMMON_SUPPORT_DIR)

DOMAIN_DIR = os.path.join(ROOT_DIR, 'Domain')
DOMAIN_MODELS_JIRAMODELS_DIR = os.path.join(DOMAIN_DIR, 'Models/JiraModels')
DOMAIN_MODELS_DBMODELS_DIR = os.path.join(DOMAIN_DIR, 'Models/DbModels')
DOMAIN_MODELS_CSVMODELS = os.path.join(DOMAIN_DIR, 'Models/CsvModels')
DOMAIN_REPOSITORIES_DIR = os.path.join(DOMAIN_DIR, 'Repositories')
sys.path.append(DOMAIN_DIR)
sys.path.append(DOMAIN_MODELS_JIRAMODELS_DIR)
sys.path.append(DOMAIN_MODELS_DBMODELS_DIR)
sys.path.append(DOMAIN_MODELS_CSVMODELS)
sys.path.append(DOMAIN_REPOSITORIES_DIR)

SERVICES_DIR = os.path.join(ROOT_DIR, 'Services')
SERVICES_JIRADATACOLLECTOR_DIR = os.path.join(SERVICES_DIR, 'JiraDataCollector')
SERVICES_CSVFILEMANAGER_DIR = os.path.join(SERVICES_DIR, 'CsvFileManager')
SERVICES_PROCESSMINING_DIR = os.path.join(SERVICES_DIR, 'ProcessMining')
sys.path.append(SERVICES_DIR)
sys.path.append(SERVICES_JIRADATACOLLECTOR_DIR)
sys.path.append(SERVICES_CSVFILEMANAGER_DIR)
sys.path.append(SERVICES_PROCESSMINING_DIR)

import time
import logging

import ProgramSettings as settings

from Support.JiraConnectionModel import JiraConnectionModel
from JiraDataCollector.JiraDataImporter import JiraDataImporter

from DbContext import DbContext
from CsvFileManager import CsvFileManager
from ProcessMining import ProcessMining

from TIssue import TIssue


if __name__ == "__main__":
    if settings.Debug:
        logging.basicConfig(format='%(asctime)s %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    else:
        logging.basicConfig(filename='app.log', filemode='w', format='%(asctime)s %(name)s - \
                                            %(levelname)s - %(message)s', level=logging.INFO)
    try:
        dbContext = DbContext(settings)
    except Exception as e:
        logging.error("Could not create db context")
        exit(1)
    startTime = time.time()
    #jiraImporter = JiraDataImporter(settings, dbContext)
    #projectsList = jiraImporter.GetProjectsList()
    #for project in ["CONBR", "PSH"]:
    #    issues = jiraImporter.GetProjectIssues(project)
    #    jiraImporter.StoreIssuesToDatabase(issues)
    #fileManager = CsvFileManager(dbContext, settings)
    #fileManager.CreateEventLogFromDb(onlyDone=True)
    #fileManager.CreateTeamMemberCollectionFromDb()
    processMiner = ProcessMining(settings, onlyDone=True)
    #processMiner.RunAllDiscoveryAlgorithms()
    processMiner.ConformanceChecking()
    #alphaResults = processDiscovery.PetriNetAlphaMiner(save=True)
    logging.info("Execution time was "+str(time.time()-startTime)+" s")