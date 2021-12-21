Jira = {
    "Servername": "https://jira.indicia.nl",
    "Username": "aaron.kannangara",
    "Password": "Hartje1962",
    "ConnectionRefreshTimer": 600
}

Debug=True #todo server: set to false

DataStoreFolder = "C:\_thesis\DataStore"

GraphVizLocation = "C:\Program Files\Graphviz\bin"

ImageStorage = {
    "ImagesSinkProcessDiscovery":"ProcessDiscoveryImages",
    "alphaMiner":"Alphaminer.png",
    "alphaPlusMiner": "AlphaPlusMiner.png",
    "inductiveMiner":"InductiveMiner.png",
    "heuristicsMiner":"HeuristicsMiner.png",
    "heuristicsNetMiner":"HeuristicsNetMiner.png",
    "processTreeInductive": "ProcessTreeInductive.png",
    "dfg":"DFG.png",
    "ImagesSinkProcessConformance":"ProcessConformanceImages"
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
    "MinerConformanceEvaluation": "MinerConformanceEvaluation.csv"
}

GraphViz = {
    "binLocation": "C:\Program Files\Graphviz\\bin",
    "exeLocation": "C:\Program Files\Graphviz\\bin\dot.exe"
}