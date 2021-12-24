import os
import logging
from typing import List
from pydantic import BaseModel

import pandas as pd

from DbContext import DbContext
from EventLogItem import EventLogItem
from TeamMember import TeamMember
from StatusCsvItem import StatusCsvItem
from TIssue import TIssue
from TChangeLog import TChangeLog
from TTeamMember import TTeamMember
from TStatus import TStatus

from ProcessMinerConformance import ProcessMinerConformance

class CsvFileManager(BaseModel):
		__DbContext = None
		__Settings = None
		__SinkDirectory = None

		def __init__(self, dbContext : DbContext, settings):
				CsvFileManager.__DbContext = dbContext
				CsvFileManager.__Settings = settings.CsvStorageManager
				fileDir = os.path.dirname(os.path.abspath(__file__))
				pathToRepository = os.path.join(fileDir, "../../Domain/Repositories")

				CsvFileManager.__SinkDirectory = os.path.join(pathToRepository, CsvFileManager.__Settings["SinkDirectory"])

		def CreateEventLogFromDb(self, projectsList : List[str] = [], onlyDone=False):
				logging.info("Storing events from projects list " +(' '.join(str(x) for x in projectsList))+ " as csv")
				try:
						eventLogName = CsvFileManager.__Settings["EventLogFileName"]
						allChangeLogs = []
						if not(projectsList):
								if onlyDone:
										#10001 == Done and 10003 == Rejected
										issues = CsvFileManager.__DbContext.QueryOr(TIssue, "StatusId", "10001", "10003")
										for issue in issues:
												issueChangeLogs = CsvFileManager.__DbContext.Query(TChangeLog, "IssueId", issue.Id)
												allChangeLogs.extend(issueChangeLogs)
								else:
										allChangeLogs = CsvFileManager.__DbContext.Query(TChangeLog, "", "")
						else:
								for project in projectsList:
										projectChangeLogs = []
										if onlyDone:
												issues = CsvFileManager.__DbContext.QueryChainOrLike(TIssue, 'StatusId', "10001", "10003", 'IssueKey', project+"%")
												for issue in issues:
														issueChangeLogs = CsvFileManager.__DbContext.Query(TChangeLog, "IssueId", issue.Id)
														projectChangeLogs.extend(issueChangeLogs)
										else:
												projectChangeLogs = CsvFileManager.__DbContext.QueryLike(TChangeLog, 'IssueKey', project+"%")
										allChangeLogs.extend(projectChangeLogs)
						if onlyDone:
								eventLogName = CsvFileManager.__Settings["OnlyDoneEventLogFileName"]
						else:
								eventLogName = CsvFileManager.__Settings["EventLogFileName"]
						self.__CreateAndStoreDataFrameFromEntityList(allChangeLogs, EventLogItem, eventLogName)
						if onlyDone:
								CsvFileManager.__Settings["EventLogFileName"] = eventLogName
				except Exception as e:
						logging.error("Error storing projects list as csv", exc_info=True)

		def CreateStatusCollectionFromDb(self):
				logging.info("Creating status collection as csv")
				try:
						allStatuses = CsvFileManager.__DbContext.Query(TStatus, "", "")
						if not(allStatuses):
								logging.error("No Statuses found when creating status collection as csv")
								return
						self.__CreateAndStoreDataFrameFromEntityList(allStatuses, StatusCsvItem, CsvFileManager.__Settings["StatusesFileName"])
				except Exception as e:
						logging.error("Error storing status collection to csv", exc_info=True)

		def CreateTeamMemberCollectionFromDb(self):
				logging.info("Creating team member collection as csv")
				try:
						allTeamMembers = CsvFileManager.__DbContext.Query(TTeamMember, "", "")
						if not(allTeamMembers):
								logging.error("No teamMembers found when creating team member collection as csv")
								return
						self.__CreateAndStoreDataFrameFromEntityList(allTeamMembers, TeamMember, CsvFileManager.__Settings["TeamMembersFileName"])
				except Exception as e:
						logging.error("Error storing teamMember collection to csv", exc_info=True)

		def UpdateTeamMemberTypeFromCsv(self):
				logging.info("Updating TeamMember collection from csv")
				try:
						dataframe = pd.read_csv(os.path.join(CsvFileManager.__SinkDirectory, CsvFileManager.__Settings["TeamMembersFileName"]), sep=';')
						for index, row in dataframe.iterrows():
								dbEntity = CsvFileManager.__DbContext.Query(TTeamMember, "Key", row["Key"])
								dbEntity.Type = row["Type"]
								CsvFileManager.__DbContext.UpdateEntity(dbEntity)
				except Exception as e:
						logging.error("Error updating teamMember from csv", exc_info=True)

		def StoreMinerConformanceEvaluation(self, conformanceCollection : List[ProcessMinerConformance], fileName : str):
				dataframe = pd.DataFrame()
				for conformanceItem in conformanceCollection:
						dataframe = self.__AddEntityToDataFrame(conformanceItem, dataframe)
				self.__SaveDataFrameToCsv(dataframe, fileName)

		def __CreateAndStoreDataFrameFromEntityList(self, entityList : List, entityType, filename : str):
				dataframe = pd.DataFrame()
				for entity in entityList:
						row = entityType(entity)
						dataframe = self.__AddEntityToDataFrame(row, dataframe)
				self.__SaveDataFrameToCsv(dataframe, filename)

		def __AddEntityToDataFrame(self, entity, dataframe : pd.DataFrame):
				properties = entity.__dict__
				data = {}
				for key, value in properties.items():
						data[key] = [value]
				dataframe = pd.concat([dataframe, pd.DataFrame(data)], ignore_index=True)
				return dataframe

		def __SaveDataFrameToCsv(self, dataframe : pd.DataFrame, filename : str):
				dataframe.index.name = "df_index"
				dataframe.to_csv(os.path.join(CsvFileManager.__SinkDirectory, filename), sep=';')