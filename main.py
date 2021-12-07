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
DOMAIN_REPOSITORIES_DIR = os.path.join(DOMAIN_DIR, 'Repositories')
sys.path.append(DOMAIN_DIR)
sys.path.append(DOMAIN_MODELS_JIRAMODELS_DIR)
sys.path.append(DOMAIN_MODELS_DBMODELS_DIR)
sys.path.append(DOMAIN_REPOSITORIES_DIR)

SERVICES_DIR = os.path.join(ROOT_DIR, 'Services')
sys.path.append(SERVICES_DIR)


import pdb
import logging

import ProgramSettings as settings

from Support.JiraConnectionModel import JiraConnectionModel
from JiraDataCollection.JiraImporter import JiraImporter

from DbContext import DbContext


if __name__ == "__main__":
    logging.basicConfig(filename='app.log', filemode='w', format='%(asctime)s %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    
    try:
        dbContext = DbContext(settings)
    except Exception as e:
        logging.error("Could not create db context")
        exit(1)
    jiraImporter = JiraImporter(settings, dbContext)
    jiraImporter.GetProjectsList()
    issue = jiraImporter.GetIssue('CONBR-121')
    x = jiraImporter.StoreIssuesToDb([issue])
    y = dbContext.GetIssue('CONBR-121')
    issue = jiraImporter.GetIssue('PSH-589')
    jiraImporter.StoreIssuesToDb([issue])
    z = 0