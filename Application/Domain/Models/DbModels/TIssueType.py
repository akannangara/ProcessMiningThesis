import logging
from typing import List
from pydantic import BaseModel

from sqlalchemy import Column, Integer, String, Boolean

from Base import Base

from JiraIssueType import JiraIssueType

class TIssueType(Base):
		__tablename__ = 'IssueType'

		Id = Column(Integer, primary_key=True, autoincrement=False)
		Description = Column(String)
		Name = Column(String(255))
		Subtask = Column(Boolean)

		def __repr__(self):
				return "<IssueTypes(Id='%d', Description='%s', Name='%s', Subtask='%r'>" % (
										self.Id, self.Description, self.Name, self.Subtask)

		def __init__(self, jiraIssueType : JiraIssueType):
				self.Id = int(jiraIssueType.id)
				self.Description = jiraIssueType.description
				self.Name = jiraIssueType.name
				self.Subtask = bool(jiraIssueType)