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
				CsvFileManager.__Settings = settings
				fileDir = os.path.dirname(os.path.abspath(__file__))
				pathToRepository = os.path.join(fileDir, "../../Domain/Repositories")

				CsvFileManager.__SinkDirectory = os.path.join(pathToRepository, CsvFileManager.__Settings.CsvStorageManager["SinkDirectory"])

		def ReadFileToDataFrame(self, fileName):
				logging.info(f"Reading {fileName} to dataframe")
				try:
						df = pd.read_csv(os.path.join(CsvFileManager.__SinkDirectory, fileName), sep=';')
						return df
				except Exception as e:
						logging.error(f"Error occurred while reading in {fileName} as dataframe")
						raise

		def CreateEventLogFromDb(self, projectsList : List[str] = [], onlyDone=False):
				logging.info("Storing events from projects list " +(' '.join(str(x) for x in projectsList))+ " as csv")
				try:
						allChangeLogs = []
						if not(projectsList):
								if onlyDone:
										completedStatusIds = CsvFileManager.__Settings.CompletedStatusIds
										issues = CsvFileManager.__DbContext.QueryOr(TIssue, "StatusId", str(completedStatusIds[0]), str(completedStatusIds[1]))
										for issue in issues:
												issueChangeLogs = CsvFileManager.__DbContext.QueryAnd(TChangeLog, "IssueId", issue.Id, "Field", "status")
												allChangeLogs.extend(issueChangeLogs)
								else:
										allChangeLogs = CsvFileManager.__DbContext.Query(TChangeLog, "Field", "status")
						else:
								for project in projectsList:
										projectChangeLogs = []
										if onlyDone:
												completedStatusIds = CsvFileManager.__Settings.CompletedStatusIds
												issues = CsvFileManager.__DbContext.QueryChainOrLike(TIssue, 'StatusId', str(completedStatusIds[0]), str(completedStatusIds[1]), 'IssueKey', project+"%")
												for issue in issues:
														issueChangeLogs = CsvFileManager.__DbContext.QueryAnd(TChangeLog, "IssueId", issue.Id, "Field", "status")
														projectChangeLogs.extend(issueChangeLogs)
										else:
												projectChangeLogs = CsvFileManager.__DbContext.QueryLikeAnd(TChangeLog, 'IssueKey', project+"%", "Field", "status")
										allChangeLogs.extend(projectChangeLogs)
						if onlyDone:
								eventLogName = CsvFileManager.__Settings.CsvStorageManager["OnlyDoneEventLogFileName"]
						else:
								eventLogName = CsvFileManager.__Settings.CsvStorageManager["EventLogFileName"]
						self.DeleteFileIfExists(eventLogName)
						self.__CreateAndStoreDataFrameFromEntityList(allChangeLogs, EventLogItem, eventLogName)
						if onlyDone:
								CsvFileManager.__Settings.CsvStorageManager["EventLogFileName"] = eventLogName
				except Exception as e:
						logging.error("Error storing projects list as csv", exc_info=True)

		def CreateFileFromEntityCollection(self, entityCollection : List, entityType, filename : str):
				logging.info(f"Creating csv file {filename} from entity collection")
				try:
						self.__CreateAndStoreDataFrameFromEntityList(entityCollection, entityType, filename)
				except Exception as e:
						logging.error(f"Error occurred while creating csv {filename} from entity collection", exc_info=True)

		def DeleteFileIfExists(self, filename):
				logging.info(f"Deleting {filename} if it exists.")
				try:
						fileLocation = os.path.join(CsvFileManager.__SinkDirectory, filename)
						if os.path.exists(fileLocation):
								os.remove(fileLocation)
				except Exception as e:
						logging.error(f"Error occurred while deleting file {filename} if exits", exc_info=True)

		def CreateStatusCollectionFromDb(self):
				logging.info("Creating status collection as csv")
				try:
						allStatuses = CsvFileManager.__DbContext.Query(TStatus, "", "")
						if not(allStatuses):
								logging.error("No Statuses found when creating status collection as csv")
								return
						self.__CreateAndStoreDataFrameFromEntityList(allStatuses, StatusCsvItem, CsvFileManager.__Settings.CsvStorageManager["StatusesFileName"])
				except Exception as e:
						logging.error("Error storing status collection to csv", exc_info=True)

		def CreateTeamMemberCollectionFromDb(self):
				logging.info("Creating team member collection as csv")
				try:
						allTeamMembers = CsvFileManager.__DbContext.Query(TTeamMember, "", "")
						if not(allTeamMembers):
								logging.error("No teamMembers found when creating team member collection as csv")
								return
						self.__CreateAndStoreDataFrameFromEntityList(allTeamMembers, TeamMember, CsvFileManager.__Settings.CsvStorageManager["TeamMembersFileName"])
				except Exception as e:
						logging.error("Error storing teamMember collection to csv", exc_info=True)

		def UpdateTeamMemberTypeFromCsv(self):
				logging.info("Updating TeamMember collection from csv")
				try:
						dataframe = pd.read_csv(os.path.join(CsvFileManager.__SinkDirectory, CsvFileManager.__Settings.CsvStorageManager["TeamMembersFileName"]), sep=';')
						for index, row in dataframe.iterrows():
								dbEntity = CsvFileManager.__DbContext.Query(TTeamMember, "Key", row["Key"])
								if not(dbEntity):
										continue
								dbEntity[0].Type = row.Type
								CsvFileManager.__DbContext.UpdateEntity(dbEntity[0])
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
						if type(entity) == entityType:
								row = entity
						else:
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
				filePath = os.path.join(CsvFileManager.__SinkDirectory, filename)
				dataframe.to_csv(filePath, sep=';', mode='a', header=not(os.path.exists(filePath)))