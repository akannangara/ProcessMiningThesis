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

db=DbContext(settings)