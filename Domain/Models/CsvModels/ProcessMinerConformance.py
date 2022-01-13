import logging
from typing import List
from pydantic import BaseModel

from dataclasses import dataclass
from statistics import mean

@dataclass
class ProcessMinerConformance:
    MinerName : str
    AverageTraceFitness : float
    PercentageFitTraces : float
    LogFitness : float
    Precision : float
    Generalization : float
    Simplicity : float
    AverageScore : float
    AverageScoreIgnoringSimplicity : float

    def __init__(self, minerName: str, fitness, precision : float, generalization : float, simplicity : float):
        self.MinerName = minerName
        self.AverageFitness = fitness['average_trace_fitness']
        self.PercentageOfFittingTraces = fitness['perc_fit_traces']
        self.LogFitness = fitness['log_fitness']
        self.Precision = precision
        self.Generalization = generalization
        self.Simplicity = simplicity
        self.AverageScore = mean([self.AverageFitness, self.Precision, self.Generalization, self.Simplicity])
        self.AverageScoreIgnoringSimplicity = mean([self.AverageFitness, self.Precision, self.Generalization])