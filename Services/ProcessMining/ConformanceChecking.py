import logging
import os
import pandas as pd
from pydantic import BaseModel

import pm4py as pm4py

class ConformanceChecking(BaseModel):
    __Settings = None


    def __init__(self, settings):
        ConformanceChecking.__Settings = settings