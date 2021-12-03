class JiraIssueType:
    id = "" #string value
    description = "" #string value
    name = "" #string value
    subtask = False #boolean value

    def __init__(self, jiraIssueType):
        self.id = jiraIssueType.id
        self.description = jiraIssueType.description
        self.name = jiraIssueType.name
        self.subtask = jiraIssueType.subtask