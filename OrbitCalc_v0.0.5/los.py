
import math
import time
from datetime import datetime
import ephem

degrees_per_radian = 180.0 / math.pi

def los(site_selected, tle_line1, tle_line2):

    if site_selected =="HTSA":
        print "HTSA"
    else:
        print "False"

    print site_selected
    print tle_line1
    print tle_line1
    return "done"
    #home = ephem.Observer()
    #home.lon = '-122.63'   # +E
    #home.lat = '45.56'      # +N
    #home.elevation = 80 # meters

    ## Always get the latest ISS TLE data from:
    ## http://spaceflight.nasa.gov/realdata/sightings/SSapplications/Post/JavaSSOP/orbit/ISS/SVPOST.html
    #name = "SV1"
    #iss = ephem.readtle(name, tle_line1, tle_line2)


    ##iss = ephem.readtle('ISS',
    ##    '1 25544U 98067A   11290.51528320  .00016717  00000-0  10270-3 0  9006',
    ##    '2 25544  51.6378 264.9380 0016170 337.7557  22.2896 15.60833726 20019'
    ##)
    #home.date = datetime.utcnow()
    #iss.compute(home)
    #los_output = ('iss: altitude %4.1f deg, azimuth %5.1f deg' % (iss.alt * degrees_per_radian, iss.az * degrees_per_radian))
    #time.sleep(1.0)
    #return los_output
    #while True:

#los()

