import logging

from JiraConnectionModel import JiraConnectionModel
from JiraDataCollection.Support.JiraClient import JiraClient
from JiraIssue import JiraIssue

class JiraImporter:
    __settings = None
    __client = None

    def __init__(self, settings):
        JiraImporter.___settings = settings
        jiraConnectionSettings = JiraConnectionModel(settings.Jira["Servername"],
                                                 settings.Jira["Username"],
                                                 settings.Jira["Password"],
                                                 settings.Jira["ConnectionRefreshTimer"])

        JiraImporter.__client = JiraClient(jiraConnectionSettings)

    def ImportIssue(self, issueId : str):
        jiraIssue = JiraImporter.__client.GetIssue(issueId)
        issue = JiraIssue(jiraIssue)

    def ImportProjectIssues(self, projectKey):
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

    def ImportIssuesFromProjectsList(self, projectList):
        logging.info("importing projects from projectsList {projectList}")
        try:
            issuesList = []
            for x in projectList.intersect(JiraImporter.__client.GetProjects()):
                issuesList.extend(self.ImportProjectIssues(x))
            return issuesList
        except Exception as e:
            logging.error("Exception occurred when importing issues from projectsList {projectList}",
                          exc_info=True)

    def ImportAllProjectIssues(self):
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

