import logging
from typing import List
from pydantic import BaseModel

from dataclasses import dataclass

@dataclass
class ProcessMinerConformance:
    MinerName : str
    AverageFitness : float
    PercentageOfFittingTraces : float
    LogFitness : float
    Precision : float
    Generalization : float
    Simplicity : float

    def __init__(self, minerName: str, fitness, precision : float, generalization : float, simplicity : float):
        self.MinerName = minerName
        self.AverageFitness = fitness['averageFitness']
        self.PercentageOfFittingTraces = fitness['percentage_of_fitting_traces']
        self.LogFitness = fitness['log_fitness']
        self.Precision = precision
        self.Generalization = generalization
        self.Simplicity = simplicity