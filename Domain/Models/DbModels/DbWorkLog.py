from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from Base import Base


#TODO check if this works with foreign key and stuff
class DbChangeLog(Base):
		__tablename__ = 'ChangeLog'

		Id = Column(Integer, primary_key=True)

		AuthorId = Column(Integer)
		Author = relationship("TeamMember", back_populates="ChangeLog")

		Created = Column(DateTime)
		Updated = Column(DateTime)
		Started = Column(DateTime)

		TimeSpent = Column(Integer)

		IssueId = Column(Integer, ForeignKey('Issues.Id'))
		Issue = relationship("Issues", back_populates="ChangeLog")



		def __repr__(self):
				return "<ChangeLog(Id='%d', AuthorId='%d', Created='%f' Updated='%f', Started='%s', TimeSpent='%s', IssueId='%d'>" % (
										self.Id, self.AuthorId, self.Created, self.Updated, self.Started, self.TimeSpent, self.IssueId) 