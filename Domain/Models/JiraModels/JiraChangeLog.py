from JiraTeamMember import JiraTeamMember

class JiraChangeLog:
    logs = []

    def __init__(self, jiraChangeLog):
        for x in jiraChangeLog.histories:
            self.logs.extend(JiraChangeLogHistories(x).logs)

class JiraChangeLogHistories:
    logs = []

    def __init__(self, changeLogsHistories):
        for x in changeLogsHistories.items:
            self.logs.append(
                JiraChangeLogItem(x, changeLogsHistories.id,
                            changeLogsHistories.author,
                            changeLogsHistories.created))

class JiraChangeLogItem:
    id = "" #string value
    author = None #JiraTeamMember
    created = "" #string value #dateTime
    field = "" #string value
    fieldtype = "" #string value
    fromString = "" #string value
    toString = "" #string value

    def __init__(self, changeLog, id, author, created):
        self.id = id
        self.author = author
        self.created = created
        self.field = changeLog.field
        self.fieldtype = changeLog.fieldtype
        self.fromString = changeLog.fromString
        self.toString = changeLog.toString