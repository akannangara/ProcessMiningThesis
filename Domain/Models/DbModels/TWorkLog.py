import logging
from typing import List
from pydantic import BaseModel

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from Base import Base

from JiraWorkLog import JiraWorkLogItem


#TODO check if this works with foreign key and stuff
class TWorkLog(Base):
		__tablename__ = 'WorkLog'

		Id = Column(Integer, primary_key=True)

		AuthorId = Column(String(255), ForeignKey('TeamMembers.Key'))
		Author = relationship("TTeamMember", foreign_keys=[AuthorId])

		UpdateAuthorId = Column(String(255), ForeignKey('TeamMembers.Key'))
		UpdateAuthor = relationship("TTeamMember", foreign_keys=[UpdateAuthorId])

		Created = Column(DateTime)
		Updated = Column(DateTime)
		Started = Column(DateTime)

		TimeSpent = Column(Integer)

		IssueId = Column(Integer, ForeignKey("Issues.Id"))



		def __repr__(self):
				return "<DbWorkLog(Id='%d', AuthorId='%d', Created='%f' Updated='%f', Started='%s', TimeSpent='%s', IssueId='%d'>" % (
										self.Id, self.AuthorId, self.Created, self.Updated, self.Started, self.TimeSpent, self.IssueId) 

		def __init__(self, jiraWorkLogItem : JiraWorkLogItem):
				self.Id = int(jiraWorkLogItem.id)
				self.Created = jiraWorkLogItem.created[:-5]
				self.Updated = jiraWorkLogItem.updated[:-5]
				self.Started = jiraWorkLogItem.started[:-5]
				self.TimeSpent = jiraWorkLogItem.timeSpentSeconds
				self.IssueId = int(jiraWorkLogItem.issueId)
