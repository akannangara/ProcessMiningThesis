from JiraTeamMember import JiraTeamMember

class JiraWorkLog:
    logs = []

    def __init__(self, jiraWorkLogs):
        for x in jiraWorkLogs.worklogs:
            self.logs.append(JiraWorkLogItem(x))

class JiraWorkLogItem:
    author = None #JiraTeamMember
    updateAuthor = None #JiraTeamMember
    created = "" #string value #datetime
    updated = "" #string value #datetime
    started = "" #string value #datetime
    timeSpentSeconds = -999
    id = "" #string value
    issueId = "" #string value

    def __init__(self, jiraWorkLogItem):
        self.author = jiraWorkLogItem.author
        self.updateAuthor = jiraWorkLogItem.updateAuthor
        self.created = jiraWorkLogItem.created
        self.updated = jiraWorkLogItem.updated
        self.started = jiraWorkLogItem.started
        self.timeSpentSeconds = jiraWorkLogItem.timeSpentSeconds
        self.id = jiraWorkLogItem.id
        self.issueId = jiraWorkLogItem.issueId