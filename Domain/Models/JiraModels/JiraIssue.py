﻿from JiraIssueType import JiraIssueType
from JiraProject import JiraProject
from JiraResolution import JiraResolution
from JiraPriority import JiraPriority
from JiraTeamMember import JiraTeamMember
from JiraStatus import JiraStatus
from JiraTimeTracking import JiraTimeTracking
from JiraProgress import JiraProgress
from JiraWorkLog import JiraWorkLog
from JiraChangeLog import JiraChangeLog

class JiraIssue:
		id = "" #string value
		key = "" #string value
		issuetype = None #JiraIssueType
		timespent = -999 #int value
		project = None #JiraProject
		aggregatetimespent = -999 #int value
		resolution = None #JiraResolution
		resolutiondate= "" #string value #datetime
		workratio = -999.9
		created = "" #string value #datetime
		priority = None #JiraPriority
		timeestimate = -999 #int value
		aggregatetimeoriginalestimate = -999 #int value
		assignee = None #JiraTeamMember
		updated = "" #string value #datetime
		status = None #JiraStatus
		timeoriginalestimate = -999 #int value
		timetracking = None #JiraTimeTracking
		aggregatetimeestimate = -999 #int value
		reporter = None #JiraTeamMember
		creator = None #JiraTeamMember
		summary = "" #string value
		aggregateprogress = None #JiraProgress
		duedate= "" #string value #date
		progress = None #JiraProgress
		worklogs = None #[] #collection of JiraWorkLogs
		changelog = None #[] #collection of JiraChangeLogs

		def __init__(self, jiraIssue):
				self.id = jiraIssue.id
				self.key = jiraIssue.key
				self.issuetype = JiraIssueType(jiraIssue.fields.issuetype)
				self.timetimespent = jiraIssue.fields.timespent
				self.project = JiraProject(jiraIssue.fields.project)
				self.aggregatetimespent = jiraIssue.fields.aggregatetimespent
				self.resolution = JiraResolution(jiraIssue.fields.resolution)
				self.resolutiondate= jiraIssue.fields.resolutiondate
				self.workratio = jiraIssue.fields.workratio
				self.created = jiraIssue.fields.created
				self.priority = JiraPriority(jiraIssue.fields.priority)
				self.timeestimate = jiraIssue.fields.timeestimate
				self.aggregatetimeoriginalestimate = jiraIssue.fields.aggregatetimeoriginalestimate
				self.assignee = JiraTeamMember(jiraIssue.fields.assignee)
				self.updated = jiraIssue.fields.updated
				self.status = JiraStatus(jiraIssue.fields.status)
				self.timeoriginalestimate = jiraIssue.fields.timeoriginalestimate
				self.timetracking = JiraTimeTracking(jiraIssue.fields.timetracking)
				self.aggregatetimeestimate = jiraIssue.fields.aggregatetimeestimate
				self.reporter = JiraTeamMember(jiraIssue.fields.reporter)
				self.creator = JiraTeamMember(jiraIssue.fields.creator)
				self.summary = jiraIssue.fields.summary
				self.aggregateprogress = JiraProgress(jiraIssue.fields.aggregateprogress)
				self.duedate= jiraIssue.fields.duedate
				self.progress = JiraProgress(jiraIssue.fields.progress)
				self.worklogs = JiraWorkLog(jiraIssue.fields.worklog)
				self.changelog = JiraChangeLog(jiraIssue.changelog
																	 )