# Built by John W. Harms ##
# Version 0.01 -- Initial Build ##
# Version 0.02 -- Refactored to be added as module to different project ##

import math
import datetime


# Constants
mu = 398600.000000000000000000000
radSec2degDay = 4950355.35


def DriftDvCalc(DriftDvCurrentDriftRate, DriftDvTargetDriftRate):
    DriftDvCalc_w = 0.0000729211585530  # rad/sol sec
    DriftDvCalc_SVd = DriftDvCurrentDriftRate / radSec2degDay
    DriftDvCalc_SVa = math.pow(((mu) / (math.pow((DriftDvCalc_SVd + DriftDvCalc_w), 2))), (1.00000 / 3.00000))
    DriftDvCalc_Targd = DriftDvTargetDriftRate / radSec2degDay
    DriftDvCalc_Targa = math.pow(((mu) / (math.pow((DriftDvCalc_Targd + DriftDvCalc_w), 2))), (1.00000 / 3.00000))
    DriftDvCalc_Orb1 = DriftDvCalc_SVa + 0.000000000000000000000
    DriftDvCalc_Orb2 = DriftDvCalc_Targa + 0.000000000000000000000
    DriftDvCalc_xferSMA = ((DriftDvCalc_Orb1 + DriftDvCalc_Orb2) / 2)
    DriftDvCalc_SpMechEngy = ((-1) * ((mu / (DriftDvCalc_xferSMA * 2))))
    DriftDvCalc_Orb1Engy = ((-1) * ((mu / (DriftDvCalc_Orb1 * 2))))
    DriftDvCalc_Orb1Vel = math.sqrt(2 * ((mu / DriftDvCalc_Orb1) + DriftDvCalc_Orb1Engy))
    DriftDvCalc_xferVel1 = math.sqrt(2 * ((mu / DriftDvCalc_Orb1) + DriftDvCalc_SpMechEngy))
    DriftDvCalc_dV1 = (math.fabs(DriftDvCalc_xferVel1 - DriftDvCalc_Orb1Vel))*1000
    DriftDvCalc_xferVel2 = math.sqrt(2 * ((mu / DriftDvCalc_Orb2) + DriftDvCalc_SpMechEngy))
    DriftDvCalc_Orb2Engy = ((-1) * ((mu / (DriftDvCalc_Orb2 * 2))))
    DriftDvCalc_Orb2Vel = math.sqrt(2 * ((mu / DriftDvCalc_Orb2) + DriftDvCalc_Orb2Engy))
    DriftDvCalc_dV2 = (math.fabs(DriftDvCalc_Orb2Vel - DriftDvCalc_xferVel2))*1000
    DriftDvCalc_dVcombo = (DriftDvCalc_dV1 + DriftDvCalc_dV2)
    DriftDvCalc_TOF = (math.pi * math.sqrt((math.pow(DriftDvCalc_xferSMA, 3)) / mu))
    DriftDvCalc_TOFhms = (datetime.timedelta(seconds=DriftDvCalc_TOF))
    DriftDvCalc_out = "DriftDvCalc Transfer elements are: " \
                      "\nStarting SMA: %.3f KM\nTarget SMA: %.3f KM\nDelta-V 1:  %.3f m/s " \
                      "\nDelta-V 2:  %.3f m/s \nDelta-V Combined: %.3f m/s " \
                      "\nTime of Flight: %.1f seconds \nTime of Flight: %s hh:mm:ss.ms" \
                      % (DriftDvCalc_Targa, DriftDvCalc_SVa, DriftDvCalc_dV1, DriftDvCalc_dV2,
                         DriftDvCalc_dVcombo, DriftDvCalc_TOF, DriftDvCalc_TOFhms)
    return DriftDvCalc_out
