# Built by John W. Harms ##
# Version 0.0.1 -- Initial Build ##
# Version 0.1.0 -- overhauled to use other RV2COE
# Last Change 12 June 15

from sgp4.earth_gravity import wgs84
from sgp4.io import twoline2rv
import datetime
from RV2COE import rv2coe

mu = 398600.4415

def tlekep(tle_line1, tle_line2, timeset):
    t = datetime.datetime.strptime(timeset, "%Y-%m-%d %H:%M:%S.%f")
    satellite = twoline2rv(tle_line1, tle_line2, wgs84)
    position, velocity = satellite.propagate(int(t.year), int(t.month), int(t.day),
                                             int(t.hour), int(t.minute), int(t.second))

    rv2coe_out = rv2coe(position, velocity)
    totalout = "Time: %s\n%s" % (timeset, rv2coe_out)

    return totalout
