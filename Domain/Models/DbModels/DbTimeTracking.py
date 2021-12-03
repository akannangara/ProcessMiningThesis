from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from Base import Base


#TODO check if this works with foreign key and stuff
class DbTimeTracking(Base):
		__tablename__ = 'DbTimeTracking'

		Id = Column(Integer, primary_key=True, autoincrement=1)

		OriginalEstimate = Column(Integer)
		RemainingEstimate = Column(Integer)
		TimeSpent = Column(Integer)

		IssueId = Column(Integer, ForeignKey('Issues.Id'))
		Issue = relationship("Issues", back_populates="Progress")



		def __repr__(self):
				return "<DbTimeTracking(Id='%d', OriginalEstimate='%d', RemainingEstimate='%d', TimeSpent='%d', IssueId='%d'>" % (
								self.Id, self.OriginalEstimate, self.RemainingEstimate, self.TimeSpent, self.IssueId)