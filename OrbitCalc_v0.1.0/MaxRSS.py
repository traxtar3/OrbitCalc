# Built by John W. Harms ##
# Version 0.01 -- Initial Build ##
# Version 0.02 -- Refactored to be added as module to different project ##

# Last Change 10 June 15

import math

sidreal = 86164.090524

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
    SvVel_ms = ((((SVSma * math.pi * 2) / 360) * SVIncl) / (sidreal/4)) * 1000
    TargtVel_ms = ((((TargSma * math.pi * 2) / 360) * TargIncl) / (sidreal/4)) * 1000
    SvVel_kmh = ((((SVSma * math.pi * 2) / 360) * SVIncl) / (sidreal/4)) * 60
    TargtVel_kmh = ((((TargSma * math.pi * 2) / 360) * TargIncl) / (sidreal/4)) * 60
    MaxRSS_out = ("Worst Case Max Distance: %09.7f Km \nBest Case Max Distance: %09.7f Km"
                  "\nVehicle 1 Cross Track Velocity @ node %1.5f m/s\nVehicle 2 Cross Track Velocity @ node %1.5f m/s"
                  "\nVehicle 1 Cross Track Velocity @ node %1.5f km/h\nVehicle 2 Cross Track Velocity @ node %1.5f km/h"
                  % (WorstRSS, BestRSS, SvVel_ms, TargtVel_ms, SvVel_kmh, TargtVel_kmh))
    return MaxRSS_out
