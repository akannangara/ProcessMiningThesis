import logging
import os
import pandas as pd
from pydantic import BaseModel
from typing import List, Dict

from DbContext import DbContext
from CsvFileManager import CsvFileManager

class ProcessEnhancement(BaseModel):
    __Settings = None
    __DbContext = None

    def __init__(self, settings, dbContext : DbContext):
        ProcessEnhancement.__Settings = settings
        ProcessEnhancement.__DbContext = dbContext

    def AddFitnessToIssues(self, issueFitnessCollection : List, eventLog : List):
        logging.info("Adding issue fitness to each issue in db")
        try:
            nrEvents = len(eventLog)
            dbContext = ProcessEnhancement.__DbContext
            for i in range(0, nrEvents):
                issueKey = eventLog[i].attributes["concept:name"]
                dbIssue = dbContext.GetIssue(issueKey)
                dbIssue.Fitness = issueFitnessCollection[i]["trace_fitness"]
                dbContext.UpdateEntity(dbIssue)
        except Exception as e:
            logging.error("Error occurred when adding issue fitness to each issue in db", exc_info=True)

    def AddTeamMemberTypToDbFromCsv(self):
        fileManager = CsvFileManager(ProcessEnhancement.__DbContext, ProcessEnhancement.__Settings)
        fileManager.UpdateTeamMemberTypeFromCsv()