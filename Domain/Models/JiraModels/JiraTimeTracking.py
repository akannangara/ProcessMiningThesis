class JiraTimeTracking:
    originalEstimateSeconds = -999 #int value
    remainingEstimateSeconds = -999 #int value
    timeSpentSeconds = -999 #int value

    def __init__(self, jiraTimeTracking):
        self.originalEstimateSeconds = jiraTimeTracking.originalEstimateSeconds
        self.remainingEstimateSeconds = jiraTimeTracking.remainingEstimateSeconds
        self.timeSpentSeconds = jiraTimeTracking.timeSpentSeconds