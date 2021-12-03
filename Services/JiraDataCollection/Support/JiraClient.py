import sys
import os
import logging
import time

from jira import JIRA

from Common.Support import JiraConnectionModel

class JiraClient:
    
    __jiraConnectRefreshTimer = 600 #default 10 minutes
    __jiraConnectionTime = time.time() - time.time()
    __jiraConnectTime = 0
    __connectionSettings = None
    __client = None

    def __init__(self, JiraConnectionSettings : JiraConnectionModel):
        JiraClient.__connectionSettings = JiraConnectionSettings
        if (JiraClient.__connectionSettings.ConnectionRefreshTimer > 0):
            JiraClient.__jiraConnectRefreshTimer = JiraConnectionSettings.ConnectionRefreshTimer

    def GetIssue(self, jiraIssueId : str):
        self.__ConnectToJira()
        logging.info("Importing issue {issueId} from Jira".format(issueId=jiraIssueId))
        try:
            issue = JiraClient.__client.issue(jiraIssueId, expand='changelog')
            return issue
        except Exception as e:
            logging.error("Exception occurred when importing from Jira", exc_info=True)

    def GetProjectIssues(self, jiraProjectName : str):
        self.__ConnectToJira()
        logging.debug("Importing all issues of project {projectName} from Jira".format(projectName=jiraProjectName))
        try:
            projectIssues = JiraClient.__client.search_issues(jql_str='project='+jiraProjectName, maxResults=False, expand='changelog')
            return projectIssues
        except Exception as e:
            logging.error("Exception occurred when importing project issues Jira", exc_info=True)

    def GetProjects(self):
        self.__ConnectToJira()
        logging.info("Importing all projects from Jira")
        try:
            projects = JiraClient.__client.projects()
            return projects
        except Exception as e:
            logging.error("Exception occurred when importing all projects from Jira", exc_info=True)

    def __ConnectToJira(self):
        if (time.time() - JiraClient.__jiraConnectionTime) > JiraClient.__jiraConnectRefreshTimer:
            try:
                JiraClient.__client = JIRA(JiraClient.__connectionSettings.Servername,
                                       basic_auth=(JiraClient.__connectionSettings.Username, JiraClient.__connectionSettings.Password))
                JiraClient.__jiraConnectionTime = time.time()
            except Exception as e:
                logging.error("Exception occurred when trying to connect to jira", exc_info=True)