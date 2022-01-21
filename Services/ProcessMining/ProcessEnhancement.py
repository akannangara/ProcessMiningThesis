import logging
import os
import pandas as pd
from pydantic import BaseModel
from typing import List, Dict

from DbContext import DbContext
from CsvFileManager import CsvFileManager
from TIssue import TIssue
from TChangeLog import TChangeLog
from MLDataSetModel import MLDataSetModel



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

    def AddTeamMemberTypeToDbFromCsv(self):
        fileManager = CsvFileManager(ProcessEnhancement.__DbContext, ProcessEnhancement.__Settings)
        fileManager.UpdateTeamMemberTypeFromCsv()

    def CreateMLDataSet(self):
        completedStatusIds = ProcessEnhancement.__Settings.CompletedStatusIds
        doneIssues = ProcessEnhancement.__DbContext.QueryOr(TIssue, "StatusId",  str(completedStatusIds[0]), str(completedStatusIds[1]))
        MLDataSetCollection = []
        for issue in doneIssues:
            db = ProcessEnhancement.__DbContext
            changelogs = db.GetIssueChangeLogs(issue.Key)
            for i in range(len(changelogs)):
                if changelogs[i].Field == 'status':
                    if changelogs[i].ToString == 'Done' or changelogs[i].ToString == 'Rejected':
                        continue
                    currentStatus = ProcessEnhancement.__Settings.StatusIntDictionary[changelogs[i].ToString]
                    timeEstimate = 0
                    timeSpent = 0
                    comingBack = 0
                    for j in reversed(range(i)):
                        if changelogs[j].Field == 'timeestimate' and not(changelogs[j].ToString == timeEstimate):
                            if timeEstimate:
                                timeEstimate = int(changelogs[j].ToString)
                        elif changelogs[j].Field == 'timespent':
                            if changelogs[j].ToString:
                                timeSpent = int(changelogs[j].ToString)
                        elif changelogs[j].Field == 'status' and comingBack == 0:
                            if ProcessEnhancement.__Settings.StatusIntDictionary[changelogs[j].ToString] > currentStatus:
                                comingBack = 1
                                break
                        else:
                            raise ValueError(f"Unknown change log field {changelogs[j].Field}")
                    timeSinceToDo = 0
                    for j in range(i):
                        if changelogs[j].Field == 'status' and changelogs[j].ToString == 'To Do':
                            timeSinceToDo = (changelogs[i].Created - changelogs[j].Created).total_seconds()
                            break
                    rejected = False
                    if issue.StatusId == completedStatusIds[1]:
                        rejected = True
                    MLDataSetCollection.append(MLDataSetModel(issue, currentStatus, timeEstimate, timeSpent, timeSinceToDo, comingBack, rejected))
        fileManager = CsvFileManager(ProcessEnhancement.__DbContext, ProcessEnhancement.__Settings)
        fileManager.DeleteFileIfExists(ProcessEnhancement.__Settings.CsvStorageManager["mlDataSet"])
        fileManager.CreateFileFromEntityCollection(MLDataSetCollection, MLDataSetModel, \
        ProcessEnhancement.__Settings.CsvStorageManager["mlDataSet"])