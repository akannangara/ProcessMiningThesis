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
        JiraImporter.___settings = settings
        jiraConnectionSettings = JiraConnectionModel(settings.Jira["Servername"],
                                                 settings.Jira["Username"],
                                                 settings.Jira["Password"],
                                                 settings.Jira["ConnectionRefreshTimer"])

        JiraImporter.__client = JiraClient(jiraConnectionSettings)
        if not(dbContext==None):
            JiraImporter.__dbContext = dbContext

    def GetProjectsList(self):
        projects = JiraImporter.__client.GetProjects()
        projectKeys = [p.key for p in projects]
        return projects

    def GetIssue(self, issueId : str):
        jiraIssue = JiraImporter.__client.GetIssue(issueId)
        if jiraIssue == None:
            return
        issue = JiraIssue(jiraIssue)
        return issue

    def GetProjectIssues(self, projectKey : str):
        logging.info("Importing project issues for the project {projectKey} using JiraImporter")
        try:
            projectIssuesDictionary = {}
            projectIssuesList = []
            projectIssues = JiraImporter.__client.GetProjectIssues(projectKey)
            for issue in projectIssues:
                projectIssuesList.append(JiraIssue(issue))
            projectIssuesDictionary[projectKey] = projectIssuesList
            return projectIssuesDictionary
        except Exception as e:
            logging.error("Exception occurred with importing project {projectKey} issues in JiraImporter",
                          exc_info=True)

    def GetIssuesFromProjectsList(self, projectList : List[str]):
        logging.info("importing projects from projectsList {projectList}")
        try:
            issuesList = []
            for x in projectList.intersect(JiraImporter.GetProjectsList()):
                issuesList.extend(self.ImportProjectIssues(x))
            return issuesList
        except Exception as e:
            logging.error("Exception occurred when importing issues from projectsList {projectList}",
                          exc_info=True)

    def GetAllProjectIssues(self):
        logging.info("Importing all project issues using JiraImporter")
        try:
            allProjectIssuesDictionary = {}
            allProjects = JiraImporter.__client.GetProjects()
            allProjects = ["CONBR", "PSH"]
            for project in allProjects:
                allProjectIssuesDictionary = allProjectIssuesDictionary | self.ImportProjectIssues(project)
            return allProjectIssuesDictionary
        except Exception as e:
            logging.error("Exception occurred with imporing all project issues using JiraImporter",
                          exc_info=True)

    def StoreIssuesToDatabase(self, issuesList : List[JiraIssue]):
        for issue in issuesList:
            JiraDataImporter.__dbContext.AddIssueToDb(issue)