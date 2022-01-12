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

    def __init__(self, *args, **kwargs):
        if (len(args) == 1):#got changeLogs
            changeLogItem = args[0]
            self.IssueId = changeLogItem.IssueId
            self.IssueKey = changeLogItem.IssueKey
            self.TeamMemberKey = changeLogItem.Author.Key
            self.TimeStamp = changeLogItem.Created
            self.From = changeLogItem.FromString
            self.To = changeLogItem.ToString
            self.Field = changeLogItem.Field
            self.FieldType = changeLogItem.FieldType
        if (len(args)==8):#got args List
            arguments = args
            self.IssueId = arguments[0]
            self.IssueKey = arguments[1]
            self.TeamMemberKey = arguments[2]
            self.TimeStamp = arguments[3]
            self.From = arguments[4]
            self.To = arguments[5]
            self.Field = arguments[6]
            self.FieldType = arguments[7]