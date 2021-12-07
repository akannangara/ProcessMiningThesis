import logging
from typing import List
from pydantic import BaseModel

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

import datetime

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

		AggregateProgressId = Column(Integer, ForeignKey('Progress.IssueId'))
		AggregateProgress = relationship("TProgress", foreign_keys=[AggregateProgressId])

		DueDate = Column(DateTime)

		ProgressId = Column(Integer, ForeignKey('Progress.IssueId'))
		Progress = relationship("TProgress", foreign_keys=[ProgressId])


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
				self.IssueType = TIssueType(jiraIssue.issuetype)
				self.IssueTypeId = self.IssueType.Id
				self.TimeSpent = jiraIssue.timespent

				self.Project = TProject(jiraIssue.project)
				self.ProjectId = self.Project.Id

				self.AggregateTimeSpent = jiraIssue.aggregatetimespent

				self.Resolution = TResolution(jiraIssue.resolution)
				self.ResolutionId = self.Resolution.Id

				self.ResolutionDate = datetime(jiraIssue.resolutiondate)
				self.WorkRatio = jiraIssue.workratio
				self.Created = datetime(jiraIssue.created)

				self.Priority = TPriority(jiraIssue.priority)
				self.PriorityId = self.Priority.Id

				self.TimeEstimate = jiraIssue.timeestimate
				self.AggregateTimeOriginalEstimate = jiraIssue.aggregatetimeoriginalestimate

				sef.Assignee = TTeamMember(jiraIssue.assignee)
				self.AssigneeId = self.Assignee.Key

				self.Updated = datetime(jiraIssue.updated)

				self.Status = TStatus(jiraIssue.status)
				self.StatusId = self.Status.Id

				self.TimeOriginalEstimate = jiraIssue.timeoriginalestimate

				self.TimeTracking = TTimeTracking(jiraIssue.timetracking, self.Id)
				self.TimeTrackingId = self.TimeTracking.Id 

				self.AggregateTimeEstimate = jiraIssue.aggregatetimeestimate

				self.Reporter = TTeamMember(jiraIssue.reporter)
				self.ReporterId = self.Reporter.Key
				self.Creator = TTeamMember(jiraIssue.creator)
				self.CreatorId = self.Creator.Key

				self.Summary = jiraIssue.summary

				self.AggregateProgress = TProgress(jiraIssue.aggregateprogress)
				self.AggregateProgressId = self.AggregateProgress.Id
				self.DueDate = datetime(jiraIssue.duedate)
				self.Progress = TProgress(jiraIssue.progress)
				self.ProgressId = self.Progress.Id