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
    __Y_rejected = None


    def __init__(self, settings, dbContext : DbContext):
        PredictiveTechniques.__Settings = settings
        PredictiveTechniques.__DbContext = dbContext
        self.__ReadCsvDataSet()

    def __RunSVR(self, Y, name : str):
        logging.info("Running SVR")
        try:
            svrML = SVRML(PredictiveTechniques.__Settings, PredictiveTechniques.__DbContext)
            gpScore = svrML.Run(PredictiveTechniques.__X, Y, name)
            del svrML
            return gpScore
        except Exception as e:
            logging.error("Error occurred running SVR", exc_info=True)

    def __RunMLP(self, Y, name : str):
        logging.info("Running MLP")
        try:
            mlpML = MLPML(PredictiveTechniques.__Settings, PredictiveTechniques.__DbContext)
            gpScore = mlpML.Run(PredictiveTechniques.__X, Y, name)
            del mlpML
            return gpScore
        except Exception as e:
            logging.error("Error occurred running MLP", exc_info=True)

    def __RunDTR(self, Y, name : str):
        logging.info("Running DTR")
        try:
            dtrML = DTRML(PredictiveTechniques.__Settings, PredictiveTechniques.__DbContext, PredictiveTechniques.__X.size)
            gpScore = dtrML.Run(PredictiveTechniques.__X, Y, name)
            del dtrML
            return gpScore
        except Exception as e:
            logging.error("Error occurred running DTR", exc_info=True)

    def __RunInParrallel(self, *fns):
        from multiprocessing import Process
        proc = []
        for fn in fns:
            p = Process(target=fn)
            p.start()
            proc.append(p)
        for p in proc:
            p.join()

    def RunWorkRatioEstimation(self):
        logging.info("Running WorkRatio estimation")
        try:
            #self.__RunInParrallel(self.__RunSVR, self.__RunDTR, self.__RunMLP)
            dtr_results = self.__RunDTR(PredictiveTechniques.__Y_workRatio, "DTRWORKRATIO")
            mlp_results = self.__RunMLP(PredictiveTechniques.__Y_workRatio, "MLPWORKRATIO")
            svr_results = self.__RunSVR(PredictiveTechniques.__Y_workRatio, "SVRWORKRATIO")

            import matplotlib.pyplot as plt
            plt.clf()
            import numpy as np
            plt.plot(np.arange(1, len(dtr_results) +1), dtr_results, label='DTR GP score')
            plt.plot(np.arange(1, len(mlp_results) +1), mlp_results, label='MLP GP score')
            plt.plot(np.arange(1, len(svr_results) +1), svr_results, label='LinearSVR GP score')
            plt.title(f"Score per GP run for work ratio score")
            plt.xlabel("Run count")
            plt.ylabel("Mean absolute error")
            repsoitoryLocation = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../Domain/Repositories")
            imagesSink = os.path.join(repsoitoryLocation, PredictiveTechniques.__Settings.ImageStorage["ImagesSinkProcessDiscovery"])
            plt.grid(visible=True, axis='both', which='both')
            plt.xlim(xmin=0)
            plt.savefig(os.path.join(imagesSink, "GPSCOREWORKRATIO.png"))
            del plt
        except Exception as e:
            logging.error("Error occurred while running workRatio estimation", exc_info=True)

    def RunFitnessEstimation(self):
        logging.info("Running Fitness estimation")
        try:
            #self.__RunInParrallel(self.__RunSVR, self.__RunDTR, self.__RunMLP)
            dtr_results = self.__RunDTR(PredictiveTechniques.__Y_fitness, "DTRFITNESS")
            mlp_results = self.__RunMLP(PredictiveTechniques.__Y_fitness, "MLPFITNESS")
            svr_results = self.__RunSVR(PredictiveTechniques.__Y_fitness, "SVRFITNESS")

            import matplotlib.pyplot as plt
            plt.clf()
            import numpy as np
            plt.plot(np.arange(1, len(dtr_results) +1), dtr_results, label='DTR GP score')
            plt.plot(np.arange(1, len(mlp_results) +1), mlp_results, label='MLP GP score')
            plt.plot(np.arange(1, len(svr_results) +1), svr_results, label='LinearSVR GP score')
            plt.title(f"Score per GP run for Fitness score")
            plt.xlabel("Run count")
            plt.ylabel("Mean absolute error")
            repsoitoryLocation = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../Domain/Repositories")
            imagesSink = os.path.join(repsoitoryLocation, PredictiveTechniques.__Settings.ImageStorage["ImagesSinkProcessDiscovery"])
            plt.grid(visible=True, axis='both', which='both')
            plt.xlim(xmin=0)
            plt.savefig(os.path.join(imagesSink, "GPSCOREFITNESS.png"))
            del plt
        except Exception as e:
            logging.error("Error occurred while running workRatio estimation", exc_info=True)

    def __ReadCsvDataSet(self):
        logging.info("Reading in data set for SVR")
        try:
            fileManager = CsvFileManager(PredictiveTechniques.__DbContext, PredictiveTechniques.__Settings)
            dataset = fileManager.ReadFileToDataFrame(PredictiveTechniques.__Settings.CsvStorageManager["mlDataSet"])
            columnsToDrop = ['df_index','Key', 'WorkRatio', 'Fitness', 'Rejected']
            PredictiveTechniques.__X = dataset.drop(columnsToDrop, axis='columns')
            PredictiveTechniques.__Y_workRatio = dataset['WorkRatio']
            PredictiveTechniques.__Y_fitness = dataset['Fitness']
            PredictiveTechniques.__Y_rejected = dataset['Rejected']
            logging.info(f"ML data set shape is {dataset.shape}")
        except Exception as e:
            logging.error("Error occurred while reading in dataset for SVR.", exc_info=True)