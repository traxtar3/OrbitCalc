# Built by John W. Harms ##
# Version 0.01 -- Initial Build ##
# Version 0.02 -- Refactored to be added as module to different project ##

import math
import datetime

# Constants
mu = 398600.000000000000000000000
deg2km = 737.918151127

def Hohman(HohmanOrbit1_Input, HohmanOrbit2_Input):
    # You have to add some significant digits to get Python to properly compute REALLY small numbers
    Orb1 = HohmanOrbit1_Input + 0.000000000000000000000
    Orb2 = HohmanOrbit2_Input + 0.000000000000000000000
    xferSMA = ((Orb1 + Orb2) / 2)
    SpMechEngy = ((-1) * ((mu / (xferSMA * 2))))
    Orb1Engy = ((-1) * ((mu / (Orb1 * 2))))
    Orb1Vel = math.sqrt(2 * ((mu / Orb1) + Orb1Engy))
    xferVel1 = math.sqrt(2 * ((mu / Orb1) + SpMechEngy))
    dV1 = (math.fabs(xferVel1 - Orb1Vel)) * 1000
    xferVel2 = math.sqrt(2 * ((mu / Orb2) + SpMechEngy))
    Orb2Engy = ((-1) * ((mu / (Orb2 * 2))))
    Orb2Vel = math.sqrt(2 * ((mu / Orb2) + Orb2Engy))
    dV2 = (math.fabs(Orb2Vel - xferVel2)) *1000
    dVcombo = (dV1 + dV2)
    TOF = (math.pi * math.sqrt((math.pow(xferSMA, 3)) / mu))
    TOFhms = datetime.timedelta(seconds=TOF)
    Hohman_out = ("Hohman Transfer elements are: \nDelta-V 1: %.2f m/s \nDelta-V 2: %.2f  m/s "
                  "\nDelta-V Combined: %.2f  m/s\nTime of Flight: %.1f seconds \nTime of Flight: %s hh:mm:ss.ms"
                  % (dV1, dV2, dVcombo, TOF, TOFhms))
    return Hohman_out