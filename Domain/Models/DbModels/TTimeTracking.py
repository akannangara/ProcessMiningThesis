import logging
from typing import List
from pydantic import BaseModel

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from Base import Base

from JiraTimeTracking import JiraTimeTracking


#TODO check if this works with foreign key and stuff
class TTimeTracking(Base):
		__tablename__ = 'TimeTracking'

		Id = Column(Integer, primary_key=True, autoincrement=1)

		OriginalEstimate = Column(Integer)
		RemainingEstimate = Column(Integer)
		TimeSpent = Column(Integer)

		IssueId = Column(Integer, ForeignKey('Issues.Id'))



		def __repr__(self):
				return "<TimeTracking(Id='%d', OriginalEstimate='%d', RemainingEstimate='%d', TimeSpent='%d', IssueId='%d'>" % (
								self.Id, self.OriginalEstimate, self.RemainingEstimate, self.TimeSpent, self.IssueId)

		def __init__(self, jiraTimeTracking : JiraTimeTracking, issueId : int):
				self.Id = jiraTimeTracking.id
				self.OriginalEstimate = jiraTimeTracking.originalEstimateSeconds
				self.RemainingEstimate = jiraTimeTracking.remainingEstimateSeconds
				self.TimeSpent = jiraTimeTracking.timeSpentSeconds
				self.IssueId = issueId