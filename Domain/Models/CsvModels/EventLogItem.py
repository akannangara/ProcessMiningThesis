import logging
from typing import List
from dataclasses import dataclass

from TChangeLog import TChangeLog
from datetime import datetime

@dataclass
class EventLogItem():
    IssueId : int
    IssueKey : str
    TeamMemberKey : str
    TimeStamp : datetime
    From : str
    To : str
    Field : str
    FieldType : str

    def __init__(self, changeLogItem : TChangeLog):
        self.IssueId = changeLogItem.IssueId
        self.IssueKey = changeLogItem.IssueKey
        self.TeamMemberKey = changeLogItem.Author.Key
        self.TimeStamp = changeLogItem.Created
        self.From = changeLogItem.FromString
        self.To = changeLogItem.ToString
        self.Field = changeLogItem.Field
        self.FieldType = changeLogItem.FieldType