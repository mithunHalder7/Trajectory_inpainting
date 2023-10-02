from abc import ABC, abstractmethod
from typing import *
import pandas as pd

from diverging_trajectories.pattern import Pattern
from diverging_trajectories.YupiUtils import YupiUtils

class SequenceExtractor(ABC):

    @abstractmethod
    def extract(self, trackId: str, track: pd.DataFrame) -> List[Pattern]:
        raise NotImplementedError()
    
    def validateSequence(self, patterns: List[Pattern]) -> bool:
        # sequence validity checks that the starting point of a Pattern is the ending point of the previous only
        prevPattern = None
        for pattern in patterns:
            if prevPattern is not None:
                # print(f"prevPattern ={prevPattern.r}, {prevPattern.t}")
                prevEnd = prevPattern[-1]
                currStart = pattern[0]
                # print(f"prevEnd={prevEnd}, \ncurrStart={currStart}")
                if not YupiUtils.areSamePointsInTime(prevEnd, currStart): # match pos and time
                    return False

            prevPattern = pattern
        return True