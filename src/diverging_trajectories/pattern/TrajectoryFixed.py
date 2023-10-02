
import warnings
from typing import *
import numpy as np
from yupi import Trajectory, TrajectoryPoint
from yupi.trajectory import Axis, Point, Vector, _THRESHOLD


class TrajectoryFixed(Trajectory):
    
    def __init__(
        self,
        x: Optional[Axis] = None,
        y: Optional[Axis] = None,
        z: Optional[Axis] = None,
        points: Optional[Collection[Point]] = None,
        axes: Optional[Collection[Axis]] = None,
        t: Optional[Collection[float]] = None,
        dt: Optional[float] = None,
        t_0: float = 0.0,
        traj_id: str = "",
        lazy: Optional[bool] = False,
        diff_est: Optional[Dict[str, Any]] = None,
        vel_est: Optional[Dict[str, Any]] = None,
        t0: Optional[float] = None,  # pylint: disable=invalid-name
    ):  # pylint: disable=too-many-arguments
        
        if t is not None:
            t_0 = t[0]

        super().__init__(
            x=x,
            y=y,
            z=z,
            points=points,
            axes=axes,
            t=t,
            dt=dt,
            t_0=t_0,
            traj_id=traj_id,
            lazy=lazy,
            diff_est=diff_est,
            vel_est=vel_est,
            t0=t0,
        )
            
    def __getitem__(self, index) -> Union[Trajectory, TrajectoryPoint]:
            if isinstance(index, int):
                index = index % len(self.r)
            return super().__getitem__(index) # fix