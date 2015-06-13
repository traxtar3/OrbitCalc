from math import (acos, asinh, atan2, copysign, cos, fabs, fmod,
                  pi, sin, sinh, sqrt, tan)
from datetime import datetime
from sgp4.earth_gravity import wgs84
from sgp4.io import twoline2rv



# r = [42164, 0, 0]
# v = [0, 0, -3.0747]

#r = [-26811.804312763237, -32974.87361092998, 2016.17279659361]
#v = [2.3680716296404896, -1.933259141153603, -0.134203491989653]



#
#
#
# line1 = ('1 25544U 98067A   15159.73191137  .00006600  00000-0  10229-3 0  9992')
# line2 = ('2 25544  51.6431 126.2443 0004739  37.0689  24.1172 15.55345846946721')
#
# satellite = twoline2rv(line1, line2, wgs84)
# position, velocity = satellite.propagate(2015, 06, 12, 00, 00, 00)
#
# # print(satellite.error)    # nonzero on error
# # 0
# # print(satellite.error_message)
# # None
# print(position)
# # (5576.056952..., -3999.371134..., -1521.957159...)
# print(velocity)
# # (4.772627..., 5.119817..., 4.275553...)
# r = (position)
# v = (velocity)




undefined = None
mu = 398600.000000

# def RV2COE(rI_Input, rJ_Input, rK_Input, vI_Input, vJ_Input, vK_Input):
#     rI = rI_Input + 0.000000000000000000000
#     rJ = rJ_Input + 0.000000000000000000000
#     rK = rK_Input + 0.000000000000000000000
#     vI = vI_Input + 0.000000000000000000000
#     vJ = vJ_Input + 0.000000000000000000000
#     vK = vK_Input + 0.000000000000000000000
#
#


def mag(x):
    return sqrt(x[0]*x[0] + x[1]*x[1] + x[2]*x[2])

def cross(vec1, vec2, outvec):
    outvec[0]= vec1[1]*vec2[2] - vec1[2]*vec2[1]
    outvec[1]= vec1[2]*vec2[0] - vec1[0]*vec2[2]
    outvec[2]= vec1[0]*vec2[1] - vec1[1]*vec2[0]

def dot(x, y):
    return (x[0]*y[0] + x[1]*y[1] + x[2]*y[2])

def angle(vec1, vec2):

    small     = 0.00000001
    undefined = 999999.1

    magv1 = mag(vec1)
    magv2 = mag(vec2)

    if magv1*magv2 > small*small:

        temp= dot(vec1,vec2) / (magv1*magv2)
        if fabs(temp) > 1.0:
            temp = copysign(1.0, temp)
        return acos( temp )

    else:
        return undefined

def newtonnu(ecc, nu):

    #  ---------------------  implementation   ---------------------
    e0= 999999.9
    m = 999999.9
    small = 0.00000001

    #  --------------------------- circular ------------------------
    if fabs(ecc) < small:

        m = nu
        e0= nu

    else:
        #  ---------------------- elliptical -----------------------
        if ecc < 1.0-small:

            sine= ( sqrt( 1.0 -ecc*ecc ) * sin(nu) ) / ( 1.0 +ecc*cos(nu) )
            cose= ( ecc + cos(nu) ) / ( 1.0  + ecc*cos(nu) )
            e0  = atan2( sine,cose )
            m   = e0 - ecc*sin(e0)

        else:
            #  -------------------- hyperbolic  --------------------
            if ecc > 1.0 + small:

                if ecc > 1.0 and fabs(nu)+0.00001 < pi-acos(1.0 /ecc):

                    sine= ( sqrt( ecc*ecc-1.0  ) * sin(nu) ) / ( 1.0  + ecc*cos(nu) )
                    e0  = asinh( sine )
                    m   = ecc*sinh(e0) - e0

            else:
                #  ----------------- parabolic ---------------------
                if fabs(nu) < 168.0*pi/180.0:

                    e0= tan( nu*0.5  )
                    m = e0 + (e0*e0*e0)/3.0

    if ecc < 1.0:

        m = fmod( m,2.0 *pi )
        if m < 0.0:
            m = m + 2.0 *pi
        e0 = fmod( e0,2.0 *pi )

    return e0, m

