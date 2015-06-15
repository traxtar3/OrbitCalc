# Built by John W. Harms ##
# Version 0.01 -- Initial Build ##
# Version 0.02 -- Refactored to be added as module to different project ##
# Last Change 08 June 15
import math

# Constants
mu = 398600.000000000000000000000
radSec2degDay = 4950355.35


def Drift2SMA(Drift2SMArate):
    Drift2SMA_d = Drift2SMArate / radSec2degDay
    Drift2SMA_w = (0.0000729211585530)  # rad/sol sec
    Drift2SMA_a = math.pow(((mu) / (math.pow((Drift2SMA_d + Drift2SMA_w), 2))), (1.00000 / 3.00000))
    if Drift2SMA_a > 42164.154054:
        Drift2SMA_abvbel = "above"
    else:
        Drift2SMA_abvbel = "below"
    Drift2SMA_aDif = math.fabs(42164.154054 - Drift2SMA_a)
    Drift2SMA_out = "Semi-Major Axis is %09.3f Km\n %.3f km %s GEO" % (Drift2SMA_a, Drift2SMA_aDif, Drift2SMA_abvbel)
    return Drift2SMA_out
