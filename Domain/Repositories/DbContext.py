﻿import logging
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

    def AddMultipleToDb(self, entitiesList):
        #session = DbContext.__sessionMaker()
        DbContext.__session.add_all(entitiesList)
        DbContext.__session.commit()

    def AddToDb(self, entity):
        #session = DbContext.__sessionMaker()
        DbContext.__session.add(entity)
        DbContext.__session.commit()
        DbContext.__session.refresh(entity)
        return entity
    
    def UpdateEntity(self, entity):
        #session = DbContext.__sessionMaker()
        DbContext.__session.commit()
        DbContext.__session.refresh(entity)
        return entity

    def AddIssueToDb(self, jiraIssue : JiraIssue):
        issue = self.AddToDb(TIssue(jiraIssue))

        #add IssueType
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
        entity = self.AddToDb(entityType(jiraEntity, issue.Id))
        setattr(issue, entityTypeAttribute+'Id', entity.Id)
        return self.UpdateEntity(issue)

    def __AddAttributeWithIdToIssue(self, issue : TIssue, entityType, jiraEntity, 
                              entityTypeAttribute : str, identityAttribute : str):
        entity =  DbContext.__session.query(entityType).filter(
                getattr(entityType, identityAttribute)==getattr(jiraEntity, identityAttribute.lower())).first()
        if entity == None:
            entity = entityType(jiraEntity)
            entity = self.AddToDb(entity)
        setattr(issue, entityTypeAttribute+identityAttribute, getattr(entity, identityAttribute))
        return self.UpdateEntity(issue)


    def __AddIssueTypeToIssue(self, jiraIssueType, issue : TIssue):
        #session = DbContext.__sessionMaker()
        issueType = DbContext.__session.query(TIssueType).filter_by(Id=jiraIssueType.id).first()
        if issueType == None:
            entity = TIssueType(jiraIssueType)
            issueType = self.AddToDb(entity)
        issue.IssueTypeId = issueType.Id
        return self.UpdateEntity(issue)

    def __AddPriorityToIssue(self, jiraPriority, issue : TIssue):
        priority = DbContext.__session.query(TPriority).filter_by(Id=jiraPriority.id).first()
        if priority == None:
            entity = TPriority(jiraPriority)
            priority = self.AddToDb(entity)
        issue.PriorityId = priority.Id
        return self.UpdateEntity(issue)

    def __AddStatusToIssue(self, jiraStatus, issue : TIssue):
        status = DbContext.__session.query(TStatus).filter_by(Id=jiraStatus.id).first()
        if priority == None:
            entity = TStatus(jiraStatus)
            status = self.AddToDb(entity)
        issue.StatusId = status.Id
        return self.UpdateEntity(issue)

    def __AddProjectToIssue(self, jiraProject, issue : TIssue):
        project = DbContext.__session.query(TProject).filter_by(Id=jiraProject.id).first()
        if priority == None:
            entity = TStatus(jiraStatus)
            project = self.AddToDb(entity)
        issue.ProjectId = project.Id
        return self.UpdateEntity(issue)

    

    def GetIssue(self, issueKey):
        #session = DbContext.__sessionMaker()
        queryResult = DbContext.__session.query(TIssue).filter_by(Key=issueKey).first()
        return queryResult

    def EntityExists(self, entityType, idValue : str):
        #session = DbContext.__sessionMaker()
        query = DbContext.__session.query(entityType).filter_by(Id=idValue).first()
        if query == None:
            return False
        return True