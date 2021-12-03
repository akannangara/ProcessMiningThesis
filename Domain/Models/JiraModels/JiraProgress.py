class JiraProgress:
    progress = -999 #int value
    total = -999 #int value
    percent = -999 #int value

    def __init__(self, jiraProgress):
        self.progress = jiraProgress.progress
        self.total = jiraProgress.total
        self.percent = jiraProgress.percent