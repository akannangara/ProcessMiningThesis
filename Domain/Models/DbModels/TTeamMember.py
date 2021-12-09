import logging
from typing import List
from pydantic import BaseModel

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from Base import Base

from JiraTeamMember import JiraTeamMember


#TODO check if this works with foreign key and stuff
class TTeamMember(Base):
		__tablename__ = 'TeamMembers'

		Key = Column(String(255), primary_key=True)
		DisplayName = Column(String)
		Name = Column(String(255))
		Active = Column(Boolean)
		Type = Column(String)
		
		def __repr__(self):
				return "<TeamMember(Key='%d', Description='%s', Name='%s', Active='%r', Type='%s'>" % (
								self.key, self.Description, self.Name, self.Active, self.Type)

		def __init__(self, jiraTeamMember : JiraTeamMember):
				self.Key = jiraTeamMember.key
				self.DisplayName = jiraTeamMember.displayName
				self.Name = jiraTeamMember.name
				self.Active = bool(jiraTeamMember.active)
				self.Type = ""