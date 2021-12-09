class JiraProject:
    id = "" #string value
    key = "" #string value
    name = "" #string value
    projectTypeKey = "" #string value

    def __init__(self, jiraProject):
        self.id = jiraProject.id
        self.key = jiraProject.key
        self.name = jiraProject.name
        self.projectTypeKey = jiraProject.projectTypeKey