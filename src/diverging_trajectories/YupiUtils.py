from yupi import Trajectory, TrajectoryPoint
from yupi._checkers import (
    check_exact_dim,
    check_same_dim,
    check_same_dt,
    check_same_t,
    check_uniform_time_spaced,
)

from yupi.transformations._resamplers import resample, _interpolate_axis
from typing import *
import numpy as np

class YupiUtils:

    @staticmethod
    def haveSamePos(p1: TrajectoryPoint, p2: TrajectoryPoint) -> bool:
        return np.array_equal(p1.r, p2.r)

    @staticmethod
    def areSamePointsInTime(p1: TrajectoryPoint, p2: TrajectoryPoint) -> bool:
        return YupiUtils.haveSamePos(p1, p2) and p1.t == p2.t
    
    
    @staticmethod
    @check_same_dim
    def speed_ensemble(trajs: List[Trajectory], step: int = 1) -> np.ndarray:
        """
        Estimate speeds of the list of trajectories, ``trajs``,
        by computing displacements according to a certain sample
        frequency given by ``step``.

        Parameters
        ----------
        trajs : List[Trajectory]
            Input list of trajectories.
        step : int
            Numer of sample points.

        Returns
        -------
        np.array
            Concatenated array of speeds.
        """

        trajs_ = [YupiUtils.subsample(traj, step) for traj in trajs]
        return np.concatenate([traj.v.norm for traj in trajs_])
    
    def subsample(traj: Trajectory, step: int = 1, new_traj_id: Optional[str] = None):
        """
        Sample the trajectory ``traj`` by removing evenly spaced
        points according to ``step``.

        Parameters
        ----------
        traj : Trajectory
            Input trajectory.
        step : int, optional
            Number of sample points or period. By default 1.
        new_traj_id : Optional[str]
            New trajectory ID. By default None.

        Returns
        -------
        Trajectory
            Output trajectory.
        """

        points = traj.r[::step]
        t = traj.t[::step] if traj.t is not None else None

        subsampled_traj = Trajectory(
            points=points,
            t=t,
            t_0=t[0],
            dt=step * traj.dt,
            traj_id=new_traj_id,
            diff_est=traj.diff_est,
        )
        return subsampled_traj
    
    def resample(
        traj: Trajectory,
        new_dt: Optional[float] = None,
        new_t: Optional[Collection[float]] = None,
        new_traj_id: Optional[str] = None,
        order: int = 1,
    ):
        """
        Resamples a trajectory to a new dt or a new array of time.

        One of ``new_dt`` or ``new_t`` must be specified.

        Parameters
        ----------
        traj : Trajectory
            Input trajectory.
        new_dt: Optional[float]
            New dt. By default None.
        new_t: Optional[Collection[float]]
            New sample rate or array of time. By default None.
        new_traj_id : Optional[str]
            New trajectory ID. By default None.
        order : int, optional
            How many points to use for the interpolation of each value. By default 2.

        Returns
        -------
        Trajectory
            Output trajectory.

        Raises
        ------
        ValueError
            If neither ``new_dt`` nor ``new_t`` is specified.
        ValueError
            If both ``new_dt`` and ``new_t`` are specified.
        """

        if new_t is not None and new_dt is not None:
            raise ValueError("new_t and new_dt cannot be both specified")
        if new_t is None and new_dt is None:
            raise ValueError("new_t or new_dt must be specified")

        from_dt = new_dt is not None

        new_t = (
            traj.t[0] + np.arange(0, traj.t[-1], new_dt)
            if new_dt is not None
            else np.array(new_t)
        )
        new_dims: List[Collection[float]] = []
        old_t = traj.t

        for dim in range(traj.dim):
            dim_data = traj.r.component(dim)
            new_dim = _interpolate_axis(dim_data, old_t, new_t, order)
            new_dims.append(new_dim)

        if from_dt:
            return Trajectory(
                axes=new_dims,
                dt=new_dt,
                traj_id=new_traj_id,
                diff_est=traj.diff_est,
            )
        return Trajectory(
            axes=new_dims,
            t=new_t,
            traj_id=new_traj_id,
            diff_est=traj.diff_est,
        )
