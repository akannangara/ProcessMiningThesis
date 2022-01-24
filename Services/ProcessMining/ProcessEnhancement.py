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

from DateTimeConverter import DateTimeConverter

from TTeamMember import TTeamMember



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
        logging.info("Creating Ml data set")
        try:
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

                        priority = 3
                        if issue.PriorityId:
                            priority = issue.PriorityId
                        sizeSummary = len(issue.Summary.split())
                        sizeDescription = 0
                        if issue.Description:
                            sizeDescription = len(issue.Description.split())
                        timeEstimate = 0
                        if issue.TimeEstimate:
                            timeEstimate = issue.TimeEstimate
                        issueType = issue.IssueType.Name
                        dueDate = None
                        if issue.DueDate:
                            dueDate = issue.DueDate
                        assignee = None
                        if issue.Assignee:
                            assignee = issue.Assignee
                        for j in range(len(changelogs)):
                            if changelogs[j].Field == 'priority':
                                if changelogs[j].FromString:
                                    priority = ProcessEnhancement.__Settings.PriorityIntDictionary[changelogs[j].FromString]
                            elif changelogs[j].Field == 'summary':
                                sizeSummary = len(changelogs[j].FromString.split())
                            elif changelogs[j].Field == 'description':
                                if changelogs[j].FromString:
                                    sizeDescription = len(changelogs[j].FromString.split())
                            elif changelogs[j].Field == 'timeestimate':
                                if changelogs[j].FromString:
                                    timeEstimate = int(changelogs[j].FromString)
                            elif changelogs[j].Field == 'issuetype':
                                issueType = changelogs[j].FromString
                            elif changelogs[j].Field == 'duedate':
                                if changelogs[j].FromString:
                                    dueDate = DateTimeConverter.ConvertDatetime(changelogs[j].FromString)
                            elif changelogs[j].Field == 'assignee':
                                searchResult = db.Query(TTeamMember, "Name", changelogs[j].FromString)
                                if searchResult:
                                    assignee = searchResult[0]

                        timeSpent = 0
                        for j in range(len(changelogs)):
                            if changelogs[j].Field == 'timespent' and changelogs[j].FromString:
                                timeSpent = changelogs[j].FromString

                        changeFields = ['priority', 'issuetype', 'summary', 'description', 'Attachment', 'assignee', 'duedate']
                        comingBack = 0
                        timeSpent = 0
                        reachedLastStatusChange = False
                        changeSinceCreation = False
                        for j in reversed(range(i)):
                            if changelogs[j].Field == 'status':
                                reachedLastStatusChange = True
                                if comingBack == 0 and ProcessEnhancement.__Settings.StatusIntDictionary[changelogs[j].ToString] > currentStatus:
                                    comingBack = 1
                            elif changelogs[j].Field == 'timespent' and timeSpent == 0:
                                timeSpent = int(changelogs[j].ToString)
                            elif changelogs[j].Field in changeFields and not(reachedLastStatusChange):
                                changeSinceLastStatus = True

                        timeSinceToDo = 0
                        reachedToDo = False
                        changeSinceCreation = False
                        for j in range(i):
                            if changelogs[j].Field == 'status' and changelogs[j].ToString == 'To Do' and not(reachedToDo):
                                timeSinceToDo = (changelogs[i].Created - changelogs[j].Created).total_seconds()
                                reachedToDo = True
                            elif changelogs[j].Field in changeFields:
                                changeSinceCreation = True

                        rejected = False
                        if issue.StatusId == completedStatusIds[1]:
                            rejected = True
                        MLDataSetCollection.append(MLDataSetModel(issue, priority, issueType, currentStatus, timeEstimate, timeSpent, timeSinceToDo, comingBack,
                                                                 dueDate, sizeSummary, sizeDescription, changeSinceCreation,
                                                                 changeSinceCreation, assignee, rejected))
            fileManager = CsvFileManager(ProcessEnhancement.__DbContext, ProcessEnhancement.__Settings)
            fileManager.DeleteFileIfExists(ProcessEnhancement.__Settings.CsvStorageManager["mlDataSet"])
            fileManager.CreateFileFromEntityCollection(MLDataSetCollection, MLDataSetModel, \
            ProcessEnhancement.__Settings.CsvStorageManager["mlDataSet"])
        except Exception as e:
            logging.error("Error creating ml dataset", exc_info=True)