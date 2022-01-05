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

    def __init__(self, issueId : str, issueKey : str, teamMember : str,\
                    timestamp : datetime, fromStatus : str, toStatus : str,\
                    field : str, fieldType : str):
        self.IssueId = issueId
        self.IssueKey = issueKey
        self.TeamMemberKey = teamMember
        self.TimeStamp = timestamp
        self.From = fromStatus
        self.To = toStatus
        self.Field = field
        self.FieldType = fieldType