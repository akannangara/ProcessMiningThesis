from JiraTeamMember import JiraTeamMember

AcceptedActivities = ['status']

class JiraChangeLog:
    logs = []

    def __init__(self, jiraChangeLog, issueId : str):
        self.logs = []
        for x in jiraChangeLog.histories:
            self.logs.extend(JiraChangeLogHistories(x, issueId).logs)

class JiraChangeLogHistories:
    logs = []

    def __init__(self, changeLogsHistories, issueId : str):
        self.logs = []
        for x in changeLogsHistories.items:
            if (x.field in AcceptedActivities):
                self.logs.append(
                    JiraChangeLogItem(x, changeLogsHistories.id,
                            changeLogsHistories.author,
                            changeLogsHistories.created,
                            issueId))

class JiraChangeLogItem:
    id = "" #string value
    author = None #JiraTeamMember
    created = "" #string value #dateTime
    field = "" #string value
    fieldtype = "" #string value
    fromString = "" #string value
    toString = "" #string value
    issueId = "" #string value

    def __init__(self, changeLog, id, author, created, issueId : str):
        self.id = id
        self.author = author
        self.created = created
        self.field = changeLog.field
        self.fieldtype = changeLog.fieldtype
        self.fromString = changeLog.fromString
        self.toString = changeLog.toString
        self.issueId = issueId