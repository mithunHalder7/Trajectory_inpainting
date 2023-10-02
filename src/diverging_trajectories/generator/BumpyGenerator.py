import random
from typing import List
from diverging_trajectories.pattern.IntervalPatternRepository import IntervalPatternRepository
from diverging_trajectories.pattern.Pattern import Pattern
from diverging_trajectories.pattern.TrajectoryFixed import TrajectoryFixed
from diverging_trajectories.generator.TrajectoryGenerator import TrajectoryGenerator


class BumpyGenerator(TrajectoryGenerator):
    """Bumpy generator stiches patterns without any smoothing. We can only constrain in the heading difference
    """

    def __init__(self, patternRepository: IntervalPatternRepository, interval: float, maxHeadingDiff: float = 90.0) -> None:
        """_summary_

        Args:
            patternRepository (IntervalPatternRepository): _description_
            interval (float): in meters
            maxHeadingDiff (float): in degrees
        """
        self.patternRepository = patternRepository
        self.interval = interval
        self.maxHeadingDiff = maxHeadingDiff
        pass


    def generateByRoundedOffset(self, n: int) -> List[TrajectoryFixed]:
        interval = int(self.interval)
        roundYOffset = 0
        segmentPatterns = self.patternRepository.getPatternsByHeadingStart(startPositive=True, roundYOffset=roundYOffset)
        trajPatterns = []
        for i in range(n):
            trajPatterns.append([random.choice(segmentPatterns)])

        roundYOffset += interval
        segmentPatterns = self.patternRepository.getPatternsByHeadingStart(startPositive=True, roundYOffset=roundYOffset)
        while len(segmentPatterns) > 0:
            for i in range(n): # for each trajectory to be generated, add the next segment part
                if len(trajPatterns[i]) == 0:
                    continue # has been cleared
                allowedPatterns = self.filterByHeadingDiff(trajPatterns[i][-1].headingEnd, segmentPatterns)
                if len(allowedPatterns) == 0:
                    # print(f"number of segmend patterns = {len(segmentPatterns)} and number of allowed patterns = {len(allowedPatterns)}")
                    trajPatterns[i].clear()
                    continue
                trajPatterns[i].append(random.choice(allowedPatterns))
            roundYOffset += interval
            segmentPatterns = self.patternRepository.getPatternsByHeadingStart(startPositive=True, roundYOffset=roundYOffset)
        
        nonEmptyTrajPatterns = [pattern for pattern in trajPatterns if len(pattern) > 0]
        combinedPatterns = [self.combinePatterns(patterns) for patterns in nonEmptyTrajPatterns]
        return combinedPatterns
    
    def filterByHeadingDiff(self, heading: float, patterns: List[Pattern]) -> List[Pattern]:
        filteredPatterns = []
        for pattern in patterns:
            if abs(pattern.headingStart - heading) <= self.maxHeadingDiff:
                filteredPatterns.append(pattern)
        return filteredPatterns
        
        

