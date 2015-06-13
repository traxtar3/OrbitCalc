# Built by John W. Harms ##
# Version 0.01 -- Initial Build ##
# Version 0.02 -- Refactored to be added as module to different project ##

import math

# Constants
mu = 398600.000000000000000000000


def RV2COE(rI_Input, rJ_Input, rK_Input, vI_Input, vJ_Input, vK_Input):
    rI = rI_Input + 0.000000000000000000000
    rJ = rJ_Input + 0.000000000000000000000
    rK = rK_Input + 0.000000000000000000000
    vI = vI_Input + 0.000000000000000000000
    vJ = vJ_Input + 0.000000000000000000000
    vK = vK_Input + 0.000000000000000000000

    rVector = math.sqrt((math.pow(rI, 2)) + (math.pow(rJ, 2)) + (math.pow(rK, 2)))
    vVector = math.sqrt((math.pow(vI, 2)) + (math.pow(vJ, 2)) + (math.pow(vK, 2)))
    math.sqrt((math.pow(rI, 2)) + (math.pow(rJ, 2)) + (math.pow(rK, 2)))

    crossI = (rJ * vK) - (vJ * rK)
    crossJ = (rI * vK) - (vI * rK)
    crossK = (rI * vJ) - (vI * rJ)
    crossVector = math.sqrt(
        (math.pow(crossI, 2)) + (math.pow(crossJ, 2)) + (math.pow(crossK, 2)))

    dotI = (rI * vI)
    dotJ = (rJ * vJ)
    dotK = (rK * vK)
    dotVector = (dotI + dotJ + dotK)

    nI = crossI
    nJ = crossJ
    nK = 0
    nVector = math.sqrt((math.pow(nI, 2)) + (math.pow(nJ, 2)) + (math.pow(nK, 2)))
    eI = ((1 / mu) * (((((math.pow(vVector, 2))) - (mu / rVector))) * rI) - (
        (1 / mu) * (dotVector * vI)))
    eJ = ((1 / mu) * (((((math.pow(vVector, 2))) - (mu / rVector))) * rJ) - (
        (1 / mu) * (dotVector * vJ)))
    eK = ((1 / mu) * (((((math.pow(vVector, 2))) - (mu / rVector))) * rK) - (
        (1 / mu) * (dotVector * vK)))
    eVector = math.sqrt((math.pow(eI, 2)) + (math.pow(eJ, 2)) + (math.pow(eK, 2)))
    spMechEn = (((math.pow(vVector, 2)) / 2) - (mu / rVector))

    # SemiMajor Axis
    semiMajorAxis = (-1) * (mu / (2 * spMechEn))
    # Eccentricity
    ecc = eVector
    # Inclination
    if (math.degrees(math.acos(crossK / crossVector))) < 180:
        incl = math.degrees(math.acos(crossK / crossVector))
    else:
        incl = 180 - math.degrees(math.acos(crossK / crossVector))
    # RAAN
    if nVector < 0:
        raan = math.degrees(math.acos(nJ / nVector))
    else:
        raan = 360 - (math.degrees(math.acos(nJ / nVector)))
    # Argument of Perigee
    if eK > 0:
        aPer = (math.degrees(math.acos(
            ((nJ * eI) + (nI * eJ) + (nK * eK)) / (
                nVector * ecc))))
    else:
        aPer = (360 - math.degrees(math.acos(
            ((nJ * eI) + (nI * eJ) + (nK * eK)) / (
                nVector * ecc))))
    # True Anomaly
    if dotVector > 0:
        trueAnom = math.degrees(math.acos((((eI * rI) + (eJ * rJ) + (
            eK * rK)) / (eVector * rVector))))
    else:
        trueAnom = 360 - math.degrees(math.acos((((eI * rI) + (eJ * rJ) + (
            eK * rK)) / (eVector * rVector))))
    RV2COE_out = ("Semi-Major Axis: %.3f Km\nEccentricity: %1.5f \nInclination: %.3f deg"
                  "\nRAAN: %.3f deg\nArgument of Perigee: %.3f deg\nTrue Anomaly: %.3f deg"
                  % (semiMajorAxis, ecc, incl, raan, aPer, trueAnom))
    return RV2COE_out
