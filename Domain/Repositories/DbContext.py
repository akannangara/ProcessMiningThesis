import logging
from typing import List
from pydantic import BaseModel

import sqlalchemy as sql


#from DbChangeLog import DbChangeLog
from TIssueType import TIssueType
from TProject import TProject
#from TResolution import TResolution
#from TPriority import TPriority
#from TTeamMember import TTeamMember
#from TStatus import TStatus
#from TTimeTracking import TTimeTracking
#from TProgress import TProgress

#from DbProgress import DbProgress
#from DbResolution import DbResolution
#from DbStatus import DbStatus
#from DbTimeTracking import DbTimeTracking
#from DbWorkLog import DbWorkLog
from TIssue import TIssue


from Base import Base


class DbContext:
    __engine = None #sql db engine
    __sessionMaker = None

    def __init__(self, settings):
        logging.info("Initializing DbContext")
        try:
            connectionString = settings.SqlDb["ConnectionString"]
            DbContext.__engine = sql.create_engine(connectionString, echo=True)
            Base.metadata.create_all(DbContext.__engine)
            DbContext.__sessionMaker = sql.orm.sessionmaker(bind=DbContext.__engine)
        except Exception as e:
            logging.error("Exception occurred when creating DbContext", exc_info=True)
            return e

    def AddMultipleToDb(self, entitiesList):
        session = DbContext.__sessionMaker()
        session.add_all(entitiesList)
        session.commit()

    def AddToDb(self, entity):
        session = DbContext.__sessionMaker()
        session.add(entity)
        session.commit()

    def GetIssue(self, issueKey):
        session = DbContext.__sessionMaker()
        queryResult = session.query(DbIssue).filter_by(Key=issueKey).first()
        return queryResult

    def GetDatabase(self):
        x = DbProjects.__table__

        newProject = DbProjects(Id=1, Key='projectKey', Name='projectName', ProjectTypeKey='project type key')
        session = DbContext.__sessionMaker()
        session.add(newProject)
        session.commit()