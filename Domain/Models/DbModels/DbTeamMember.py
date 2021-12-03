from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from Base import Base


#TODO check if this works with foreign key and stuff
class DbTeamMember(Base):
		__tablename__ = 'DbTeamMember'

		Key = Column(String, primary_key=True)
		Description = Column(String)
		Name = Column(String(255))
		Active = Column(Boolean)
		Type = Column(String)
		
		def __repr__(self):
				return "<DbTeamMember(Id='%d', Description='%s', Name='%s', Active='%r'>" % (
								self.Id, self.Description, self.Name, self.Active)