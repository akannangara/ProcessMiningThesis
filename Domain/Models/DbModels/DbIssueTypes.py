﻿from sqlalchemy import Column, Integer, String, Boolean

from Base import Base

class DbIssueTypes(Base):
		__tablename__ = 'IssueTypes'

		Id = Column(Integer, primary_key=True, autoincrement=False)
		Description = Column(String)
		Name = Column(String(255))
		Subtask = Column(Boolean)

		def __repr__(self):
				return "<IssueTypes(Id='%d', Description='%s', Name='%s', Subtask='%r'>" % (
										self.Id, self.Description, self.Name, self.Subtask)