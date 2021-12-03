from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from Base import Base


#TODO check if this works with foreign key and stuff
class DbResolution(Base):
		__tablename__ = 'DbResolution'

		Id = Column(Integer, primary_key=True)
		Description = Column(String)
		Name = Column(String(255))
		
		def __repr__(self):
				return "<Progress(Id='%d', Description='%s', Name='%s'>" % (
								self.Id, self.Description, self.Total)