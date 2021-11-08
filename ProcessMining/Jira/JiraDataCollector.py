import JiraConfig as cfg
from jira import JIRA


class JiraDataCollector:
    def __init__(self):
        if cfg.debug:
            servername = input("Please enter server name: ")
            username = input("Please enter username: ")
            password = input("Please enter Password")
        else:
            servername = cfg.Jira['ServerName']
            username = cfg.Jira['Username']
            password = cfg.Jira['Password']
        self.client = JIRA(servername, basic_auth=(username, password))

    def test(self):
        self.projects = self.collectProjects()
        self.issue = self.collectIssue('CONBR-76')
        self.issue2 = self.collectProjectIssues('CONBR')
        x = 0
        

    def collectIssue(self, issue):
        return self.client.issue(issue, expand='changelog')

    def collectProjectIssues(self, project):
        return self.client.search_issues(jql_str='project='+project, maxResults=False, expand='changelog')

    def collectProjects(self, **kwargs):
        if 'projectId' in kwargs:
            if type(kwargs['projectId']) == list:
                projects = []
                for pId in kwargs['projectId']:
                    projects.append(self.collectProjects(pId))
                return projects
            return self.client.project(kwargs['projectId'], expand='issue')
        else:
            return self.client.projects()