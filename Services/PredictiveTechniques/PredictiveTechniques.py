import logging
import os
import pandas as pd
from pydantic import BaseModel
from typing import List, Dict

from CsvFileManager import CsvFileManager

from ProcessDiscovery import ProcessDiscovery
from ConformanceChecking import ConformanceChecking
from ProcessEnhancement import ProcessEnhancement
from DbContext import DbContext

from SVRML import SVRML
from DTRML import DTRML
from MLPML import MLPML

from enum import Enum

class DataSetY(Enum):
    WorkRatio=1,
    Fitness=2


class PredictiveTechniques(BaseModel):
    __Settings = None
    __DbContext = None
    __X = None
    __Y_workRatio = None
    __Y_fitness = None


    def __init__(self, settings, dbContext : DbContext):
        PredictiveTechniques.__Settings = settings
        PredictiveTechniques.__DbContext = dbContext
        self.__ReadCsvDataSet()

    def RunWorkRatioEstimation(self):
        logging.info("Running WorkRatio estimation")
        try:
            svrML = SVRML(PredictiveTechniques.__Settings, PredictiveTechniques.__DbContext)
            svrML.Run(PredictiveTechniques.__X, PredictiveTechniques.__Y_workRatio)

            dtrML = DTRML(PredictiveTechniques.__Settings, PredictiveTechniques.__DbContext, PredictiveTechniques.__X.size)
            dtrML.Run(PredictiveTechniques.__X, PredictiveTechniques.__Y_workRatio)

            mlpML = MLPML(PredictiveTechniques.__Settings, PredictiveTechniques.__DbContext)
            mlpML.Run(PredictiveTechniques.__X, PredictiveTechniques.__Y_workRatio)
        except Exception as e:
            logging.error("Error occurred while running workRatio estimation", exc_info=True)


    def __ReadCsvDataSet(self):
        logging.info("Reading in data set for SVR")
        try:
            fileManager = CsvFileManager(PredictiveTechniques.__DbContext, PredictiveTechniques.__Settings)
            dataset = fileManager.ReadFileToDataFrame(PredictiveTechniques.__Settings.CsvStorageManager["mlDataSet"])
            columnsToDrop = ['df_index','Key', 'WorkRatio', 'Fitness']
            PredictiveTechniques.__X = dataset.drop(columnsToDrop, axis='columns')
            PredictiveTechniques.__Y_workRatio = dataset['WorkRatio']
            PredictiveTechniques.__Y_fitness = dataset['Fitness']
            logging.info(f"ML data set shape is {dataset.shape}")
        except Exception as e:
            logging.error("Error occurred while reading in dataset for SVR.", exc_info=True)