from JiraIssueType import JiraIssueType
from JiraProject import JiraProject
from JiraResolution import JiraResolution
from JiraPriority import JiraPriority
from JiraTeamMember import JiraTeamMember
from JiraStatus import JiraStatus
from JiraTimeTracking import JiraTimeTracking
from JiraProgress import JiraProgress
from JiraWorkLogItem import JiraWorkLogItem
from JiraChangeLogItem import JiraChangeLogItem

@auto_attr_check
class JiraIssue:
		id : str
		key : str
		issuetype : JiraIssueType
		timespent : int
		project : JiraProject
		aggregatetimespent : int
		resolution : JiraResolution
		resolutiondate: str #datetime
		workratio : float
		created : str #datetime
		priority : JiraPriority
		timeestimate : int
		aggregatetimeoriginalestimate : int
		assignee : JiraTeamMember
		updated : str #datetime
		status : JiraStatue
		timeoriginalestimate : int
		timetracking : JiraTimeTracking
		aggregatetimeestimate : int
		reporter : JiraTeamMember
		creator : JiraTeamMember
		summary : str
		aggregateprogress : JiraProgress
		duedate: str #date
		progress : JiraProgress
		worklog : [] #collection of JiraWorkLogs
		changelog : [] #collection of JiraChangeLogs