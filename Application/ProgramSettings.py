Jira = {
    "Servername": "https://jira.indicia.nl",
    "Username": "aaron.kannangara",
    "Password": "Hartje1962",
    "ConnectionRefreshTimer": 600
}

Debug=False #todo server: set to false

DataStoreFolder = "C:\_thesis\DataStore"

GraphVizLocation = "C:\Program Files\Graphviz\bin"

ImageStorage = {
    "ImagesSinkProcessDiscovery":"ProcessDiscoveryImages",
    "alphaMiner":"Alphaminer.png",
    "alphaPlusMiner": "AlphaPlusMiner.png",
    "inductiveMiner":"InductiveMiner.png",
    "desiredInductiveMiner":"DesiredInductiveMiner.png",
    "heuristicsMiner":"HeuristicsMiner.png",
    "heuristicsNetMiner":"HeuristicsNetMiner.png",
    "processTreeInductive": "ProcessTreeInductive.png",
    "dfg":"DFG.png",
    "ImagesSinkProcessConformance":"ProcessConformanceImages",
    "4d_heuristicsPlot": "4d_heuristicsPlot.png"
}

SqlDb = {
    "ConnectionString": 'mssql+pyodbc://DESKTOP-3L76FTS/processMiningThesis?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server',
    "ConnectionStringServer": 'mssql+pyodbc://DESKTOP-3L76FTS/processMiningThesis?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server',
    "ConnectionStringFile": "sqlite:///Database.db",
    "Debug": False
}

CsvStorageManager = {
    "SinkDirectory":"CsvCollection",
    "EventLogFileName": "Eventlog.csv",
    "OnlyDoneEventLogFileName": "OnlyDoneEventLog.csv",
    "TeamMembersFileName": "TeamMembers.csv",
    "StatusesFileName":"Statuses.csv",
    "MinerConformanceEvaluation": "MinerConformanceEvaluation.csv",
    "MultiDimensionalHeuristicConformanceEvaluation":"4dHeuristicsConfromanceEvaluation.csv",
    "DesiredEventLogFileName": "DesiredWorkflowEventLog.csv",
    "mlDataSet":"MLDataSet.csv"
}

GaussianProcess = {
    "acq_func" : "EI",
    "n_calls" : 100,
    "n_initial_points": 10,
    "noise": "gaussian"
}

GraphViz = {
    "binLocation": "C:\Program Files\Graphviz\\bin",
    "exeLocation": "C:\Program Files\Graphviz\\bin\dot.exe"
}

StatusIntDictionary = {
    "Reserved": 0,
    "Backlog": 0,
    "Pre-Refinement": 1,
    "Refinement": 2,
    "To Do": 3,
    "In Progress": 4,
    "Ready to Review": 5,
    "In Review": 6,
    "Ready to Deploy to Test": 7,
    "Ready to Test": 8,
    "In Test": 9,
    "Ready for Acceptance": 10,
    "Ready to Deploy to Acceptance": 11,
    "Ready for Acceptance": 12,
    "In Acceptance": 13,
    "Ready to Deploy to Production": 14,
    "Done": 15,
    "Rejected": 15
}

PriorityIntDictionary = {
    "Highest": 1,
    "High": 2,
    "Medium": 3,
    "Low": 4,
    "Lowest": 5
}

CompletedStatusIds = [10001, 10003]