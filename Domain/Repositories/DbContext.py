import logging
from typing import List
from pydantic import BaseModel

import sqlalchemy as sql
from sqlalchemy import or_
from sqlalchemy import and_

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
from JiraChangeLog import JiraChangeLogItem

from Base import Base


class DbContext:
    __engine = None #sql db engine
    __sessionMaker = None
    __session = None

    def __init__(self, settings):
        logging.info("Initializing DbContext")
        logging.getLogger('sqlalchemy').setLevel(logging.ERROR)
        try:
            if settings.Debug:
                connectionString = settings.SqlDb["ConnectionStringServer"]
            else:
                connectionString = settings.SqlDb["ConnectionStringFile"]
            DbContext.__engine = sql.create_engine(connectionString, echo=settings.SqlDb["Debug"])
            Base.metadata.create_all(DbContext.__engine)
            sessionMaker = sql.orm.sessionmaker(bind=DbContext.__engine)
            DbContext.__session = sessionMaker()
        except Exception as e:
            logging.error("Exception occurred when creating DbContext", exc_info=True)
            return e

    def GetSession(self):
        return DbContext.__session

    def GetEngine(self):
        return DbContext.__engine

    def AddMultipleEntitiesToDb(self, entitiesList):
        try:
            DbContext.__session.add_all(entitiesList)
            DbContext.__session.commit()
        except Exception as e:
            logging.error("Exception occurred when adding multiple entities to DbContext", exc_info=True)

    def GetIssue(self, issueKey : str):
        queryResult = DbContext.__session.query(TIssue).filter_by(Key=issueKey).first()
        return queryResult

    def GetAllIssues(self, projectsList : List[str] = []) -> List[TIssue]:
        if not(projectsList):
            issues = DbContext.__session.query(TIssue).all()
            return issues
        else:
            issues = []
            for project in projectsList:
                query = self.Query(TProject, 'Key', project)
                if query:
                    project = query[0]
                    projectIssues = self.Query(TIssue, 'ProjectId', project.Id)
                    issues.extend(projectIssues)
            return issues

    def GetIssueChangeLogs(self, issueKey : str):
        queryResult = DbContext.__session.query(TChangeLog).filter(TChangeLog.IssueKey == issueKey).order_by("Created").all()
        return queryResult
        
    def Query(self, entity, attribute : str, query : str):
        if not(attribute):
            queryResult = DbContext.__session.query(entity).all()
            return queryResult
        else:
            queryResult = DbContext.__session.query(entity).filter(getattr(entity, attribute) == query).all()
            return queryResult

    def QueryChainOrLike(self, entity, attribute1: str, query11 : str, query12 : str, attribute2 : str, query2 : str):
        queryResult = DbContext.__session.query(entity)\
            .filter(or_(getattr(entity, attribute1) == query11, getattr(entity, attribute1) == query12))\
            .filter(getattr(entity, attribute2).like(query2)).all()
        return queryResult

    def QueryLike(self, entity, attribute : str, query : str):
        queryResult = DbContext.__session.query(entity).filter(getattr(entity, attribute).like(query)).all()
        return queryResult

    def QueryLikeAnd(self, entity, attribute1 : str, query1 : str, attribute2 : str, query2 : str):
        queryResult = DbContext.__session.query(entity).filter(and_(getattr(entity, attribute1).like(query1), getattr(entity, attribute2) == query2)).all()
        return queryResult

    def QueryOr(self, entity, attribute : str, query1 : str, query2 : str):
        queryResult = DbContext.__session.query(entity).filter(or_(getattr(entity, attribute) == query1, getattr(entity, attribute) == query2)).all()
        return queryResult

    def QueryAnd(self, entity, attribute : str, query1 : str, query2 : str):
        queryResult = DbContext.__session.query(entity).filter(and_(getattr(entity, attribute) == query1, getattr(entity, attribute) == query2)).all()
        return queryResult

    def AddIssueToDb(self, jiraIssue : JiraIssue):
        logging.info("Adding jiraIssue "+ jiraIssue.key+ " to the database.")
        if self.GetIssue(jiraIssue.key):
            logging.error("Tried to add jiraIssue that already exists with key "+ jiraIssue.key+ "and Id "+jiraIssue.id)
            return None
        issue = self.__AddEntityToDb(TIssue(jiraIssue))
        issue = self.__AddAttributeWithIdToEntity(issue, TIssueType, jiraIssue.issuetype, 'IssueType', 'Id')
        if jiraIssue.priority:
            issue = self.__AddAttributeWithIdToEntity(issue, TPriority, jiraIssue.priority, 'Priority', 'Id')
        issue = self.__AddAttributeWithIdToEntity(issue, TStatus, jiraIssue.status, 'Status', 'Id')
        issue = self.__AddAttributeWithIdToEntity(issue, TProject, jiraIssue.project, 'Project', 'Id')
        if jiraIssue.resolution.id:
            issue = self.__AddAttributeWithIdToEntity(issue, TResolution, jiraIssue.resolution, 'Resolution', 'Id')
        issue = self.__AddAttributeWithIdToEntity(issue, TTeamMember, jiraIssue.reporter, 'Reporter', 'Key')
        issue = self.__AddAttributeWithIdToEntity(issue, TTeamMember, jiraIssue.assignee, 'Assignee', 'Key')
        issue = self.__AddAttributeWithIdToEntity(issue, TTeamMember, jiraIssue.creator, 'Creator', 'Key')
        if jiraIssue.aggregateprogress:
            issue = self.__AddAttributeWithoutIdToIssue(issue, TProgress, jiraIssue.aggregateprogress, 'AggregateProgress')
        if jiraIssue.progress:
            issue = self.__AddAttributeWithoutIdToIssue(issue, TProgress, jiraIssue.progress, 'Progress')
        if jiraIssue.timetracking:
            issue = self.__AddAttributeWithoutIdToIssue(issue, TTimeTracking, jiraIssue.timetracking, 'TimeTracking')
        if jiraIssue.worklogs:
            for workLog in jiraIssue.worklogs:
                logItem = self.__AddEntityToDb(TWorkLog(workLog))
                logItem = self.__AddAttributeWithIdToEntity(logItem, TTeamMember, workLog.author, 'Author', 'Key')
                logItem = self.__AddAttributeWithIdToEntity(logItem, TTeamMember, workLog.updateAuthor, 'UpdateAuthor', 'Key')
        #TODO: this could become a problem... setting the changelogid = jiraIssue.Id * 1000000
        initialChangelog = JiraChangeLogItem(None, str(int(jiraIssue.id)*-1), jiraIssue.creator, jiraIssue.created, jiraIssue.id, jiraIssue.key)
        initialChangeLogItem = self.__AddEntityToDb(TChangeLog(initialChangelog))
        initialChangeLogItem = self.__AddAttributeWithIdToEntity(initialChangeLogItem, TTeamMember, initialChangelog.author, 'Author', 'Key')
        for changeLog in jiraIssue.changelog.logs:
            logItem = self.__AddEntityToDb(TChangeLog(changeLog))
            logItem = self.__AddAttributeWithIdToEntity(logItem, TTeamMember, changeLog.author, 'Author', 'Key')
        return issue

    def UpdateEntity(self, entity):
        try:
            DbContext.__session.commit()
            DbContext.__session.refresh(entity)
            return entity
        except Exception as e:
            logging.error(f"Exception occurred when updating entity in database. Entity was {entity}", exc_info=True)

    def __AddEntityToDb(self, entity):
        try:
            DbContext.__session.add(entity)
            DbContext.__session.commit()
            DbContext.__session.refresh(entity)
            return entity
        except Exception as e:
            logging.error("Exception occurred when adding entity to database.", exc_info=True)

    def __AddAttributeWithoutIdToIssue(self, issue : TIssue, entityType, jiraEntity, entityTypeAttribute : str):
        entity = self.__AddEntityToDb(entityType(jiraEntity, issue.Id))
        setattr(issue, entityTypeAttribute+'Id', entity.Id)
        return self.UpdateEntity(issue)

    def __AddAttributeWithIdToEntity(self, entity, SubEntityType, jiraEntity, 
                              subEntityTypeAttribute : str, identityAttribute : str):
        subEntity =  DbContext.__session.query(SubEntityType).filter(
                getattr(SubEntityType, identityAttribute)==getattr(jiraEntity, identityAttribute.lower())).first()
        if subEntity == None:
            subEntity = SubEntityType(jiraEntity)
            subEntity = self.__AddEntityToDb(subEntity)
        setattr(entity, subEntityTypeAttribute+'Id', getattr(subEntity, identityAttribute))
        return self.UpdateEntity(entity)