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

    Story : int
    Epic : int
    Task : int
    Bug : int
    Incident : int

    CProjectManager : int
    CSeniorDeveloper : int
    CMediorDeveloper : int
    CJuniorDeveloper : int
    CDesigner : int
    CSystemAccount : int
    CTester : int
    CIntern : int
    CClient : int
    CUndefined : int

    AProjectManager : int
    ASeniorDeveloper : int
    AMediorDeveloper : int
    AJuniorDeveloper : int
    ADesigner : int
    ASystemAccount : int
    ATester : int
    AIntern : int
    AClient : int
    AUndefined : int

    RProjectManager : int
    RSeniorDeveloper : int
    RMediorDeveloper : int
    RJuniorDeveloper : int
    RDesigner : int
    RSystemAccount : int
    RTester : int
    RIntern : int
    RClient : int
    RUndefined : int

    def __init__(self, issue : TIssue):
        self.Key = issue.Key
        self.Priority = issue.Priority
        self.TimeEstimate = issue.TimeEstimate
        self.TimeOriginalEstimate = issue.TimeOriginalEstimate
        self.DeltaDueCreate = (issue.DueDate - issue.Created).total_seconds()
        self.SizeSummary = len(issue.Summary.split())