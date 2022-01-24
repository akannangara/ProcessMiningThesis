import logging
from typing import List
from pydantic import BaseModel

from dataclasses import dataclass
from statistics import mean

from TIssue import TIssue

from datetime import datetime

@dataclass
class MLDataSetModel:
    Key : str
    Priority : int = 3
    TimeEstimate : int = 0
    CurrentStatus : int = 0
    TimeOriginalEstimate : int = 0
    DeltaDueCreate : int = 60*60*24*365
    TimeSpent : int = 0
    CalculatedWorkRatio : int = 0
    TimeSinceToDo : int = 0
    ComingBack : int = 0
    SizeSummary : int = 0
    SizeDescription : int = 0
    ChangeSinceCreation : int = 0
    ChangeSinceLastStatus : int = 0

    Story : int = 0
    Epic : int = 0
    Task : int = 0
    Bug : int = 0
    Incident : int = 0
    SubTask : int = 0

    CDeliveryManager : int = 0
    CProjectManager : int = 0
    CSeniorDeveloper : int = 0
    CMediorDeveloper : int = 0
    CJuniorDeveloper : int = 0
    CDesigner : int = 0
    CSystemAccount : int = 0
    CTester : int = 0
    CIntern : int = 0
    CClient : int = 0
    CUndefined : int = 1

    ADeliveryManager : int = 0
    AProjectManager : int = 0
    ASeniorDeveloper : int = 0
    AMediorDeveloper : int = 0
    AJuniorDeveloper : int = 0
    ADesigner : int = 0
    ASystemAccount : int = 0
    ATester : int = 0
    AIntern : int = 0
    AClient : int = 0
    AUndefined : int = 1

    RDeliveryManager : int = 0
    RProjectManager : int = 0
    RSeniorDeveloper : int = 0
    RMediorDeveloper : int = 0
    RJuniorDeveloper : int = 0
    RDesigner : int = 0
    RSystemAccount : int = 0
    RTester : int = 0
    RIntern : int = 0
    RClient : int = 0
    RUndefined : int = 1

    Rejected : int = 0
    WorkRatio : float = 0.0
    Fitness : float = 0.0

    def __init__(self, issue : TIssue, priority : int, issueType : str, currentStatus : int, timeEstimate : int, timespent : int,
                 timeSinceToDo : int, comingBack : bool, dueDate : datetime, sizeSummary : int,
                 sizeDescription : int, changeSinceCreation : bool, changeSinceLastStatusChange: bool,
                 assignee, rejected : bool):
        self.Key = issue.Key
        self.Priority = priority
        self.TimeEstimate = timeEstimate
        self.CurrentStatus = currentStatus
        self.TimeOriginalEstimate = 0
        if issue.TimeOriginalEstimate:
            self.TimeOriginalEstimate = issue.TimeOriginalEstimate
        self.DeltaDueCreate = 60*60*24*365
        if dueDate:
            self.DeltaDueCreate = (dueDate - issue.Created).total_seconds()
        if self.DeltaDueCreate < 0:
            self.DeltaDueCreate == 0
        self.TimeSpent = timespent
        if timespent > 0 and timeEstimate > 0:
            self.CalculatedWorkRatio = (timespent / timeEstimate) * 100
        else:
            self.CalculatedWorkRatio = 0
        self.TimeSinceToDo = timeSinceToDo
        self.ComingBack = comingBack
        self.SizeSummary = sizeSummary
        self.SizeDescription = sizeDescription
        self.ChangeSinceCreation = int(changeSinceCreation)
        self.ChangeSinceLastStatus = int(changeSinceLastStatusChange)

        self.Story = (int(issueType == "Story"))
        self.Epic = (int(issueType == "Epic"))
        self.Task = (int(issueType == "Task"))
        self.Bug = (int(issueType == "Bug"))
        self.Incident = (int(issueType == "Incident"))
        self.SubTask = (int(issueType == "Sub-task"))

        if (issue.Creator):
            self.CDeliveryManager = (int(issue.Creator.Type=="Delivery manager"))
            self.CProjectManager = (int(issue.Creator.Type=="Project manager"))
            self.CSeniorDeveloper = (int(issue.Creator.Type=="Senior developer"))
            self.CMediorDeveloper = (int(issue.Creator.Type=="Medior developer"))
            self.CJuniorDeveloper = (int(issue.Creator.Type=="Junior developer"))
            self.CDesigner = (int(issue.Creator.Type=="Designer"))
            self.CSystemAccount = (int(issue.Creator.Type=="Systeem account"))
            self.CTester = (int(issue.Creator.Type=="Tester"))
            self.CIntern = (int(issue.Creator.Type=="Stagiair"))
            self.CClient = (int(issue.Creator.Type=="Klant"))
            self.CUndefined = (int(issue.Creator.Type==""))

        if (assignee):
            self.ADeliveryManager = (int(assignee.Type=="Delivery manager"))
            self.AProjectManager = (int(assignee.Type=="Project manager"))
            self.ASeniorDeveloper = (int(assignee.Type=="Senior developer"))
            self.AMediorDeveloper = (int(assignee.Type=="Medior developer"))
            self.AJuniorDeveloper = (int(assignee.Type=="Junior developer"))
            self.ADesigner = (int(assignee.Type=="Designer"))
            self.ASystemAccount = (int(assignee.Type=="Systeem account"))
            self.ATester = (int(assignee.Type=="Tester"))
            self.AIntern = (int(assignee.Type=="Stagiair"))
            self.AClient = (int(assignee.Type=="Klant"))
            self.AUndefined = (int(assignee.Type==""))

        if (issue.Reporter):
            self.RDeliveryManager = (int(issue.Reporter.Type=="Delivery manager"))
            self.RProjectManager = (int(issue.Reporter.Type=="Project manager"))
            self.RSeniorDeveloper = (int(issue.Reporter.Type=="Senior developer"))
            self.RMediorDeveloper = (int(issue.Reporter.Type=="Medior developer"))
            self.RJuniorDeveloper = (int(issue.Reporter.Type=="Junior developer"))
            self.RDesigner = (int(issue.Reporter.Type=="Designer"))
            self.RSystemAccount = (int(issue.Reporter.Type=="Systeem account"))
            self.RTester = (int(issue.Reporter.Type=="Tester"))
            self.RIntern = (int(issue.Reporter.Type=="Stagiair"))
            self.RClient = (int(issue.Reporter.Type=="Klant"))
            self.RUndefined = (int(issue.Reporter.Type==""))

        self.WorkRatio = issue.WorkRatio #if really large then rejected 
        if self.WorkRatio > 9000000000:
            if timespent > 0 and self.TimeOriginalEstimate > 0:
                self.WorkRatio = (timespent / self.TimeEstimate) *100
            else:
                self.WorkRatio = 0
        elif self.WorkRatio == -1: #if -1 then no originalTimeEstimate
            if timespent > 0 and self.TimeEstimate > 0:
                self.WorkRatio = (timespent / self.TimeEstimate) *100
            else:
                self.WorkRatio = 0

        self.Fitness = issue.Fitness
        self.Rejected = (int(rejected))