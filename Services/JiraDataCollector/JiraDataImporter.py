import logging
from typing import List
from pydantic import BaseModel

from JiraConnectionModel import JiraConnectionModel
from Support.JiraClient import JiraClient
from JiraIssue import JiraIssue

from TIssue import TIssue
from DbContext import DbContext

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