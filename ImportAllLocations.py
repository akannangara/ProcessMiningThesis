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
SERVICES_PROCESSMINING_DIR = os.path.join(SERVICES_DIR, 'ProcessMining')
sys.path.append(SERVICES_DIR)
sys.path.append(SERVICES_JIRADATACOLLECTOR_DIR)
sys.path.append(SERVICES_PROCESSMINING_DIR)