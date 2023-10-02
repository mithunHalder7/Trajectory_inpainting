from yupi import Trajectory, TrajectoryPoint

from src.diverging_trajectories.YupiUtils import YupiUtils

import numpy as np

def test_haveSamePos():
    traj1 = Trajectory(points=[[1,2], [3,3], [4,2]])
    traj2 = Trajectory(points=[[1,2], [3,3], [4,2]])

    p1 = traj1[0]
    p2 = traj2[0]

    # print(p1, p2)

    # print(traj1[1])

    # assert False
    assert YupiUtils.haveSamePos(p1, p2)
    assert YupiUtils.haveSamePos(p1, traj2[1]) == False

def test_areSamePointsInTime():
    traj1 = Trajectory(points=[[1,2], [3,3], [4,2]])
    traj2 = Trajectory(points=[[1,2], [3,3], [4,2]])
    traj3 = Trajectory(points=[[1,2], [3,3], [4,2]], t0=10.0)
    traj4 = Trajectory(points=[[1,2], [3,3], [1,2]], dt=5)

    p1 = traj1[0]
    p2 = traj2[0]
    p3 = traj3[0]
    p4 = traj4[-1]

    print(p3, p4)

    # assert False
    assert YupiUtils.areSamePointsInTime(p1, p2)
    assert YupiUtils.areSamePointsInTime(p1, p3) == False
    assert YupiUtils.areSamePointsInTime(p3, p4)