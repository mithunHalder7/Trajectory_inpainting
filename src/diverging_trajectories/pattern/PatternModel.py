import json
from typing import Collection, List
from peewee import *

from diverging_trajectories.pattern.IntervalPatternSequence import IntervalPatternSequence
from diverging_trajectories.pattern.BaseModel import BaseModel
from .db import db

class PointsField(Field):
    field_type = 'TEXT'

    def db_value(self, pointsArr: List[Collection[float]]) -> str:

        val = json.dumps(pointsArr)
        # print("python val", val)
        return val

    def python_value(self, jsonVal) -> List[Collection[float]] :
        # print("jsonVal: ", jsonVal)
        pval = json.loads(jsonVal)
        return pval

class PatternModel(BaseModel):
    sourceId = CharField()
    interval = FloatField()
    patternSeqNo = IntegerField()
    points = PointsField()
    t_0 = FloatField()
    sequence = ForeignKeyField(IntervalPatternSequence, backref='pattern')
    yOffset = FloatField(null=True)
    roundYOffset = IntegerField(null=True)
    headingStart = FloatField()
    headingEnd = FloatField()

    class Meta:
        table_name = 'pattern'
        primary_key = CompositeKey('sourceId', 'interval', 'patternSeqNo', 'sequence')