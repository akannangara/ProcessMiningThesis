import logging
from typing import List
from dataclasses import dataclass

from TStatus import TStatus
from datetime import datetime

@dataclass
class StatusCsvItem():
    Id : int
    Description : str
    Name : str

    def __init__(self, status : TStatus):
        self.Id = status.Id
        self.Description = status.Description
        self.Name = status.Name