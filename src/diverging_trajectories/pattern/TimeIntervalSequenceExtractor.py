from typing import *
import pandas as pd
import logging
import math

from diverging_trajectories.pattern import Pattern
from diverging_trajectories.YupiUtils import YupiUtils
from diverging_trajectories.pattern.SequenceExtractor import SequenceExtractor


class TimeIntervalSequenceExtractor(SequenceExtractor):

    def __init__(self, fps: float, interval: float, extendLast: False, xCol: str, yCol: str):
        self.fps = fps
        self.interval = interval
        self.timeBetweenPoints = 1 / fps
        self.patternSize = int(interval * fps)
        self.extendLast = extendLast
        self.xCol = xCol
        self.yCol = yCol
        logging.info(f"TimeIntervalSequenceExtractor: fps={fps}, patternSize={self.patternSize}")

        
    def extract(self, trackId: str, aTrack: pd.DataFrame) -> List[Pattern]:

        indices = aTrack.index.tolist()
        # print(f"extract: indices={indices}")
        nSlices = math.ceil(len(indices) / self.patternSize)

        patterns = []
        for sliceNo in range(nSlices):
            t_0 = sliceNo * self.patternSize # in timesteps
            end = (sliceNo + 1) * self.patternSize + indices[0]
            # print(f"starting at {t_0 + indices[0]} ending at {end}")
            patternDf = aTrack.loc[t_0 + indices[0] : end]
            if len(patternDf) == 0:
                break
            patterns.append(
                Pattern.fromDataFrame(
                    sourceId=trackId,
                    interval=self.interval,
                    patternSeqNo=sliceNo,
                    patternDf=patternDf,
                    xCol=self.xCol,
                    yCol=self.yCol,
                    t_0=t_0,
                    minLen=self.patternSize if self.extendLast else 1
                )
            )
        
        if self.validateSequence(patterns):
            return patterns
        else:
            raise ValueError("Invalid sequence")
                    
        