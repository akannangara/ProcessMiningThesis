class JiraTeamMember:
    key = "" #string value
    name = "" #string value
    displayName = "" #string value
    active = False #boolean value

    def __init__(self, jiraTeamMember):
        if jiraTeamMember:
            self.key = jiraTeamMember.key
            self.name = jiraTeamMember.name
            self.displayName = jiraTeamMember.displayName
            self.active = jiraTeamMember.active