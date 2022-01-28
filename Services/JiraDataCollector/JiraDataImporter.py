import logging
from typing import List
from pydantic import BaseModel

from JiraConnectionModel import JiraConnectionModel
from Support.JiraClient import JiraClient
from JiraIssue import JiraIssue
from JiraSprint import JiraSprint
from TChangeLog import TChangeLog

from sqlalchemy import and_, or_

from TIssue import TIssue
from TSprint import TSprint
from DbContext import DbContext
import datetime

class JiraDataImporter(BaseModel):
    __settings = None
    __client = None
    __dbContext = None

    def __init__(self, settings, dbContext : DbContext):
        JiraDataImporter.__settings = settings
        jiraConnectionSettings = JiraConnectionModel(settings.Jira["Servername"],
                                                 settings.Jira["Username"],
                                                 settings.Jira["Password"],
                                                 settings.Jira["ConnectionRefreshTimer"])

        JiraDataImporter.__client = JiraClient(jiraConnectionSettings)
        if not(dbContext==None):
            JiraDataImporter.__dbContext = dbContext

    def GetProjectsList(self):
        projects = JiraDataImporter.__client.GetProjects()
        projectKeys = [p.key for p in projects]
        return projectKeys

    def GetIssue(self, issueId : str):
        jiraIssue = JiraDataImporter.__client.GetIssue(issueId)
        if jiraIssue == None:
            return
        issue = JiraIssue(jiraIssue)
        return issue

    def GetBoards(self):
        boards = JiraDataImporter.__client.GetBoards()
        return boards

    def GetSprints(self):
        jiraSprints = JiraDataImporter.__client.GetSprints()
        sprints = []
        for s in jiraSprints:
            if s.name.startswith("CON"):
                sprints.append(JiraSprint(s))
        return sprints

    def GetProjectIssues(self, projectKey : str):
        logging.info("Importing project issues for the project "+projectKey+" using JiraImporter")
        try:
            projectIssuesList = []
            projectIssues = JiraDataImporter.__client.GetProjectIssues(projectKey)
            for issue in projectIssues:
                projectIssuesList.append(JiraIssue(issue))
            return projectIssuesList
        except Exception as e:
            logging.error("Exception occurred with importing project "+projectKey+" issues in JiraImporter",
                          exc_info=True)

    def GetIssuesFromProjectsList(self, projectList : List[str]):
        logging.info("importing projects from projectsList "+projectList)
        try:
            issuesList = []
            projects = set.intersection(set(projectList), set(self.GetProjectsList()))
            for x in projects:
                issuesList.extend(self.GetProjectIssues(x))
            return issuesList
        except Exception as e:
            logging.error("Exception occurred when importing issues from projectsList",
                          exc_info=True)

    def GetAllProjectIssues(self):
        logging.info("Importing all project issues using JiraImporter")
        try:
            allProjectIssues = []
            allProjects = JiraDataImporter.__client.GetProjects()
            for project in allProjects:
                allProjectIssues.append(self.GetProjectIssues(project))
            return allProjectIssues
        except Exception as e:
            logging.error("Exception occurred with imporing all project issues using JiraImporter",
                          exc_info=True)

    def StoreIssuesToDatabase(self, issuesList : List[JiraIssue]):
        for issue in issuesList:
            JiraDataImporter.__dbContext.AddIssueToDb(issue)

    def StoreSprintsToDatabase(self, sprintList : List[JiraSprint]):
        for sprint in sprintList:
            JiraDataImporter.__dbContext.AddSprintToDb(sprint)

    def EnhanceSprintData(self):
        logging.info("Enhancing sprint data")
        try:
            db = JiraDataImporter.__dbContext
            sprints = db.Query(TSprint, "", "")
            distinctIssueKeys = []
            for sprint in sprints:
                if sprint.StartDate < datetime.datetime(2020, 7, 13, 0, 0):
                    continue
                if sprint.StartDate > datetime.datetime.now():
                    break
                logging.info(f"Enhancing sprint data for {sprint.Name}")
                sprintIssueKeys = []
                ThisSprintChangeLogs = db.GetSession().query(TChangeLog).filter(and_(TChangeLog.Created >= sprint.StartDate, TChangeLog.Created < sprint.EndDate)).distinct(TChangeLog.IssueKey).all()
                sprintIssueKeys.extend([r.IssueKey for r in ThisSprintChangeLogs])
                #fromSprintChangeLogsIssues
                sprintIssueKeys.extend([r.IssueKey for r in db.GetSession().query(TChangeLog).filter(and_(TChangeLog.Field=='Sprint', and_(TChangeLog.ToString.like("%{}%".format(sprint.Name)), TChangeLog.Created < sprint.EndDate))).all()])
                allIssuesBeforeSprint = set([r.IssueKey for r in db.GetSession().query(TChangeLog).filter(and_(TChangeLog.Created < sprint.StartDate, TChangeLog.ToString=='To Do')).all()])
                for potIssue in allIssuesBeforeSprint:
                    if not(db.GetSession().query(TChangeLog).filter(and_(TChangeLog.Created < sprint.StartDate, and_(TChangeLog.IssueKey == potIssue,\
                        or_(TChangeLog.ToString == 'Done', TChangeLog.ToString=='Rejected')))).all()):
                        sprintIssueKeys.append(potIssue)
                sprintIssueKeys = set(sprintIssueKeys)
                sprint.IssueCount = len(sprintIssueKeys)

                sumSprintTimeEstimate = 0
                for key in sprintIssueKeys:
                    keySprintTimeEstimate = 0
                    keyTimeEstimateChangeLog = db.GetSession().query(TChangeLog).order_by(TChangeLog.Created.asc()).filter(\
                            and_(and_(TChangeLog.IssueKey == key, TChangeLog.Field=='timeestimate'),\
                            and_(TChangeLog.Created > sprint.StartDate, TChangeLog.Created < sprint.EndDate))\
                            ).all()
                    if keyTimeEstimateChangeLog:
                        if keyTimeEstimateChangeLog[0].FromString:
                            keySprintTimeEstimate = int(keyTimeEstimateChangeLog[0].FromString)
                    else:
                        keyTimeEstimateChangeLog = db.GetSession().query(TChangeLog).order_by(TChangeLog.Created.desc()).filter(\
                            and_(and_(TChangeLog.IssueKey == key, TChangeLog.Field=='timeestimate'),
                                 TChangeLog.Created < sprint.StartDate))\
                                     .all()
                        if keyTimeEstimateChangeLog:
                            if keyTimeEstimateChangeLog[0].ToString:
                                keySprintTimeEstimate = int(keyTimeEstimateChangeLog[0].ToString)
                    if keySprintTimeEstimate == 0:
                        issueOriginalTimeEstimate = db.Query(TIssue, "Key", key)[0].TimeOriginalEstimate
                        if issueOriginalTimeEstimate:
                            keySprintTimeEstimate = issueOriginalTimeEstimate
                    sumSprintTimeEstimate += keySprintTimeEstimate
                sprint.SprintTimeEstimate = sumSprintTimeEstimate
                db.UpdateEntity(sprint)
        except Exception as e:
            logging.error("Error occurred while enhancing sprint data", exc_info=True)