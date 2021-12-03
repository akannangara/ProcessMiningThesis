from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from Base import Base


#TODO check if this works with foreign key and stuff
class DbStatus(Base):
		__tablename__ = 'DbStatus'

		Id = Column(Integer, primary_key=True)
		Description = Column(String)
		Name = Column(String(255))
		
		def __repr__(self):
				return "<DbStatus(Id='%d', Description='%s', Name='%s'>" % (
								self.Id, self.Description, self.Name)