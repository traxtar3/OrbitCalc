# Built by John W. Harms ##
# Version 0.0.1 -- Initial Build ##
# Last Change 2 July 15

from numpy import linalg, arange, copy, dot
from math import fabs as abs
from math import (pi, sqrt, floor)
import datetime
from RV2COE import rv2coe

# I really have no idea what is going on here.....but it works...
# Code originally from matlab located here:
# http://www.mathworks.com/matlabcentral/fileexchange/48723-matlab-functions-for-two-body-orbit-propagation
# Origial Matlab Code is copyrighted to David Eagle, under BSD open source license

def twobody2(starttime, stoptime, ri, vi):
    t_start = datetime.datetime.strptime(starttime, "%Y-%m-%d %H:%M:%S.%f")
    t_end = datetime.datetime.strptime(stoptime, "%Y-%m-%d %H:%M:%S.%f")
    tau = (t_end - t_start).total_seconds()
    mu = 398600.4415
    tolerance = 1e-12
    u = 0
    imax = 20
    orbits = 0
    tdesired = copy(tau)
    threshold = tolerance * abs(tdesired)
    r0 = linalg.norm(ri)
    n0 = dot(ri,vi)
    beta = 2 * (mu / r0) - dot(vi,vi)
    if beta != 0:
        umax=+ 1 / sqrt(abs(beta))
        umin=- 1 / sqrt(abs(beta))
    if beta > 0:
        orbits = beta * tau - 2 * n0
        orbits = 1 + (orbits * sqrt(beta)) / (pi * mu)
        orbits = floor(orbits / 2)
    for i in arange(1,imax,1).reshape(-1):
        q = beta * u * u
        q = q / (1 + q)
        n = 0
        r = 1
        l = 1
        s = 1
        d = 3
        gcf = 1
        k = - 5
        gold = 0

        while (gcf != gold):
            k = - k
            l = l + 2
            d = d + 4 * l
            n = n + (1 + k) * l
            r = d / (d - n * r * q)
            s = (r - 1) * s
            gold = copy(gcf)
            gcf = gold + s

        h0 = 1 - 2 * q
        h1 = 2 * u * (1 - q)
        u0 = 2 * h0 * h0 - 1
        u1 = 2 * h0 * h1
        u2 = 2 * h1 * h1
        u3 = 2 * h1 * u2 * gcf / 3

        if orbits != 0:
            u3 = u3 + 2 * pi * orbits / (beta * sqrt(beta))

        r1 = r0 * u0 + n0 * u1 + mu * u2
        dt = r0 * u1 + n0 * u2 + mu * u3
        slope = 4 * r1 / (1 + beta * u * u)
        terror = tdesired - dt

        if abs(terror) < threshold:
            break
        if (i > 1) and (u == uold):
            break
        if (i > 1) and (dt == dtold):
            break

        uold = copy(u)
        dtold = copy(dt)
        ustep = terror / slope

        if ustep > 0:
            umin=copy(u)
            u = u + ustep
            if u > umax:
                u = (umin + umax) / 2
        else:
            umax = copy(u)
            u = u + ustep
            if u < umin:
                u = (umin + umax) / 2
        if i == imax:
            print ('\\n\\nmax iterations in twobody2 function')

    usaved=copy(u)
    f = 1.0 - (mu / r0) * u2
    gg = 1.0 - (mu / r1) * u2
    g = r0 * u1 + n0 * u2
    ff = - mu * u1 / (r0 * r1)
    for i in arange(1):
         posi = f * ri[i] + g * vi[i]
         veli = ff * ri[i] + gg * vi[i]
    for j in arange(2).reshape(-1):
         posj = f * ri[j] + g * vi[j]
         velj = ff * ri[j] + gg * vi[j]
    for k in arange(3).reshape(-1):
         posk = f * ri[k] + g * vi[k]
         velk = ff * ri[k] + gg * vi[k]

    # The final product!
    position = [posi, posj, posk]
    velocity = [veli, velj, velk]

    printout = rv2coe(position,velocity)
    return printout

