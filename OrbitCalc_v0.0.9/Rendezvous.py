# Built by John W. Harms ##
# Version 0.01 -- Initial Build ##
# Version 0.02 -- Refactored to be added as module to different project ##

# Last Change 08 June 15

import math
import datetime

# Constants
mu = 398600.000000000000000000000


def Rendezvous(RendezvousInterceptRadius, RendezvousTargetRadius, RendezvousAngularSeperation):
    intRad = RendezvousInterceptRadius + 0.0000000000
    targRad = RendezvousTargetRadius + 0.0000000000
    angle = RendezvousAngularSeperation + 0.0000000000
    intAngle = angle * (math.pi / 180)
    xferSMA = (intRad + targRad) / 2
    TOF = math.pi * (math.sqrt((math.pow(xferSMA, 3)) / mu))
    intAngVel = math.sqrt(mu / (math.pow(intRad, 3)))
    # noinspection PyPep8Naming
    targAngVel = math.sqrt(mu / (math.pow(targRad, 3)))
    leadAngle = targAngVel * TOF
    phaseAngle = math.pi - leadAngle
    wait = (phaseAngle - intAngle) / (targAngVel - intAngVel)
    waitHms = (datetime.timedelta(seconds=wait))
    SpMechEngy = ((-1) * ((mu / (xferSMA * 2))))
    Orb1Engy = ((-1) * ((mu / (intRad * 2))))
    Orb1Vel = math.sqrt(2 * ((mu / intRad) + Orb1Engy))
    xferVel1 = math.sqrt(2 * ((mu / intRad) + SpMechEngy))
    dV1 = math.fabs(xferVel1 - Orb1Vel)
    xferVel2 = math.sqrt(2 * ((mu / targRad) + SpMechEngy))
    Orb2Engy = ((-1) * ((mu / (targRad * 2))))
    Orb2Vel = math.sqrt(2 * ((mu / targRad) + Orb2Engy))
    dV2 = math.fabs(Orb2Vel - xferVel2)
    dVcombo = (dV1 + dV2)
    TOFhms = (datetime.timedelta(seconds=TOF))
    Rendezvous_out = "Rendezvous Transfer elements are: \nDelta-V 1:  %.5f m/s\nDelta-V 2: %.5f m/s" \
                     "\nDelta-V Combined: %.5f  m/s\nTime of Flight: %.1f sec\nTime of Flight: %s hh:mm:ss.ms " \
                     "\nWait Time: %.1f sec\nWait Time: %s hh:mm:ss.ms" \
                     % (dV1 * 1000, dV2 * 1000, dVcombo * 1000, TOF, TOFhms, wait, waitHms)
    return Rendezvous_out
