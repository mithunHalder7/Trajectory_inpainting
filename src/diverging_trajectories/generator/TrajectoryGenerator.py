from typing import List
from diverging_trajectories.pattern.IntervalPatternRepository import IntervalPatternRepository
from diverging_trajectories.pattern.Pattern import Pattern
from diverging_trajectories.pattern.TrajectoryFixed import TrajectoryFixed
from tti_dataset_tools import TrajectoryUtils

class TrajectoryGenerator:

    def combinePatterns(self, patterns = List[Pattern]) -> Pattern:

        points = []
        interval  = 0
        shift = (0, 0)
        prevPattern = None
        for pattern in patterns:
            # pattern = Pattern.shift(pattern, shift)
            # print(f"Adding new pattern")
            if len(points) > 0:
                shift = (points[-1][0] - pattern.points[0][0], points[-1][1] - pattern.points[0][1])
                # print(f"shift={shift}, points[-1] {points[-1]}, pattern.points[0] {pattern.points[0]}")
            shiftedPoints = TrajectoryUtils.shift(pattern.points, shift)
            # print("pattern.points", pattern.points)
            # print("shiftedPoints", shiftedPoints)
            points.extend(shiftedPoints)
            interval += pattern.interval
            
        
        pattern = Pattern (
            sourceId = patterns[0].sourceId,
            interval = interval,
            patternSeqNo = patterns[0].patternSeqNo,
            points = points,
            t_0 = patterns[0].t_0,
            yOffset = patterns[0].yOffset
        )

        # print(f"pattern.headingStart={pattern.headingStart}, pattern.headingEnd={pattern.headingEnd}")
        # print(f"patterns[0].headingStart={patterns[0].headingStart}, pattern[-1].headingEnd={patterns[-1].headingEnd}")
        assert pattern.headingStart == patterns[0].headingStart
        assert pattern.headingEnd == patterns[-1].headingEnd

        return pattern
    

    