import logging
from typing import List
from dataclasses import dataclass

from TTeamMember import TTeamMember
from datetime import datetime

@dataclass
class TeamMember():
    Key : str
    DisplayName : str
    Name : str
    Active : bool
    Type : str

    def __init__(self, teamMember : TTeamMember):
        self.Key = teamMember.Key
        self.DisplayName = teamMember.DisplayName
        self.Name = teamMember.Name
        self.Active = teamMember.Active
        self.Type = teamMember.Type