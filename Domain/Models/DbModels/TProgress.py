import logging
from typing import List
from pydantic import BaseModel

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from Base import Base

from JiraProgress import JiraProgress

#TODO check if this works with foreign key and stuff
class TProgress(Base):
		__tablename__ = 'Progress'

		Id = Column(Integer, primary_key=True, autoincrement=True)

		Progress = Column(Integer)
		Total = Column(Integer)
		Percent = Column(Integer, nullable=True)

		IssueId = Column(Integer, ForeignKey('Issues.Id'), unique=False)

		def __repr__(self):
				if self.Percent == None:
						return "<Progress(Progress='%d', Total='%d', IssueId='%d'>" % (
										self.Id, self.Progress, self.Total, self.IssueId)
				return "<Progress(Progress='%d', Total='%d', Percent='%d', IssueId='%d'>" % (
										self.Progress, self.Total, self.Percent, self.IssueId) 

		def __init__(self, jiraProgress : JiraProgress, issueId : int):
				self.Progress = JiraProgress.progress
				self.Total = jiraProgress.total
				self.Percent = jiraProgress.percent
				self.IssueId = issueId