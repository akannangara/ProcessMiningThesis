import logging
from typing import List
from pydantic import BaseModel

from dataclasses import dataclass
from statistics import mean

from TIssue import TIssue

@dataclass
class MLDataSetModel:
    Key : str
    Priority : int
    TimeEstimate : int
    TimeOriginalEstimate : int
    DeltaDueCreate : int
    SizeSummary : int
    SizeDescription : int

    Story : int
    Epic : int
    Task : int
    Bug : int
    Incident : int
    SubTask : int

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
    CUndefined : int = 0

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
    AUndefined : int = 0

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
    RUndefined : int = 0

    def __init__(self, issue : TIssue):
        self.Key = issue.Key
        self.Priority = issue.Priority
        self.TimeEstimate = issue.TimeEstimate
        self.TimeOriginalEstimate = issue.TimeOriginalEstimate
        self.DeltaDueCreate = (issue.DueDate - issue.Created).total_seconds()
        self.SizeSummary = len(issue.Summary.split())
        self.SizeDescription = len(issue.Description.split())

        self.Story = (int(issue.IssueType.Name == "Story"))
        self.Epic = (int(issue.IssueType.Name == "Epic"))
        self.Task = (int(issue.IssueType.Name == "Task"))
        self.Bug = (int(issue.IssueType.Name == "Bug"))
        self.Incident = (int(issue.IssueType.Name == "Incident"))
        self.SubTask = (int(issue.IssueType.Name == "Sub-task"))

        if (issue.Creator):
            CDeliveryManager = (int(issue.Creator.Type=="Delivery manager"))
            CProjectManager = (int(issue.Creator.Type=="Project manager"))
            CSeniorDeveloper = (int(issue.Creator.Type=="Senior developer"))
            CMediorDeveloper = (int(issue.Creator.Type=="Medior developer"))
            CJuniorDeveloper = (int(issue.Creator.Type=="Junior developer"))
            CDesigner = (int(issue.Creator.Type=="Designer"))
            CSystemAccount = (int(issue.Creator.Type=="Systeem account"))
            CTester = (int(issue.Creator.Type=="Tester"))
            CIntern = (int(issue.Creator.Type=="Stagiair"))
            CClient = (int(issue.Creator.Type=="Klant"))
            CUndefined = (int(issue.Creator.Type==""))

        if (issue.Assignee):
            ADeliveryManager = (int(issue.Assignee.Type=="Delivery manager"))
            AProjectManager = (int(issue.Assignee.Type=="Project manager"))
            ASeniorDeveloper = (int(issue.Assignee.Type=="Senior developer"))
            AMediorDeveloper = (int(issue.Assignee.Type=="Medior developer"))
            AJuniorDeveloper = (int(issue.Assignee.Type=="Junior developer"))
            ADesigner = (int(issue.Assignee.Type=="Designer"))
            ASystemAccount = (int(issue.Assignee.Type=="Systeem account"))
            ATester = (int(issue.Assignee.Type=="Tester"))
            AIntern = (int(issue.Assignee.Type=="Stagiair"))
            AClient = (int(issue.Assignee.Type=="Klant"))
            AUndefined = (int(issue.Assignee.Type==""))

        if (issue.Reporter):
            RDeliveryManager = (int(issue.Reporter.Type=="Delivery manager"))
            RProjectManager = (int(issue.Reporter.Type=="Project manager"))
            RSeniorDeveloper = (int(issue.Reporter.Type=="Senior developer"))
            RMediorDeveloper = (int(issue.Reporter.Type=="Medior developer"))
            RJuniorDeveloper = (int(issue.Reporter.Type=="Junior developer"))
            RDesigner = (int(issue.Reporter.Type=="Designer"))
            RSystemAccount = (int(issue.Reporter.Type=="Systeem account"))
            RTester = (int(issue.Reporter.Type=="Tester"))
            RIntern = (int(issue.Reporter.Type=="Stagiair"))
            RClient = (int(issue.Reporter.Type=="Klant"))
            RUndefined = (int(issue.Reporter.Type==""))