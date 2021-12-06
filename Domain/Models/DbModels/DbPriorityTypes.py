from sqlalchemy import Column, Integer, String, Boolean

from Base import Base

class DbPriorityTypes(Base):
		__tablename__ = 'PriorityTypes'

		Id = Column(Integer, primary_key=True)
		Name = Column(String(255))

		def __repr__(self):
				return "<PriorityTypes(Id='%d', Name='%s'>" % (
										self.Id, self.Name)