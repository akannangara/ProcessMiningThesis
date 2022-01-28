import ImportAllLocations

from DbContext import DbContext

import ProgramSettings as settings

from TIssue import TIssue
from TIssueType import TIssueType
from TProject import TProject
from TResolution import TResolution
from TPriority import TPriority
from TTeamMember import TTeamMember
from TStatus import TStatus
from TTimeTracking import TTimeTracking
from TProgress import TProgress
from TWorkLog import TWorkLog
from TChangeLog import TChangeLog
from TSprint import TSprint

db=DbContext(settings)

def ProjectIssueCountDictionary():
    projectIssueCount = {}
    for project in projects:
        projectIssueCount[project.Key] = len(db.Query(TIssue, "ProjectId", project.Id))
    return projectIssueCount

def TeamMemberTypeAndCount():
    teamMemberTypeAndCount = {}
    allTeamMembers = db.Query(TTeamMember,"","")
    for member in allTeamMembers:
        if not(member.Type in teamMemberTypeAndCount):
            teamMemberTypeAndCount[member.Type] = 1
        else:
            teamMemberTypeAndCount[member.Type] += 1
    return teamMemberTypeAndCount