import logging
from typing import List
from pydantic import BaseModel

from sqlalchemy import Column, Integer, String, Boolean

from Base import Base

from JiraPriority import JiraPriority

class TPriority(Base):
		__tablename__ = 'Priorities'

		Id = Column(Integer, primary_key=True)
		Name = Column(String(255))

		def __repr__(self):
				return "<Priorities(Id='%d', Name='%s'>" % (
										self.Id, self.Name)

		def __init__(self, jiraPriority : JiraPriority):
				self.Id = jiraPriority.id
				self.Name = jiraPriority.name