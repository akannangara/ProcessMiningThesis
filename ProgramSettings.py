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
    "n_calls" : 10,
    "n_initial_points": 10,
    "noise": "gaussian"
}

GraphViz = {
    "binLocation": "C:\Program Files\Graphviz\\bin",
    "exeLocation": "C:\Program Files\Graphviz\\bin\dot.exe"
}