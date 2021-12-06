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

		Field = Column(String(225))
		FieldType = Column(String(255))
		FromString = Column(String)
		ToString = Column(String)

		IssueId = Column(Integer, ForeignKey('Issues.Id'))
		Issue = relationship("Issues", back_populates="ChangeLog")



		def __repr__(self):
				return "<ChangeLog(Id='%d', AuthorId='%d', Created='%f' Field='%s', FieldType='%s', FromString='%s', ToString='%s', IssueId='%d'>" % (
										self.Id, self.AuthorId, self.Created, self.Field, self.FieldType, self.FromString, self.ToString, self.IssueId) 