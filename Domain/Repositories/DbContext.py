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
from TWorkLog import TWorkLog
from TChangeLog import TChangeLog

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
            logging.error("Exception occurred when adding entity to database.", exc_info=True)
    
    def UpdateEntity(self, entity):
        try:
            DbContext.__session.commit()
            DbContext.__session.refresh(entity)
            return entity
        except Exception as e:
            logging.error("Exception occurred when updating entity in database. Entity was {entity}", exc_info=True)

    def AddIssueToDb(self, jiraIssue : JiraIssue):
        issue = self.AddEntityToDb(TIssue(jiraIssue))
        issue = self.__AddAttributeWithIdToEntity(issue, TIssueType, jiraIssue.issuetype, 'IssueType', 'Id')
        issue = self.__AddAttributeWithIdToEntity(issue, TPriority, jiraIssue.priority, 'Priority', 'Id')
        issue = self.__AddAttributeWithIdToEntity(issue, TStatus, jiraIssue.status, 'Status', 'Id')
        issue = self.__AddAttributeWithIdToEntity(issue, TProject, jiraIssue.project, 'Project', 'Id')
        if jiraIssue.resolution.id:
            issue = self.__AddAttributeWithIdToEntity(issue, TResolution, jiraIssue.resolution, 'Resolution', 'Id')
        issue = self.__AddAttributeWithIdToEntity(issue, TTeamMember, jiraIssue.reporter, 'Reporter', 'Key')
        issue = self.__AddAttributeWithIdToEntity(issue, TTeamMember, jiraIssue.assignee, 'Assignee', 'Key')
        issue = self.__AddAttributeWithIdToEntity(issue, TTeamMember, jiraIssue.creator, 'Creator', 'Key')
        issue = self.__AddAttributeWithoutIdToIssue(issue, TProgress, jiraIssue.aggregateprogress, 'AggregateProgress')
        issue = self.__AddAttributeWithoutIdToIssue(issue, TProgress, jiraIssue.progress, 'Progress')
        if not(jiraIssue.timetracking == None):
            issue = self.__AddAttributeWithoutIdToIssue(issue, TTimeTracking, jiraIssue.timetracking, 'TimeTracking')
        if not(jiraIssue.worklogs == None):
            for workLog in jiraIssue.worklogs:
                logItem = self.AddEntityToDb(TWorkLog(workLog))
                logItem = self.__AddAttributeWithIdToEntity(logItem, TTeamMember, workLog.author, 'Author', 'Key')
                logItem = self.__AddAttributeWithIdToEntity(logItem, TTeamMember, workLog.updateAuthor, 'UpdateAuthor', 'Key')
        for changeLog in jiraIssue.changelog.logs:
            logItem = self.AddEntityToDb(TChangeLog(changeLog))
            logItem = self.__AddAttributeWithIdToEntity(logItem, TTeamMember, changeLog.author, 'Author', 'Key')


    def __AddAttributeWithoutIdToIssue(self, issue : TIssue, entityType, jiraEntity, entityTypeAttribute : str):
        entity = self.AddEntityToDb(entityType(jiraEntity, issue.Id))
        setattr(issue, entityTypeAttribute+'Id', entity.Id)
        return self.UpdateEntity(issue)

    def __AddAttributeWithIdToEntity(self, entity, SubEntityType, jiraEntity, 
                              subEntityTypeAttribute : str, identityAttribute : str):
        subEntity =  DbContext.__session.query(SubEntityType).filter(
                getattr(SubEntityType, identityAttribute)==getattr(jiraEntity, identityAttribute.lower())).first()
        if subEntity == None:
            subEntity = SubEntityType(jiraEntity)
            subEntity = self.AddEntityToDb(subEntity)
        setattr(entity, subEntityTypeAttribute+'Id', getattr(subEntity, identityAttribute))
        return self.UpdateEntity(entity)    

    def GetIssue(self, issueKey : str):
        queryResult = DbContext.__session.query(TIssue).filter_by(Key=issueKey).first()
        return queryResult