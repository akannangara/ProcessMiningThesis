import logging
import os
import pandas as pd
from pydantic import BaseModel
from typing import List

import datetime

import pm4py as pm4py

#Create petri net
from pm4py.objects.petri_net.obj import PetriNet, Marking
from pm4py.objects.petri_net.utils import petri_utils

#visualize petrinet
from pm4py.visualization.petri_net import visualizer as pn_visualizer

from ProcessMinerConformance import ProcessMinerConformance
from CsvFileManager import CsvFileManager
from DbContext import DbContext
from EventLogItem import EventLogItem
from TStatus import TStatus
from TChangeLog import TChangeLog

from ProcessDiscovery import ProcessDiscovery

class ConformanceChecking(BaseModel):
    __Settings = None
    __ImagesSink = None
    __ConformanceCheckCollection = None
    __DbContext = None

    def __init__(self, settings, dbContext : DbContext):
        ConformanceChecking.__Settings = settings
        ConformanceChecking.__DbContext = dbContext
        repsoitoryLocation = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../Domain/Repositories")
        ConformanceChecking.__ImagesSink = os.path.join(repsoitoryLocation, settings.ImageStorage["ImagesSinkProcessConformance"])
        ConformanceChecking.__ConformanceCheckCollection = []

    def ConformanceCheckDiagnosticsAlignment(self, log, petrinet, initial, final):
        return pm4py.conformance_diagnostics_alignments(log, petrinet, initial, final)

    def ConformanceCheckDiagnosticsTokenBasedReplay(self, log, petrinet, initial, final):
        return pm4py.conformance_diagnostics_token_based_replay(log, petrinet, initial, final)

    def FitnessAlignment(self, log, model, initial, final):
        return pm4py.fitness_alignments(log, model, initial, final)

    def FitnessTokenBasedReply(self, log, model, inital, final):
        return pm4py.fitness_token_based_replay(log, model, inital, final)

    def PrecisionAlignment(self, log, model, initial, final):
        return pm4py.precision_alignments(log, model, initial, final)

    def PrecisionTokenBasedReplay(self, log, model, initial, final):
        return pm4py.precision_token_based_replay(log, model, initial, final)

    def Generalization(self, log, model, initial, final):
        return pm4py.algo.evaluation.generalization.algorithm.apply(log, model, initial, final)

    def Simplicity(self, model):
        return pm4py.algo.evaluation.simplicity.algorithm.apply(model)

    def AddToConfromanceCheckCollection(self, minerName, eventLog, petrinet, initial, final):
        logging.info(f"Adding {minerName} conformance summary to conformance check collection")
        try:
            fitness = self.FitnessTokenBasedReply(eventLog, petrinet, initial, final)
            precision = self.PrecisionTokenBasedReplay(eventLog, petrinet, initial, final)
            generalization = self.Generalization(eventLog, petrinet, initial, final)
            simplicity = self.Simplicity(petrinet)
            conformance = ProcessMinerConformance(minerName, fitness, precision, generalization, simplicity)
            ConformanceChecking.__ConformanceCheckCollection.append(conformance)
        except Exception as e:
            logging.error(f"Error occurred when trying to add {minierName} data to conformance check collection")

    def SaveConformanceCollection(self, onlyDone):
        if not(ConformanceChecking.__ConformanceCheckCollection):
            logging.error("Conformance check collection is empty")
            return
        logging.info("Storing conformance collection as csv")
        try:
            fileManager = CsvFileManager(ConformanceChecking.__DbContext, ConformanceChecking.__Settings)
            fileName = ConformanceChecking.__Settings.CsvStorageManager["MinerConformanceEvaluation"]
            if onlyDone:
                fileName = "OnlyDone_"+fileName
            fileManager.StoreMinerConformanceEvaluation(ConformanceChecking.__ConformanceCheckCollection, fileName)
        except Exception as e:
            logging.error("Error occurred when storing confromance collection as csv", exc_info=True)

    def CreateDesiredEventLog(self, inputFile : str, sheetName : str):
        logging.info("Creating desired eventlog")
        try:
            desiredWorkflowEventLog = self.__ReadDesiredWorkflowResponseExcelToEventCollection(inputFile, sheetName)
            fileManager = CsvFileManager(ConformanceChecking.__DbContext, ConformanceChecking.__Settings)
            fileManager.CreateFileFromEntityCollection(desiredWorkflowEventLog, EventLogItem, ConformanceChecking.__Settings.CsvStorageManager["DesiredEventLogFileName"])
        except Exception as e:
            logging.error("Error occurred when creating desired eventlog", exc_info=True)

    def __ReadDesiredWorkflowResponseExcelToEventCollection(self, inputFile : str, sheetName : str) -> List[EventLogItem]:
        eventCollection = []
        dataframe = pd.read_excel(os.path.abspath(inputFile), sheet_name=sheetName, engine='openpyxl', header=0)
        desiredWorkflowColumnNamePrefix = "Desired workflow "
        desiredWorkflowColumnNameSuffix = " (for example \"To Do; In Progress; In Review; Done\")"
        maxWorkflowColumns = 15
        teamFunctionColumnName = "Team function (not required)"
        x = 0
        for _ , row in dataframe.iterrows():
            teamMember = row[teamFunctionColumnName]
            for i in range (1, maxWorkflowColumns):
                x+=1
                columnName = desiredWorkflowColumnNamePrefix+str(i)+desiredWorkflowColumnNameSuffix
                if row[columnName] != row[columnName]:
                    break
                eventCollection.extend(self.__CreateEventLogFromWorkflow(row[columnName], teamMember, x))
        return eventCollection

    def __CreateEventLogFromWorkflow(self, workflow : str, teamMember : str, id : int):
        fieldValue = "Jira"
        fieldType = ""
        issueKey = "CONF_DESIRED"+str(id)
        caseEventLog = self.__ParseEventWorkflow(workflow, id)
        initialDateTime = datetime.datetime(2021,12,5)
        eventCollectionForWorkflow = []
        for i in range(1, len(caseEventLog)):
            timestamp = initialDateTime + datetime.timedelta(days=i)
            fromStatus = caseEventLog[i-1]
            toStatus = caseEventLog[i]
            event = EventLogItem(id, issueKey, teamMember, timestamp, fromStatus, toStatus, fieldValue, fieldType)
            eventCollectionForWorkflow.append(event)
        return eventCollectionForWorkflow

    def __ParseEventWorkflow(self, workflowInput : str, id : int) -> List[str]:
        acceptedStatuses = self.__GetStatusNames()
        acceptedStatuses.extend(["In Test", "Pre-refinement", "Refinement", "Ready to Deploy"])
        workflow = ["Create Card"]
        workflowInputElements = workflowInput.split(";")
        for element in workflowInputElements:
            if not element:
                break
            element = element.rstrip()
            element = element.lstrip()
            elementStatus = ""
            if element.casefold() in (status.casefold() for status in acceptedStatuses):
                for status in acceptedStatuses:
                    if element.casefold() == status.casefold():
                        workflow.append(status)
                        break
            else:
                logging.error(f"Failed to identify worflow element {element} in workflow id {id}")
        return workflow

    def __GetStatusNames(self) -> List[str]:
        statusCollection = []
        dbContext = ConformanceChecking.__DbContext
        for status in dbContext.Query(TStatus, "", ""):
            statusCollection.append(status.Name)
        return statusCollection
