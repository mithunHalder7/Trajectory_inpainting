import pytest
import sys
import os
 
# append the path of the
# parent directory
sys.path.append(os.path.join(os.getcwd(), "src"))
# print(sys.path)

from diverging_trajectories.pattern.IntervalPatternSequence import IntervalPatternSequence

from diverging_trajectories.pattern.PatternModel import PatternModel

def test_points():
    seqModel = IntervalPatternSequence.create(sourceId="testSourceId", interval=100)
    pm = PatternModel.create(
            sourceId = seqModel.sourceId,
            interval = seqModel.interval,
            patternSeqNo = 10,
            points = [(1, 2), (3, 4)],
            t_0 = 1000,
            sequence = seqModel
        )
    print(pm.points)
    assert pm.points == [(1, 2), (3, 4)]