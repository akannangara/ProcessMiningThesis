from JiraTeamMember import JiraTeamMember

AcceptedActivities = ['status', 'timeestimate', 'timespent']

class JiraChangeLog:
    logs = []

    def __init__(self, jiraChangeLog, issueId : str, issueKey : str):
        self.logs = []
        for x in jiraChangeLog.histories:
            self.logs.extend(JiraChangeLogHistories(x, issueId, issueKey).logs)

class JiraChangeLogHistories:
    logs = []

    def __init__(self, changeLogsHistories, issueId : str, issueKey : str):
        self.logs = []
        for x in changeLogsHistories.items:
            #if (x.field in AcceptedActivities):
            self.logs.append(
                JiraChangeLogItem(x, changeLogsHistories.id,
                        changeLogsHistories.author,
                        changeLogsHistories.created,
                        issueId,
                        issueKey))

class JiraChangeLogItem:
    id = "" #string value
    author = None #JiraTeamMember
    created = "" #string value #dateTime
    field = "" #string value
    fieldtype = "" #string value
    fromString = "" #string value
    toString = "" #string value
    issueId = "" #string value
    issueKey = "" #string value

    def __init__(self, changeLog, id, author, created, issueId : str, issueKey : str):
        self.id = id
        self.author = author
        self.created = created
        if changeLog == None:
            self.field = 'status'
            self.fieldtype = 'jira'
            self.fromString = 'Create Card'
            self.toString = 'To Do'
        else:
            self.field = changeLog.field
            self.fieldtype = changeLog.fieldtype
            self.fromString = changeLog.fromString
            self.toString = changeLog.toString
        self.issueId = issueId
        self.issueKey = issueKey