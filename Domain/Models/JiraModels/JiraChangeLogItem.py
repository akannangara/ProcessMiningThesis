from JiraTeamMember import JiraTeamMember

class JiraChangeLogItem:
    id : str
    author : JiraTeamMember
    created : str #dateTime
    field : str
    fieldtype : str
    fromString : str
    toString : str