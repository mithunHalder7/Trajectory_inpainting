from typing import *
import pandas as pd
import logging
import math
from sortedcontainers import SortedList
import numpy as np

from diverging_trajectories.pattern import Pattern
from diverging_trajectories.YupiUtils import YupiUtils
from diverging_trajectories.pattern.SequenceExtractor import SequenceExtractor


class DisplacementIntervalSequenceExtractor(SequenceExtractor):
    """This extractor discards if a pattern does not equal interval in length with a little bit of tolerance.

    Args:
        SequenceExtractor (_type_): _description_
    """
    
    def __init__(
            self,
            interval: float,
            tolerance: float, # fraction of interval
            yLow: float,
            yHigh: float,
            xCol: str, yCol: str
            ) -> None:
        self.interval = interval
        self.tolerance = tolerance
        self.yLow = yLow # now we can use incomplete trajectories
        self.yHigh = yHigh
        self.xCol = xCol
        self.yCol = yCol

        assert yLow < yHigh, "yLow must be less than yHigh"

        self.segmentOffsets = SortedList([])
        for offset in np.arange(yLow, yHigh, interval):
            self.segmentOffsets.add(offset)
        # print(self.segmentOffsets)
    
    def _getSegmentOffset(self, y: float) -> float:
        """Get the offset of the segment that contains the y value.

        Args:
            y (float): y value

        Returns:
            float: offset of the segment
        """
        assert y >= self.yLow and y <= self.yHigh, f"y must be within the range of {self.yLow} and {self.yHigh}"
        idx = self.segmentOffsets.bisect_left(y)
        if y not in self.segmentOffsets:
            idx -= 1
        return self.segmentOffsets[idx]
    

    def extract(self, trackId: str, track: pd.DataFrame) -> List[Pattern]:
        
        # corner cases
        # 1. may not start at yLow
        # 2. may not end at yHigh
        # 3. may not have enough points to form a pattern
        # 4. may not have enough points to form a pattern at the end
        # 5. may not have enough points to form a pattern at the beginning

        # now we walk along the track and extract patterns
        patterns = []
        patternStarted = False
        yOffset = None
        patternRows = []
        seqNo = 0
        t_0 = 0.0
        for _, row in track.iterrows():
            if not patternStarted:
                # find the segment first
                yOffset = self._getSegmentOffset(row[self.yCol])
                patternStarted = True
                # print(f"pattern started at {row[self.yCol]} with offset {yOffset}")
            
            if patternStarted:
                patternRows.append(row)
                # check if we are still in the segment
                if row[self.yCol] > yOffset + self.interval:
                    # we are out of the segment, so we need to create a pattern
                    # print(f"pattern end at {row[self.yCol]} with offset {yOffset}")

                    if len(patternRows) > 0:
                        # convert it to a pattern
                        pattern = Pattern.fromDataFrameRows(
                            sourceId=trackId,
                            interval=self.interval,
                            patternSeqNo=seqNo,
                            rows=patternRows,
                            xCol=self.xCol,
                            yCol=self.yCol,
                            t_0=t_0,
                            yLow=self.yLow
                        )
                    patterns.append(pattern)
                    t_0 += len(patternRows) - 1 # we are adding the last point to the next
                    patternStarted = False
                    patternRows = [row] # next must start at the end of the current
                    seqNo += 1
                # else:
                #     # we are still in the segment
                #     patternRows.append(row)

        if self.validateSequence(patterns):
            return patterns
        else:
            raise ValueError("Invalid sequence. Check if they are broken.")
        # return patterns
    

    def adjustAllToInterval(
            self, 
            patterns: List[Pattern],
        ) -> List[Pattern]:
        """This adjustment cannot work as we have regular interval in time, not space.

        Args:
            patterns (List[Pattern]): _description_

        Raises:
            ValueError: _description_

        Returns:
            List[Pattern]: _description_
        """
        adjustedPatterns = []
        previousNewPattern = None
        for pattern in patterns:

            if previousNewPattern is not None:
                # two adjustments
                # the last of previous new pattern has to be the first of new pattern
                # newPattern t needs to be updated.
                new_t_0 = previousNewPattern[-1].t
                newPattern = self.adjustToStartInterval(pattern, new_t_0=new_t_0)
                newPattern = self.adjustToEndInterval(newPattern, new_t_0=new_t_0)

            else:
                new_t_0 = pattern.t_0
                newPattern = self.adjustToStartInterval(pattern, new_t_0=new_t_0)
                newPattern = self.adjustToEndInterval(newPattern, new_t_0=new_t_0)

            adjustedPatterns.append(newPattern)
            
            previousNewPattern = newPattern
            
        if self.validateSequence(adjustedPatterns):
            return adjustedPatterns
        else:
            raise ValueError("Invalid sequence. Check if they are broken.")
    
    def adjustToStartInterval(
            self,
            pattern: Pattern,
            new_t_0: float
        ) -> Pattern:
        """Adjust the pattern by predicting, instead of extending. We can train a model to predict the missing parts.
        """

        firstY = pattern[0].r[1]
        # print(f"first point y: {firstY}")
        segmentOffset = self._getSegmentOffset(firstY)
        # print(f"segmentOffset: {segmentOffset}")
        if segmentOffset != firstY:
            # we need to extend the pattern to the _getSegmentOffset
            oldPoints = pattern.points
            newPoint = (oldPoints[0][0], segmentOffset)
            newPoints = [newPoint] + oldPoints[1:]
            return Pattern(
                sourceId=pattern.sourceId,
                interval=self.interval,
                patternSeqNo=pattern.patternSeqNo,
                points=newPoints,
                t_0=new_t_0,
                yOffset=segmentOffset - self.yLow,
            )
        
        return pattern
    
    def adjustToEndInterval(
            self,
            pattern: Pattern,
            new_t_0: float
        ) -> Pattern:
        """Replaces the last point. Adjust the pattern by predicting, instead of extending. We can train a model to predict the missing parts.
        """

        lastY = pattern[-1].r[1]
        # print(f"last point y: {lastY}")
        segmentOffset = self._getSegmentOffset(lastY)
        # print(f"segmentOffset: {segmentOffset}")
        if segmentOffset != lastY:
            # we need to extend the pattern to the _getSegmentOffset
            oldPoints = pattern.points
            newPoint = (oldPoints[-1][0], segmentOffset)
            newPoints = oldPoints[0: len(oldPoints) - 1] + [newPoint]
            return Pattern(
                sourceId=pattern.sourceId,
                interval=self.interval,
                patternSeqNo=pattern.patternSeqNo,
                points=newPoints,
                t_0=new_t_0,
                yOffset=self._getSegmentOffset(pattern[0].r[1]) - self.yLow,
            )
        
        return pattern




    


