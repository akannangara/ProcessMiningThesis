import logging
from typing import List
from pydantic import BaseModel

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from Base import Base

from JiraStatus import JiraStatus


class TStatus(Base):
		__tablename__ = 'Statuses'

		Id = Column(Integer, primary_key=True)
		Description = Column(String)
		Name = Column(String(255))
		
		def __repr__(self):
				return "<Statuses(Id='%d', Description='%s', Name='%s'>" % (
								self.Id, self.Description, self.Name)

		def __init__(self, jiraStatus : JiraStatus):
				self.Id = jiraStatus.id
				self.Description = jiraStatus.description
				self.Name = jiraStatus.name