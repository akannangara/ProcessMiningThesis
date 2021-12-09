from sqlalchemy import Column, Integer, String, Boolean, DateTime, BigInteger
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from Base import Base

from JiraChangeLog import JiraChangeLog
from DateTimeConverter import DateTimeConverter


#TODO check if this works with foreign key and stuff
class TChangeLog(Base):
		__tablename__ = 'ChangeLog'

		Id = Column(BigInteger, primary_key=True)

		AuthorId = Column(String(255), ForeignKey('TeamMembers.Key'))
		Author = relationship("TTeamMember")

		Created = Column(DateTime)

		Field = Column(String(225))
		FieldType = Column(String(255))
		FromString = Column(String)
		ToString = Column(String)

		IssueId = Column(Integer, ForeignKey('Issues.Id'))
		IssueKey = Column(String(255))


		def __repr__(self):
				return "<ChangeLog(Id='%d', AuthorId='%d', Created='%f' Field='%s', FieldType='%s', FromString='%s', ToString='%s', IssueId='%d'>" % (
										self.Id, self.AuthorId, self.Created, self.Field, self.FieldType, self.FromString, self.ToString, self.IssueId) 

		def __init__(self, jiraChangeLog : JiraChangeLog):
				self.Id = jiraChangeLog.id
				self.Created = DateTimeConverter.ConvertDatetime(jiraChangeLog.created[:-5])
				self.Field = jiraChangeLog.field
				self.FieldType = jiraChangeLog.fieldtype
				self.FromString = jiraChangeLog.fromString
				self.ToString = jiraChangeLog.toString
				self.IssueId = int(jiraChangeLog.issueId)
				self.IssueKey = jiraChangeLog.issueKey