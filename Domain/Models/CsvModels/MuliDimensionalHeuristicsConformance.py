import logging
from typing import List
from pydantic import BaseModel

from dataclasses import dataclass
from statistics import mean

@dataclass
class MuliDimensionalHeuristicsConformance():
    MinerName : str
    dependency_threshold : float
    and_threshold : float
    loop_two_threshold : float
    AverageTraceFitness : float
    PercentageFitTraces : float
    LogFitness : float
    Precision : float
    Generalization : float
    Simplicity : float
    AverageScore : float
    AverageScoreIgnoringSimplicity : float

    def __init__(self, minerName: str, dependency_threshold : float, and_threshold: float, loop_two_threshold : float,
                 fitness, precision : float, generalization : float, simplicity : float):
        self.MinerName = minerName
        self.dependency_threshold = dependency_threshold
        self.and_threshold = and_threshold
        self.loop_two_threshold = loop_two_threshold
        self.AverageFitness = fitness['average_trace_fitness']
        self.PercentageOfFittingTraces = fitness['perc_fit_traces']
        self.LogFitness = fitness['log_fitness']
        self.Precision = precision
        self.Generalization = generalization
        self.Simplicity = simplicity
        self.AverageScore = mean([self.AverageFitness, self.Precision, self.Generalization, self.Simplicity])
        self.AverageScoreIgnoringSimplicity = mean([self.AverageFitness, self.Precision, self.Generalization])