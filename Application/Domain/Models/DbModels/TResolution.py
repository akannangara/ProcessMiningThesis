import logging
from typing import List
from pydantic import BaseModel

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from Base import Base

from JiraResolution import JiraResolution

#TODO check if this works with foreign key and stuff
class TResolution(Base):
		__tablename__ = 'Resolutions'

		Id = Column(Integer, primary_key=True)
		Description = Column(String)
		Name = Column(String(255))
		
		def __repr__(self):
				return "<Resolution(Id='%d', Description='%s', Name='%s'>" % (
								self.Id, self.Description, self.Total)

		def __init__(self, jiraResolution : JiraResolution):
				self.Id = int(jiraResolution.id)
				self.Description = jiraResolution.description
				self.Name = jiraResolution.name