import logging
from typing import List
from pydantic import BaseModel

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from datetime import datetime

from Base import Base
from DateTimeConverter import DateTimeConverter

from JiraSprint import JiraSprint


class TSprint(Base):
		__tablename__ = 'Sprints'

		Id = Column(Integer, primary_key=True)
		Name = Column(String(255))
		StartDate = Column(DateTime)
		EndDate = Column(DateTime)
		Goal = Column(String)
		IssueCount = Column(Integer, nullable=True)
		SprintTimeEstimate = Column(Integer, nullable=True)

		def __init__(self, jiraSprint : JiraSprint):
				self.Id = jiraSprint.Id
				self.Name = jiraSprint.Name
				self.StartDate = DateTimeConverter.ConvertDatetime(jiraSprint.StartDate[:-5])
				self.EndDate = DateTimeConverter.ConvertDatetime(jiraSprint.EndDate[:-5])
				self.Goal = jiraSprint.Goal
				self.IssueCount = None
				self.SprintTimeEstimate = None