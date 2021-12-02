from JiraTeamMember import JiraTeamMember

class JiraWorkLogItem:
    author : JiraTeamMember
    updateAuthor : JiraTeamMember
    created : str #datetime
    updated : str #datetime
    started : str #datetime
    timeSpentSeconds : int
    id : str
    issueId : str