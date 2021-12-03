from sqlalchemy import Column, Integer, String

from Base import Base

class DbProjects(Base):
		__tablename__ = 'Projects'

		Id = Column(Integer, primary_key=True, autoincrement=False)
		Key = Column(String(255))
		Name = Column(String(255))
		ProjectTypeKey = Column(String(255))

		def __repr__(self):
				return "<Projects(Id='%d', Key='%s', Name='%s', ProjectTypeKey='%s'>" % (
										self.Id, self.Key, self.Name, self.ProjectTypeKey)