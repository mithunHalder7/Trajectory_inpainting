from typing import List
from peewee import *

from diverging_trajectories.pattern.BaseModel import BaseModel
from diverging_trajectories.pattern import Pattern
from diverging_trajectories.pattern.PatternSequence import PatternSequence


class IntervalPatternSequence(BaseModel):
    sourceId = CharField(primary_key=True)
    interval = FloatField()
    type = CharField(max_length=5)
    # def __init__(
    #         self,
    #         sourceId: str,
    #         patterns: List[Pattern],
    #         interval: float,
            
    #         ) -> None:
    #     self.sourceId = sourceId
    #     self.patterns = patterns
    #     self.interval = interval
    #     pass
    class Meta:
        table_name = 'interval_pattern_sequence'
