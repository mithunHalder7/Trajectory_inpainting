from typing import List

from src.diverging_trajectories.pattern.Pattern import Pattern


class PatternCollection:

    

    def addSequence(self, sourceId: str, interval: float, patterns: List[Pattern]):
        for i, pattern in enumerate(patterns):
            