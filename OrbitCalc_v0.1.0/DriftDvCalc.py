# Built by John W. Harms ##
# Version 0.01 -- Initial Build ##
# Version 0.02 -- Refactored to be added as module to different project ##
# Last Change 12 June 15
import math
from Hohman import Hohman


# Constants
mu = 398600.000000000000000000000
radSec2degDay = 4950355.35


def DriftDvCalc(DriftDvCurrentDriftRate, DriftDvTargetDriftRate):
    DriftDvCalc_w = 0.0000729211585530  # rad/sol sec
    DriftDvCalc_SVd = DriftDvCurrentDriftRate / radSec2degDay
    DriftDvCalc_SVa = math.pow((mu / (math.pow((DriftDvCalc_SVd + DriftDvCalc_w), 2))), (1.00000 / 3.00000))
    DriftDvCalc_Targd = DriftDvTargetDriftRate / radSec2degDay
    DriftDvCalc_Targa = math.pow((mu / (math.pow((DriftDvCalc_Targd + DriftDvCalc_w), 2))), (1.00000 / 3.00000))

    hohman_out  = Hohman(DriftDvCalc_SVa, DriftDvCalc_Targa)

    DriftDvCalc_out = "DriftDvCalc Transfer elements are: " \
                      "\nStarting SMA: %.3f KM\nTarget SMA: %.3f KM\n\n%s" \
                      % (DriftDvCalc_Targa, DriftDvCalc_SVa, hohman_out)

    return DriftDvCalc_out
