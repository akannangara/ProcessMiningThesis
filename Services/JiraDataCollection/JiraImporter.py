from Support.JiraConnectionModel import JiraConnectionModel
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