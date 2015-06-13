# Built by John W. Harms ##
# Version 0.01 -- Initial Build ##
# Version 0.02 -- Refactored to be added as module to different project ##
# Version 0.09 -- fixed bug
# Last Change 08 June 15
# Constants
sidreal = 86164.09052400000000000  # seconds ( 23:56:04.090524 )


# noinspection PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming
def Rate2Arrive(Rate2ArriveHowManyDegreesAway, Rate2ArriveHowmanyDaystoArrive):
    Rate2Arrive_AngDist = Rate2ArriveHowManyDegreesAway
    Rate2Arrive_Days = Rate2ArriveHowmanyDaystoArrive
    Rate2Arrive_halfDaySeconds = (sidreal / 2)
    Rate2Arrive_early = Rate2Arrive_AngDist / (Rate2Arrive_Days * (sidreal - Rate2Arrive_halfDaySeconds)) * sidreal
    Rate2Arrive_ontime = Rate2Arrive_AngDist / (Rate2Arrive_Days * (sidreal)) * sidreal
    Rate2Arrive_late = Rate2Arrive_AngDist / (Rate2Arrive_Days * (sidreal + Rate2Arrive_halfDaySeconds)) * sidreal
    Rate2Arrive_ahead = Rate2ArriveHowmanyDaystoArrive - 1
    Rate2Arrive_out = "To arrive in %09.7f day(s) and 12 hours, drift at %09.7f deg/day " \
                      "\nTo arrive on time, drift at %09.7f deg/day " \
                      "\nTo arrive in %09.7f day(s) and 12 hours, drift at %09.7f deg/day" \
                      % (Rate2Arrive_ahead, Rate2Arrive_early, Rate2Arrive_ontime,
                         Rate2ArriveHowmanyDaystoArrive, Rate2Arrive_late)
    return Rate2Arrive_out
