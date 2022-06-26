import ImportAllLocations

from DbContext import DbContext
from CsvFileManager import CsvFileManager
from MLPML import MLPML

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

def CreateNewMLRow():
    columns = "ProjectIssueNumber;Priority;TimeEstimate;CurrentStatus;TimeOriginalEstimate;DeltaDueCreate;TimeSpent;CalculatedWorkRatio;TimeSinceToDo;ComingBack;SizeSummary;SizeDescription;ChangeSinceCreation;ChangeSinceLastStatus;Story;Epic;Task;Bug;Incident;SubTask;CDeliveryManager;CProjectManager;CSeniorDeveloper;CMediorDeveloper;CJuniorDeveloper;CDesigner;CSystemAccount;CTester;CIntern;CClient;CUndefined;ADeliveryManager;AProjectManager;ASeniorDeveloper;AMediorDeveloper;AJuniorDeveloper;ADesigner;ASystemAccount;ATester;AIntern;AClient;AUndefined;RDeliveryManager;RProjectManager;RSeniorDeveloper;RMediorDeveloper;RJuniorDeveloper;RDesigner;RSystemAccount;RTester;RIntern;RClient;RUndefined;SprintChangeSinceCreation;SprintChangeSinceStatusChange;YearSprintNumber;SprintIssueCount;DeltaSprintIssueCount;SprintSumEstimatedTime;DeltaSumEstimatedTime"
    columns = columns.split(';')
    values = "1283.724992;3;2619.311733;3;11631.98643;31427566.13;2467.125014;46.37955937;977069.5602;0;7.720703926;25.76455017;0.383244473;0.383244473;0;0;1;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0;0.443458484;0.697811416;14.02572611;979.0979829;48.48682003;14727353.36;782819.0233"
    values = values.split(';')
    values_ = []
    for v in values:
        values_.append(int(float(v)))
    row = dict(zip(columns, values_))
    return row

def GetMLX_Y():
    fm = CsvFileManager(db, settings)
    ds = fm.ReadFileToDataFrame(settings.CsvStorageManager["mlDataSet"])
    columnsToDrop = ['df_index','Key', 'WorkRatio', 'Fitness', 'Rejected', 'NextState']
    X_full = ds.drop(columnsToDrop, axis='columns')
    Y_workRatio = ds['WorkRatio']
    Y_fitness = ds['Fitness']
    Y_rejected = ds['Rejected']
    Y_nextState = ds['NextState']
    return X_full, Y_workRatio, Y_fitness, Y_nextState


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