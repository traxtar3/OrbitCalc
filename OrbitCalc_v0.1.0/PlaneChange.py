# Built by John W. Harms ##
# Version 0.01 -- Initial Build ##
# Version 0.02 -- Refactored to be added as module to different project ##
# Last Change 08 June 15

import math
# Constants
mu = 398600.000000000000000000000

def PlaneChange(PlaneChangeOrbitRadius, PlaneChangeInitialInclination, PlaneChangeFinalInclination):
    OrbRad = PlaneChangeOrbitRadius + 0.0000000000
    Ii = PlaneChangeInitialInclination + 0.0000000000
    If = PlaneChangeFinalInclination + 0.0000000000
    SpMechEngy = ((-1) * (mu / (OrbRad * 2)))
    InitOrbVel = math.sqrt(2 * ((mu / OrbRad) + SpMechEngy))
    PlaneChg = math.fabs(If - Ii)
    dVsimple = (2 * (InitOrbVel) * (math.sin((PlaneChg * math.pi / 180) / 2)))*1000
    PlaneChange_out = "Total Inclination Change: %.2f deg " \
                      "\nDeltaV Simple: %.3f m/s" % (PlaneChg, dVsimple)
    return PlaneChange_out
