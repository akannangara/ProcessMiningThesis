import os
import logging
from typing import List
from pydantic import BaseModel

import pandas as pd

from DbContext import DbContext
from EventLogItem import EventLogItem
from TChangeLog import TChangeLog

class CsvFileManager(BaseModel):
		__DbContext = None
		__Settings = None
		__SinkDirectory = None

		def __init__(self, dbContext : DbContext, settings):
				CsvFileManager.__DbContext = dbContext
				CsvFileManager.__Settings = settings
				fileDir = os.path.dirname(os.path.abspath(__file__))
				pathToRepository = os.path.join(fileDir, "../../Domain/Repositories")

				CsvFileManager.__SinkDirectory = os.path.join(pathToRepository, CsvFileManager.__Settings.CsvStorageManager["SinkDirectory"])

		def CreateEventLogFromDb(self, projectsList : List[str] = []):
				logging.info("Storing events from projects list " +(' '.join(str(x) for x in projectsList))+ " as csv")
				try:
						allChangeLogs = None
						if not(projectsList):
								for project in projectsList:
										projectChangeLogs = CsvFileManager.__DbContext.QueryLike(TChangeLog, 'IssueKey', project+"%")
										allChangeLogs.extend(projectChangeLogs)
						else:
								allChangeLogs = CsvFileManager.__DbContext.Query(TChangeLog, "", "")
						dataframe = pd.DataFrame()
						for logItem in allChangeLogs:
								event = EventLogItem(logItem)
								properties = event.__dict__
								data = {}
								for key, value in properties.items():
										data[key] = [value]
								dataframe = pd.concat([dataframe, pd.DataFrame(data)], ignore_index=True)
						filename = "Eventlog.csv"
						dataframe.index.name = "df_index"
						dataframe.to_csv(os.path.join(CsvFileManager.__SinkDirectory, filename))
				except Exception as e:
						logging.error("Error storing projects list as csv", exc_info=True)