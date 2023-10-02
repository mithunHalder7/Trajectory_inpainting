from typing import List
import matplotlib.pyplot as plt
from yupi.stats import turning_angles_ensemble
from yupi.graphics import plot_2d, plot_speed_hist, plot_angles_hist

from diverging_trajectories.pattern.Pattern import Pattern
from diverging_trajectories.YupiUtils import YupiUtils

class PatternVisualizer:

    def plotPatterns(
            self,
            patterns: List[Pattern],
            hLines: List[float] = None,
            xmin: float = None,
            xmax: float = None,
            title: str = None,
            legend: bool = True,
        ):

        ax = plot_2d(patterns, show=False, legend=legend)
        if title is not None:
            ax.set_title(title)
        if hLines is not None:
            ax.hlines(hLines, colors="gray", linestyles='dotted', xmin=xmin, xmax=xmax)
            ax.set_xlim(xmin, xmax)
        plt.show()

    def speedHist(
            self,
            patterns: List[Pattern],
            title: str = None,
            
        ):
        v = YupiUtils.speed_ensemble(patterns, step=1)
        ax = plot_speed_hist(v, bins=20, show=False)
        if title is not None:
            ax.set_title(title)
        plt.show()

    def turnHist(
            self,
            patterns: List[Pattern],
            title: str = None,
            
        ):
        theta = turning_angles_ensemble(patterns)
        ax = plot_angles_hist(theta, bins=30, show=False)
        if title is not None:
            ax.set_title(title)
        plt.show()