def rv2coe(r, v, mu):

    hbar = [None, None, None]
    nbar = [None, None, None]
    ebar = [None, None, None]
    typeorbit = [None, None, None]

    twopi  = 2.0 * pi
    halfpi = 0.5 * pi
    small  = 0.00000001
    undefined = 999999.1
    infinite  = 999999.9

    #  -------------------------  implementation   -----------------
    magr = mag( r )
    magv = mag( v )

    #  ------------------  find h n and e vectors   ----------------
    cross( r,v, hbar )
    magh = mag( hbar )
    if magh > small:

        nbar[0]= -hbar[1]
        nbar[1]=  hbar[0]
        nbar[2]=   0.0
        magn = mag( nbar )
        c1 = magv*magv - mu /magr
        rdotv = dot( r,v )
        for i in range(0, 3):
            ebar[i]= (c1*r[i] - rdotv*v[i])/mu
        ecc = mag( ebar )

        #  ------------  find a e and semi-latus rectum   ----------
        sme= ( magv*magv*0.5  ) - ( mu /magr )
        if fabs( sme ) > small:
            a= -mu  / (2.0 *sme)
        else:
            a= infinite
        p = magh*magh/mu

        #  -----------------  find inclination   -------------------
        hk= hbar[2]/magh
        incl= acos( hk )

        #  --------  determine type of orbit for later use  --------
        #  ------ elliptical, parabolic, hyperbolic inclined -------
        typeorbit = 'ei'
        if ecc < small:

            #  ----------------  circular equatorial ---------------
            if  incl < small or fabs(incl-pi) < small:
                typeorbit = 'ce'
            else:
                #  --------------  circular inclined ---------------
                typeorbit = 'ci'

        else:

            #  - elliptical, parabolic, hyperbolic equatorial --
            if incl < small or fabs(incl-pi) < small:
                typeorbit = 'ee'

        #  ----------  find longitude of ascending node ------------
        if magn > small:

            temp= nbar[0] / magn
            if fabs(temp) > 1.0:
                temp = copysign(1.0, temp)
            omega= acos( temp )
            if nbar[1] < 0.0:
                omega= twopi - omega

        else:
            omega= undefined

        #  ---------------- find argument of perigee ---------------
        if typeorbit == 'ei':

            argp = angle( nbar,ebar)
            if ebar[2] < 0.0:
                argp= twopi - argp

        else:
            argp= undefined

        #  ------------  find true anomaly at epoch    -------------
        if typeorbit[0] == 'e':

            nu =  angle( ebar,r)
            if rdotv < 0.0:
                nu= twopi - nu

        else:
            nu= undefined

        #  ----  find argument of latitude - circular inclined -----
        if typeorbit == 'ci':

            arglat = angle( nbar,r )
            if r[2] < 0.0:
                arglat= twopi - arglat
            m = arglat

        else:
            arglat= undefined

        #  -- find longitude of perigee - elliptical equatorial ----
        if ecc > small and typeorbit == 'ee':

            temp= ebar[0]/ecc
            if fabs(temp) > 1.0:
                temp = copysign(1.0, temp)
            lonper= acos( temp )
            if ebar[1] < 0.0:
                lonper= twopi - lonper
            if incl > halfpi:
                lonper= twopi - lonper

        else:
            lonper= undefined

        #  -------- find true longitude - circular equatorial ------
        if magr > small and typeorbit == 'ce':

            temp= r[0]/magr
            if fabs(temp) > 1.0:
                temp = copysign(1.0, temp)
            truelon= acos( temp )
            if r[1] < 0.0:
                truelon= twopi - truelon
            if incl > halfpi:
                truelon= twopi - truelon
            m = truelon

        else:
            truelon= undefined

        #  ------------ find mean anomaly for all orbits -----------
        if typeorbit[0] == 'e':
            e, m = newtonnu(ecc, nu)

    else:
        p    = undefined
        a    = undefined
        ecc  = undefined
        incl = undefined
        omega= undefined
        argp = undefined
        nu   = undefined
        m    = undefined
        arglat = undefined
        truelon= undefined
        lonper = undefined

    if incl == 999999.1:
        incl = "undefined"
    else:
        incl = "%s deg" % (incl*180/pi)
    if omega == 999999.1:
        omega = "undefined"
    else:
        omega= "%s deg" % (omega*180/pi)
    if argp == 999999.1:
        argp = "undefined"
    else:
        argp = "%s deg" % (argp*180/pi)
    if nu == 999999.1:
        nu = "undefined"
    else:
        nu = "%s deg" % (nu*180/pi)

    printout = "Semi-Major Axis: %s Km\nEccentricty: %s\nInclination: %s\nRAAN: %s\nArgument of Perigee: %s" \
                "\nTrue Anomaly: %s" % (a, ecc, incl, omega, argp, nu)
    print datetime.utcnow()
    return printout
