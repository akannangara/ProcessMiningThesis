import logging
from typing import List
from pydantic import BaseModel

import sqlalchemy as sql

from TIssue import TIssue

from JiraIssue import JiraIssue
from TIssueType import TIssueType
from TProject import TProject
from TResolution import TResolution
from TPriority import TPriority
from TTeamMember import TTeamMember
from TStatus import TStatus
from TTimeTracking import TTimeTracking
from TProgress import TProgress

from Base import Base


class DbContext:
    __engine = None #sql db engine
    __sessionMaker = None
    __session = None

    def __init__(self, settings):
        logging.info("Initializing DbContext")
        try:
            connectionString = settings.SqlDb["ConnectionString"]
            DbContext.__engine = sql.create_engine(connectionString, echo=True)
            Base.metadata.create_all(DbContext.__engine)
            sessionMaker = sql.orm.sessionmaker(bind=DbContext.__engine)
            DbContext.__session = sessionMaker()
        except Exception as e:
            logging.error("Exception occurred when creating DbContext", exc_info=True)
            return e

    def AddMultipleEntitiesToDb(self, entitiesList):
        try:
            DbContext.__session.add_all(entitiesList)
            DbContext.__session.commit()
        except Exception as e:
            logging.error("Exception occurred when adding multiple entities to DbContext", exc_info=True)

    def AddEntityToDb(self, entity):
        try:
            DbContext.__session.add(entity)
            DbContext.__session.commit()
            DbContext.__session.refresh(entity)
            return entity
        except Exception as e:
            logging.error("Exception occurred when adding entity to database. Entity was {entity}", exc_info=True)
    
    def UpdateEntity(self, entity):
        try:
            DbContext.__session.commit()
            DbContext.__session.refresh(entity)
            return entity
        except Exception as e:
            logging.error("Exception occurred when updating entity in database. Entity was {entity}", exc_info=True)

    def AddIssueToDb(self, jiraIssue : JiraIssue):
        issue = self.AddEntityToDb(TIssue(jiraIssue))
        issue = self.__AddAttributeWithIdToIssue(issue, TIssueType, jiraIssue.issuetype, 'IssueType', 'Id')
        issue = self.__AddAttributeWithIdToIssue(issue, TPriority, jiraIssue.priority, 'Priority', 'Id')
        issue = self.__AddAttributeWithIdToIssue(issue, TStatus, jiraIssue.status, 'Status', 'Id')
        issue = self.__AddAttributeWithIdToIssue(issue, TProject, jiraIssue.project, 'Project', 'Id')
        if jiraIssue.resolution.id:
            issue = self.__AddAttributeWithIdToIssue(issue, TResolution, jiraIssue.resolution, 'Resolution', 'Id')
        issue = self.__AddAttributeWithIdToIssue(issue, TTeamMember, jiraIssue.reporter, 'Reporter', 'Key')
        issue = self.__AddAttributeWithIdToIssue(issue, TTeamMember, jiraIssue.assignee, 'Assignee', 'Key')
        issue = self.__AddAttributeWithIdToIssue(issue, TTeamMember, jiraIssue.creator, 'Creator', 'Key')
        issue = self.__AddAttributeWithoutIdToIssue(issue, TProgress, jiraIssue.aggregateprogress, 'AggregateProgress')
        issue = self.__AddAttributeWithoutIdToIssue(issue, TProgress, jiraIssue.progress, 'Progress')
        issue = self.__AddAttributeWithoutIdToIssue(issue, TTimeTracking, jiraIssue.timetracking, 'TimeTracking')

    def __AddAttributeWithoutIdToIssue(self, issue : TIssue, entityType, jiraEntity, entityTypeAttribute : str):
        entity = self.AddEntityToDb(entityType(jiraEntity, issue.Id))
        setattr(issue, entityTypeAttribute+'Id', entity.Id)
        return self.UpdateEntity(issue)

    def __AddAttributeWithIdToIssue(self, issue : TIssue, entityType, jiraEntity, 
                              entityTypeAttribute : str, identityAttribute : str):
        entity =  DbContext.__session.query(entityType).filter(
                getattr(entityType, identityAttribute)==getattr(jiraEntity, identityAttribute.lower())).first()
        if entity == None:
            entity = entityType(jiraEntity)
            entity = self.AddEntityToDb(entity)
        setattr(issue, entityTypeAttribute+'Id', getattr(entity, identityAttribute))
        return self.UpdateEntity(issue)    

    def GetIssue(self, issueKey : str):
        queryResult = DbContext.__session.query(TIssue).filter_by(Key=issueKey).first()
        return queryResult