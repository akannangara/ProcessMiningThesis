class JiraResolution:
    id = "" #string value
    description = "" #string value
    name = "" #string value

    def __init__(self, jiraResolution):
        if (not(jiraResolution == None)):
            self.id = jiraResolution.id
            self.description = jiraResolution.description
            self.name = jiraResolution.name