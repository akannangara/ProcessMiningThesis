from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from Base import Base


#TODO check if this works with foreign key and stuff
class DbProgress(Base):
		__tablename__ = 'Progress'

		Id = Column(Integer, primary_key=True, autoincrement=1)

		Progress = Column(Integer)
		Total = Column(Integer)
		Percent = Column(Integer, nullable=True)

		IssueId = Column(Integer, ForeignKey('Issues.Id'))
		Issue = relationship("Issues", back_populates="Progress")



		def __repr__(self):
				if self.Percent == None:
						return "<Progress(Id='%d', Progress='%d', Total='%d', IssueId='%d'>" % (
										self.Id, self.Progress, self.Total, self.IssueId)
				return "<Progress(Id='%d', Progress='%d', Total='%d', Percent='%d', IssueId='%d'>" % (
										self.Id, self.Progress, self.Total, self.Percent, self.IssueId) 