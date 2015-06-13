
import math
from datetime import datetime
import ephem
import cities

degrees_per_radian = 180.0 / math.pi


def los(site_selected, tle_line1, tle_line2):

    sl = cities.location[site_selected]

    home = ephem.Observer()
    home.lon = sl[0]
    home.lat = sl[1]
    home.elev = 0

    vehicle = ephem.readtle('Vehicle', tle_line1, tle_line2)
    home.date = datetime.utcnow()
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
    print "date:", home.date
    print "az:", vehicle.az
    print "el:", vehicle.alt
    print "vehicle lat:", (vehicle.sublat* degrees_per_radian)
    print "vehicle long:", (vehicle.sublong * degrees_per_radian)

    if vehicle.alt < 0:
        los_output = "Vehicle is below the horizon\nVehicle: azimuth %5.1f deg, elevation %4.1f deg\nRange: %.0f Km\nVehicle Latitude: %5.1f %s\nVehicle Longitude: %5.1f %s"\
                     % (vehicle.az * degrees_per_radian, vehicle.alt * degrees_per_radian, vrange, math.fabs(vehicle.sublat * degrees_per_radian), ns, math.fabs(vehicle.sublong * degrees_per_radian), ew)
    else:
        los_output = "Vehicle: Azimuth %5.1f deg, Elevation %4.1f deg\nRange: %.0f Km\nVehicle Latitude: %5.1f %s\nVehicle Longitude: %5.1f %s"\
                     % (vehicle.az * degrees_per_radian, vehicle.alt * degrees_per_radian, vrange, math.fabs(vehicle.sublat * degrees_per_radian), ns, math.fabs(vehicle.sublong * degrees_per_radian), ew)
    return los_output
