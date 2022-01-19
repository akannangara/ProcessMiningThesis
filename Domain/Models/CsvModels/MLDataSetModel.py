import logging
from typing import List
from pydantic import BaseModel

from dataclasses import dataclass
from statistics import mean

from TIssue import TIssue

@dataclass
class MLDataSetModel:
    Key : str
    Priority : int = 3
    TimeEstimate : int = 0
    TimeOriginalEstimate : int = 0
    DeltaDueCreate : int = 60*60*24*365
    SizeSummary : int = 0
    SizeDescription : int = 0

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

    WorkRatio : float = 0.0
    Fitness : float = 0.0

    def __init__(self, issue : TIssue):
        self.Key = issue.Key
        self.Priority = 3 #not defined
        if issue.PriorityId:
            self.Priority = issue.PriorityId
        self.TimeEstimate = 0 #not defined
        if issue.TimeEstimate:
            self.TimeEstimate = issue.TimeEstimate
        self.TimeOriginalEstimate = 0 #not defined
        if issue.TimeOriginalEstimate: #not defined
            self.TimeOriginalEstimate = issue.TimeOriginalEstimate
        self.DeltaDueCreate = 60*60*24*365
        if issue.DueDate:
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

        if (issue.Assignee):
            self.ADeliveryManager = (int(issue.Assignee.Type=="Delivery manager"))
            self.AProjectManager = (int(issue.Assignee.Type=="Project manager"))
            self.ASeniorDeveloper = (int(issue.Assignee.Type=="Senior developer"))
            self.AMediorDeveloper = (int(issue.Assignee.Type=="Medior developer"))
            self.AJuniorDeveloper = (int(issue.Assignee.Type=="Junior developer"))
            self.ADesigner = (int(issue.Assignee.Type=="Designer"))
            self.ASystemAccount = (int(issue.Assignee.Type=="Systeem account"))
            self.ATester = (int(issue.Assignee.Type=="Tester"))
            self.AIntern = (int(issue.Assignee.Type=="Stagiair"))
            self.AClient = (int(issue.Assignee.Type=="Klant"))
            self.AUndefined = (int(issue.Assignee.Type==""))

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

        self.WorkRatio = issue.WorkRatio #if really large then rejected if -1 then no originalTimeEstimate
        self.Fitness = issue.Fitness