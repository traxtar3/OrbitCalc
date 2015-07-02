# Built by John W. Harms ##
# Version 0.01 -- Initial Build ##
# Version 0.02 -- Refactored to be added as module to different project ##
# Last Change 02 Jul 15

# Original Code from http://www.sharebrained.com/2011/10/18/track-the-iss-pyephem/

import math
import cities

degrees_per_radian = 180.0 / math.pi


def los(site_selected, tle_line1, tle_line2, timeset):
    try:
        import ephem
    except ImportError:
        return "Operation not supported in this version.\nPyEphem module not installed.\nCheck again later"
    else:
        pass

    sl = cities.location[site_selected]
    home = ephem.Observer()
    home.lon = sl[1]
    home.lat = sl[0]
    home.elev = sl[2]
    vehicle = ephem.readtle('Vehicle', tle_line1, tle_line2)
    home.date = timeset
    vehicle.compute(home)
    if vehicle.sublat > 0:
        ns = "N"
    else:
        ns = "S"
    if vehicle.sublong > 0:
        ew = "E"
    else:
        ew = "W"
    vrange = vehicle.range / 1000
    if vehicle.alt < 0:
        los_output = "Vehicle is below the horizon\n" \
                     "Vehicle: azimuth %5.1f deg, elevation %4.1f deg\nRange: %.0f Km\nVehicle Latitude: %5.1f %s\n" \
                     "Vehicle Longitude: %5.1f %s" % (vehicle.az * degrees_per_radian, vehicle.alt * degrees_per_radian,
                                                      vrange, math.fabs(vehicle.sublat * degrees_per_radian), ns,
                                                      math.fabs(vehicle.sublong * degrees_per_radian), ew)
    else:
        los_output = "Time: %s\nVehicle: Azimuth %5.1f deg, Elevation %4.1f deg\nRange: %.0f Km\nVehicle Latitude: %5.1f %s\n" \
                     "Vehicle Longitude: %5.1f %s" % (timeset, vehicle.az * degrees_per_radian, vehicle.alt * degrees_per_radian,
                                                      vrange, math.fabs(vehicle.sublat * degrees_per_radian), ns,
                                                      math.fabs(vehicle.sublong * degrees_per_radian), ew)
    return los_output
