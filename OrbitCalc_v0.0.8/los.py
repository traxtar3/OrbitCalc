
import math
from datetime import datetime
import cities



degrees_per_radian = 180.0 / math.pi


def los(site_selected, tle_line1, tle_line2, timeset):
    try:
        import ephem
    except ImportError:
        return "Tab not supported in this version. PyEphem module not installed"
    else:
        pass

    sl = cities.location[site_selected]
    home = ephem.Observer()
    home.lon = sl[1]
    home.lat = sl[0]
    home.elev = sl[2]
    vehicle = ephem.readtle('Vehicle', tle_line1, tle_line2)
    # home.date = datetime.utcnow()
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
    print "date:", home.date
    print "az:", vehicle.az
    print "el:", vehicle.alt
    print "vehicle lat:", (vehicle.sublat* degrees_per_radian)
    print "vehicle long:", (vehicle.sublong * degrees_per_radian)
    # print tle_line1.count()

    if vehicle.alt < 0:
        los_output = "Vehicle is below the horizon\n" \
                     "Vehicle: azimuth %5.1f deg, elevation %4.1f deg\nRange: %.0f Km\nVehicle Latitude: %5.1f %s\n" \
                     "Vehicle Longitude: %5.1f %s" % (vehicle.az * degrees_per_radian, vehicle.alt * degrees_per_radian,
                                                      vrange, math.fabs(vehicle.sublat * degrees_per_radian), ns,
                                                      math.fabs(vehicle.sublong * degrees_per_radian), ew)
    else:
        los_output = "Vehicle: Azimuth %5.1f deg, Elevation %4.1f deg\nRange: %.0f Km\nVehicle Latitude: %5.1f %s\n" \
                     "Vehicle Longitude: %5.1f %s" % (vehicle.az * degrees_per_radian, vehicle.alt * degrees_per_radian,
                                                      vrange, math.fabs(vehicle.sublat * degrees_per_radian), ns,
                                                      math.fabs(vehicle.sublong * degrees_per_radian), ew)
    return los_output



    #  backed up
    #
    # home = ephem.Observer()
    # home.lon = '-122.63'   # +E
    # home.lat = '45.56'      # +N
    # home.elevation = 80 # meters
    #
    # # Always get the latest ISS TLE data from:
    # # http://spaceflight.nasa.gov/realdata/sightings/SSapplications/Post/JavaSSOP/orbit/ISS/SVPOST.html
    # iss = ephem.readtle(name, tle_line1, tle_line2)
    #
    #
    # iss = ephem.readtle('ISS',
    #     '1 25544U 98067A   11290.51528320  .00016717  00000-0  10270-3 0  9006',
    #     '2 25544  51.6378 264.9380 0016170 337.7557  22.2896 15.60833726 20019'
    # )
    # home.date = datetime.utcnow()
    # iss.compute(home)
    # los_output = ('iss: altitude %4.1f deg, azimuth %5.1f deg' % (iss.alt * degrees_per_radian, iss.az * degrees_per_radian))
    # time.sleep(1.0)
    # return los_output

#los()

