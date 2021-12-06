from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from Base import Base


#TODO check if this works with foreign key and stuff
class DbIssue(Base):
		__tablename__ = 'Issues'

		Id = Column(Integer, primary_key=True)
		Key = Column(String(255))

		IssueTypeId = Column(Integer, ForeignKey('IssueTypes.Id'))
		IssueType = relationship("IssueTypes", back_populates="Issues", backref=backref('IssueTypes', IssueTypeId=Id))

		TimeSpent = Column(Integer)

		ProjectId = Column(Integer, ForeignKey('Projects.Id'))
		Project = relationship("Projects", back_populates="Issues", backref=backref('Projects', ProjectId=Id))

		AggregateTimeSpent = Column(Integer)

		ResolutionId = Column(Integer, ForeignKey('Resolutions.Id'))
		Resolution = relationship("Resolution", back_populates="Issues", backref=backref('Resolutions', ResolutionId=Id))

		ResolutionDate = Column(DateTime)
		WorkRatio = Column(Float)
		Created = Column(DateTime)
		
		PriorityId = Column(Integer, ForeignKey('PriorityTypes.Id'))
		Priority = relationship("PriorityTypes", back_populates="Issues", backref=backref('PriorityTypes', PriorityId=Id))

		TimeEstimate = Column(Integer)
		AggregateTimeOriginalEstimate = Column(Integer)
		
		AssigneeId = Column(Integer, ForeignKey('TeamMembers.Id'))
		Assignee = relationship("TeamMembers", back_populates="Issues", backref=backref('TeamMembers', AssigneeId=Id))

		Updated = Column(DateTime)
		
		StatusId = Column(Integer, ForeignKey('Statuses.Id'))
		Status = relationship("Statuses", back_populates="Issues", backref=backref('Statuses', StatusId=Id))

		TimeOriginalEstimate = Column(Integer)

		TimeTrackingId = Column(Integer, ForeignKey('TimeTracking.Id'))
		TimeTracking = relationship("TimeTracking", back_populates="Issues", backref=backref('TimeTracking', TimeTrackingId=Id))

		AggregateTimeEstimate = Column(Integer)

		ReporterId = Column(Integer, ForeignKey('TeamMembers.Id'))
		Reporter = relationship("TeamMembers", back_populates="Issues", backref=backref('TeamMembers', ReporterId=Id))
		CreatorId = Column(Integer, ForeignKey('TeamMembers.Id'))
		Creator = relationship("TeamMembers", back_populates="Issues", backref=backref('TeamMembers', CreatorId=Id))

		Summary = Column(String)

		AggregateProgressId = Column(Integer, ForeignKey('Progress.Id'))
		AggregateProgress = relationship("Progress", back_populates="Issues", backref=backref('Progress', AggregateProgressId=Id))

		DueDate = Column(DateTime)

		ProgressId = Column(Integer, ForeignKey('Progress.Id'))
		Progress = relationship("Progress", back_populates="Issues", backref=backref('Progress', ProgressId=Id))


		def __repr__(self):
				return "<Issue(Id='%d', Key='%s', IssueTypeId='%d' TimeSpent='%d', ProjectId='%d', AggregateTimeSpent='%d', \
												ResolutionId='%d', ResolutionDate='%f', WorkRatio='%d', Created='%f', PriorityId='%d', TimeEstimate='%d', \
												AggregateTimeOriginalEstimate='%d', AssigneeId='%d', Updated='%f', StatusId='%d', TimeOriginalEstimate='%d', \
												TimeTrackingId='%d', AggregateTimeEstimate='%d', ReporterId='%d', CreatorId='%d', Summary='%s', \
												AggregateProgressId='%d', DueDate='%f', ProgressId='%d'>" % (
										self.Id, self.Key, self.IssueTypeId, self.TimeSpent, self.ProjectId, self.AggregateTimeSpent,
										self.ResolutionId, self.ResolutionDate, self.WorkRatio, self.Created, self.PriorityId, self.TimeEstimate,
										self.AggregateTimeOriginalEstimate, self.AssigneeId, self.Updated, self.Status, self.TimeOriginalEstimate,
										self.TimeTrackingId, self.AggregateTimeEstimate, self.ReporterId, self.CreatorId, self.Summary,
										self.AggregateProgressId, self.DueDate, self.ProgressId) 