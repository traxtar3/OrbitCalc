# Built by John W. Harms ##
# Version 0.01 -- Initial Build ##
# Version 0.02 -- Refactored to be added as module to different project ##

# Last Change 12 June 15

import math


# Constants
mu = 398600.000000000000000000000
sidrealDay = 0.997269566329084
geoSMA = 42164.15405400000000000
radSec2degDay = 4950355.35


def SMA2Drift(DriftRelGeo):
    SMA2Drift_sma = geoSMA + DriftRelGeo
    SMA2Drift_n = math.sqrt(mu / (math.pow(SMA2Drift_sma, 3.000000000)))
    SMA2Drift_drift = (-1) * (360 - (SMA2Drift_n * radSec2degDay * sidrealDay))
    if SMA2Drift_sma > geoSMA:
        SMA2Drift_drift = (360 - (SMA2Drift_n * radSec2degDay * sidrealDay))
        SMA2Drift_str = "deg/day West"
    else:
        SMA2Drift_str = "deg/day East"
    SMA2Drift_drift_out = "%.3f %s" % (SMA2Drift_drift, SMA2Drift_str)
    return SMA2Drift_drift_out
