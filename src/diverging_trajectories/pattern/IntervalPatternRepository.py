from functools import lru_cache
from .db import db
from typing import List
from diverging_trajectories.pattern import Pattern
from diverging_trajectories.pattern.IntervalPatternSequence import IntervalPatternSequence
from diverging_trajectories.pattern.PatternModel import PatternModel
from diverging_trajectories.pattern.PatternSequence import PatternSequence


class IntervalPatternRepository:
    def __init__(self, intervalType: str) -> None:
        self.intervalType = intervalType
        pass


    def addSequence(self, sourceId: str, interval: float, patterns: List[Pattern]) -> IntervalPatternSequence:
        seqModel = IntervalPatternSequence.create(sourceId=sourceId, interval=interval, type=self.intervalType)
        for i, pattern in enumerate(patterns):
            PatternModel.create(
                sourceId = seqModel.sourceId,
                interval = seqModel.interval,
                patternSeqNo = i,
                points = pattern.points,
                t_0 = pattern.t_0,
                sequence = seqModel,
                yOffset = pattern.yOffset,
                roundYOffset = pattern.roundYOffset,
                headingStart = pattern.headingStart,
                headingEnd = pattern.headingEnd
            )
        return seqModel
    

    def toPatterns(self, pms: List[PatternModel]) -> Pattern:
        ps = []
        for pm in pms:
            ps.append(self.toPattern(pm))
        return ps

    def toPattern(self, pm: PatternModel) -> Pattern:
        # print(pm.points)
        return Pattern(
            sourceId=pm.sourceId,
            interval=pm.interval,
            patternSeqNo=pm.patternSeqNo,
            points=pm.points,
            t_0=pm.t_0,
            yOffset=pm.yOffset
        )


    ## region search methods

    
    @lru_cache(maxsize=1)
    def getSequences(self) -> List[IntervalPatternSequence]:
        return IntervalPatternSequence.select().where(IntervalPatternSequence.type == self.intervalType)
    
    @lru_cache(maxsize=1)
    def getPatterns(self) -> List[Pattern]:
        pms = PatternModel.select().join(IntervalPatternSequence).where(IntervalPatternSequence.type == self.intervalType)
        return self.toPatterns(pms)
    
    @lru_cache(maxsize=1)
    def getPatternsByRoundOffset(self, roundYOffset: int) -> List[Pattern]:
        pms = PatternModel.select().join(IntervalPatternSequence).where((IntervalPatternSequence.type == self.intervalType) & (PatternModel.roundYOffset == roundYOffset))
        return self.toPatterns(pms)
    
    @lru_cache(maxsize=1)
    def getPatternsByHeadingStart(self, startPositive: bool, roundYOffset: int) -> List[Pattern]:
        if startPositive:
            clauses = (PatternModel.headingStart >= 0)
        else:
            clauses = (PatternModel.headingStart < 0)

        clauses = clauses & (PatternModel.roundYOffset == roundYOffset)
        pms = PatternModel.select().join(IntervalPatternSequence).where((IntervalPatternSequence.type == self.intervalType) & clauses)
        return self.toPatterns(pms)
    
    @lru_cache(maxsize=1)
    def getPatternsByHeadingBoth(self, startPositive: bool, endPositive: bool, roundYOffset: int) -> List[Pattern]:
        if startPositive:
            clauses = (PatternModel.headingStart >= 0)
        else:
            clauses = (PatternModel.headingStart < 0)
        if endPositive:
            clauses = clauses & (PatternModel.headingEnd >= 0)
        else:       
            clauses = clauses & (PatternModel.headingEnd < 0)
        clauses = clauses & (PatternModel.roundYOffset == roundYOffset)
        pms = PatternModel.select().join(IntervalPatternSequence).where((IntervalPatternSequence.type == self.intervalType) & clauses)
        return self.toPatterns(pms)

    
    @lru_cache(maxsize=1)
    def getCachedPatterns(self) -> List[Pattern]:
        pms = PatternModel.select().join(IntervalPatternSequence).where(IntervalPatternSequence.type == self.intervalType)
        return self.toPatterns(pms)
    



    
    ## End region search methods