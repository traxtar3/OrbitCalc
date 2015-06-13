# Built by John W. Harms ##
# Version 0.01 -- Initial Build ##
# Version 0.02 -- Refactored to be added as module to different project ##

import math


# noinspection PyPep8Naming
def MaxRSS(MaxRSSVehicleSemiMajorAxis, MaxRSSTargetSemiMajorAxis, MaxRSSLongitudeDifferance,
           MaxRSSVehicleInclination, MaxRSSTargetInclination):
    SVSma = MaxRSSVehicleSemiMajorAxis + 0.0000000000
    TargSma = MaxRSSTargetSemiMajorAxis + 0.0000000000
    LongDiff = MaxRSSLongitudeDifferance + 0.0000000000
    SVIncl = MaxRSSVehicleInclination + 0.0000000000
    TargIncl = MaxRSSTargetInclination + 0.0000000000
    kmIntrack = (SVSma * 2) * math.sin((math.radians(LongDiff / 2)))
    kmSVCrossTrack = (SVSma * 2) * math.sin((math.radians(SVIncl / 2)))
    kmTargCrossTrack = (SVSma * 2) * math.sin((math.radians(TargIncl / 2)))
    kmCrossTrackDiff = math.fabs(kmSVCrossTrack + kmTargCrossTrack)
    kmRadDiff = math.fabs(SVSma - TargSma)
    WorstRSS = math.sqrt(
        (math.pow(kmRadDiff, 2)) + (math.pow(kmCrossTrackDiff, 2)) + (math.pow(kmIntrack, 2)))
    BestRSS = math.sqrt((math.pow(kmRadDiff, 2)) + (math.pow(kmIntrack, 2)))
    MaxRSS_out = ("Worst Case Max Distance: %.3f Km \nBest Case Max Distance: %.3f Km" % (WorstRSS, BestRSS))
    return MaxRSS_out
