class JiraStatus:
    id = "" #string value
    name = "" #string value
    description = "" #string value

    def __init__(self, jiraStatus):
        self.id = jiraStatus.id
        self.name = jiraStatus.name
        self.description = jiraStatus.description