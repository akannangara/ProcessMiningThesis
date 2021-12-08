import logging
from typing import List
from pydantic import BaseModel

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from datetime import datetime

from Base import Base

from JiraIssue import JiraIssue

from TIssueType import TIssueType
from TProject import TProject
from TResolution import TResolution
from TPriority import TPriority
from TTeamMember import TTeamMember
from TStatus import TStatus
from TTimeTracking import TTimeTracking
from TProgress import TProgress


#TODO check if this works with foreign key and stuff
class TIssue(Base):
		__tablename__ = 'Issues'

		Id = Column(Integer, primary_key=True, autoincrement=False)
		Key = Column(String(255))

		IssueTypeId = Column(Integer, ForeignKey('IssueType.Id'))
		IssueType = relationship("TIssueType")

		TimeSpent = Column(Integer)

		ProjectId = Column(Integer, ForeignKey('Projects.Id'))
		Project = relationship("TProject")

		AggregateTimeSpent = Column(Integer)

		ResolutionId = Column(Integer, ForeignKey('Resolutions.Id'))
		Resolution = relationship("TResolution")

		ResolutionDate = Column(DateTime)
		WorkRatio = Column(Float)
		Created = Column(DateTime)
		
		PriorityId = Column(Integer, ForeignKey('Priorities.Id'))
		Priority = relationship("TPriority")

		TimeEstimate = Column(Integer)
		AggregateTimeOriginalEstimate = Column(Integer)
		
		AssigneeId = Column(String(255), ForeignKey('TeamMembers.Key'))
		Assignee = relationship("TTeamMember", foreign_keys=[AssigneeId])

		Updated = Column(DateTime)
		
		StatusId = Column(Integer, ForeignKey('Statuses.Id'))
		Status = relationship("TStatus")

		TimeOriginalEstimate = Column(Integer)

		TimeTrackingId = Column(Integer, ForeignKey('TimeTracking.Id'))
		TimeTracking = relationship("TTimeTracking", foreign_keys=[TimeTrackingId])

		AggregateTimeEstimate = Column(Integer)

		ReporterId = Column(String(255), ForeignKey('TeamMembers.Key'))
		Reporter = relationship("TTeamMember", foreign_keys=[ReporterId])
		CreatorId = Column(String(255), ForeignKey('TeamMembers.Key'))
		Creator = relationship("TTeamMember", foreign_keys=[CreatorId])

		Summary = Column(String)

		AggregateProgressId = Column(Integer, ForeignKey('Progress.Id'))
		AggregateProgress = relationship("TProgress", foreign_keys=[AggregateProgressId], uselist=False)

		DueDate = Column(DateTime)

		ProgressId = Column(Integer, ForeignKey('Progress.Id'))
		Progress = relationship("TProgress", foreign_keys=[ProgressId], uselist=False)

		WorkLogs = relationship("TWorkLog", backref="Issue")
		ChangeLogs = relationship("TChangeLog", backref="Issue")


		def __repr__(self):
				return "<Issue(Id='%d', Key='%s', IssueTypeId='%d' TimeSpent='%d', ProjectId='%d', AggregateTimeSpent='%d', \
												AggregateTimeOriginalEstimate='%d', AssigneeId='%d', Updated='%f', StatusId='%d', TimeOriginalEstimate='%d', \
												TimeTrackingId='%d', AggregateTimeEstimate='%d', ReporterId='%d', CreatorId='%d', Summary='%s', \
												AggregateProgressId='%d', DueDate='%f', ProgressId='%d'>" % (
										self.Id, self.Key, self.IssueTypeId, self.TimeSpent, self.ProjectId, self.AggregateTimeSpent,
										self.ResolutionId, self.ResolutionDate, self.WorkRatio, self.Created, self.PriorityId, self.TimeEstimate,
										self.AggregateTimeOriginalEstimate, self.AssigneeId, self.Updated, self.StatusId, self.TimeOriginalEstimate,
										self.TimeTrackingId, self.AggregateTimeEstimate, self.ReporterId, self.CreatorId, self.Summary,
										self.AggregateProgressId, self.DueDate, self.ProgressId)

		def __init__(self, jiraIssue : JiraIssue):
				self.Id = int(jiraIssue.id)
				self.Key = jiraIssue.key
				self.TimeSpent = jiraIssue.timespent
				self.AggregateTimeSpent = jiraIssue.aggregatetimespent
				if jiraIssue.resolutiondate:
						self.ResolutionDate = jiraIssue.resolutiondate[:-5]
				self.WorkRatio = jiraIssue.workratio
				self.Created = jiraIssue.created[:-5]
				self.TimeEstimate = jiraIssue.timeestimate
				self.AggregateTimeOriginalEstimate = jiraIssue.aggregatetimeoriginalestimate
				self.Updated = jiraIssue.updated[:-5]
				self.TimeOriginalEstimate = jiraIssue.timeoriginalestimate
				self.AggregateTimeEstimate = jiraIssue.aggregatetimeestimate
				self.Summary = jiraIssue.summary
				self.DueDate = jiraIssue.duedate
				self.DueDate = jiraIssue.duedate