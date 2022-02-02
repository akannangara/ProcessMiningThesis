import logging
from dataclasses import dataclass
from datetime import datetime

@dataclass
class JiraSprint:
    Id : int
    StartDate : datetime
    EndDate : datetime
    Name : str
    Goal : str

    def __init__(self, jiraSprint):
        self.Id = jiraSprint.id
        self.StartDate = jiraSprint.startDate
        self.EndDate = jiraSprint.endDate
        self.Name = jiraSprint.name
        self.Goal = ""
        if hasattr(jiraSprint, 'goal'):
            self.Goal = jiraSprint.goal