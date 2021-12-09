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
sys.path.append(SERVICES_DIR)
sys.path.append(SERVICES_JIRADATACOLLECTOR_DIR)
sys.path.append(SERVICES_CSVFILEMANAGER_DIR)

import time
import logging

import ProgramSettings as settings

from Support.JiraConnectionModel import JiraConnectionModel
from JiraDataCollector.JiraDataImporter import JiraDataImporter

from DbContext import DbContext
from CsvFileManager import CsvFileManager

from TIssue import TIssue


if __name__ == "__main__":
    logging.basicConfig(filename='app.log', filemode='w', format='%(asctime)s %(name)s - \
                                            %(levelname)s - %(message)s', level=logging.INFO)
    try:
        dbContext = DbContext(settings)
    except Exception as e:
        logging.error("Could not create db context")
        exit(1)
    startTime = time.time()
    jiraImporter = JiraDataImporter(settings, dbContext)
    projectsList = jiraImporter.GetProjectsList()
    for project in projectsList:
        issues = jiraImporter.GetProjectIssues(project)
        jiraImporter.StoreIssuesToDatabase(issues)
    #queryResult = dbContext.Query(TIssue, 'Key', 'CONBR-121')
    #queryresult2 = dbContext.GetAllIssues(['CONBR'])
    fileManager = CsvFileManager(dbContext, settings)
    fileManager.CreateEventLogFromDb([])
    logging.info("Execution time was "+str(time.time()-startTime))