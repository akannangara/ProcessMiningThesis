import logging
from typing import List
from pydantic import BaseModel

from sqlalchemy import Column, Integer, String

from Base import Base

from JiraProject import JiraProject

class TProject(Base):
		__tablename__ = 'Projects'

		Id = Column(Integer, primary_key=True)
		Key = Column(String(255))
		Name = Column(String(255))
		ProjectTypeKey = Column(String(255))

		def __repr__(self):
				return "<Projects(Id='%d', Key='%s', Name='%s', ProjectTypeKey='%s'>" % (
										self.Id, self.Key, self.Name, self.ProjectTypeKey)

		def __init__(self, jiraProject : JiraProject):
				self.Id = int(jiraProject.id)
				self.Key = jiraProject.key
				self.Name = jiraProject.name
				self.ProjectTypeKey = jiraProject.projectTypeKey