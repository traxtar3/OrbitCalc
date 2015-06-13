# Built by John W. Harms ##
# Version 0.01 -- Initial Build ##
# Version 0.03 -- Added GUI ##


import math
import datetime
import random
import gtk
import numpy
import numpy.linalg


# Constants
# You have to add some significant digits to get Python to properly compute REALLY small numbers
mu = 398600.000000000000000000000
sidreal = 86164.09052400000000000  # seconds ( 23:56:04.090524 )
sidrealDay = 0.997269566329084
geoSMA = 42164.15405400000000000
radSec2degDay = 4950355.35
deg2km = 737.918151127


def RV2COE(rI_Input, rJ_Input, rK_Input, vI_Input, vJ_Input, vK_Input):
    rI = rI_Input + 0.000000000000000000000
    rJ = rJ_Input + 0.000000000000000000000
    rK = rK_Input + 0.000000000000000000000
    vI = vI_Input + 0.000000000000000000000
    vJ = vJ_Input + 0.000000000000000000000
    vK = vK_Input + 0.000000000000000000000

    rVector = math.sqrt((math.pow(rI, 2)) + (math.pow(rJ, 2)) + (math.pow(rK, 2)))
    vVector = math.sqrt((math.pow(vI, 2)) + (math.pow(vJ, 2)) + (math.pow(vK, 2)))
    math.sqrt((math.pow(rI, 2)) + (math.pow(rJ, 2)) + (math.pow(rK, 2)))

    crossI = (rJ * vK) - (vJ * rK)
    crossJ = (rI * vK) - (vI * rK)
    crossK = (rI * vJ) - (vI * rJ)
    crossVector = math.sqrt(
        (math.pow(crossI, 2)) + (math.pow(crossJ, 2)) + (math.pow(crossK, 2)))

    dotI = (rI * vI)
    dotJ = (rJ * vJ)
    dotK = (rK * vK)
    dotVector = (dotI + dotJ + dotK)

    nI = crossI
    nJ = crossJ
    nK = 0
    nVector = math.sqrt((math.pow(nI, 2)) + (math.pow(nJ, 2)) + (math.pow(nK, 2)))
    eI = ((1 / mu) * (((((math.pow(vVector, 2))) - (mu / rVector))) * rI) - (
        (1 / mu) * (dotVector * vI)))
    eJ = ((1 / mu) * (((((math.pow(vVector, 2))) - (mu / rVector))) * rJ) - (
        (1 / mu) * (dotVector * vJ)))
    eK = ((1 / mu) * (((((math.pow(vVector, 2))) - (mu / rVector))) * rK) - (
        (1 / mu) * (dotVector * vK)))
    eVector = math.sqrt((math.pow(eI, 2)) + (math.pow(eJ, 2)) + (math.pow(eK, 2)))

    angMom = crossVector
    spMechEn = (((math.pow(vVector, 2)) / 2) - (mu / rVector))

    # SemiMajor Axis
    semiMajorAxis = (-1) * (mu / (2 * spMechEn))
    # Eccentricity
    ecc = eVector
    # Inclination
    if (math.degrees(math.acos(crossK / crossVector))) < 180:
        incl = math.degrees(math.acos(crossK / crossVector))
    else:
        incl = 180 - math.degrees(math.acos(crossK / crossVector))
    # RAAN
    if nVector < 0:
        raan = math.degrees(math.acos(nJ / nVector))
    else:
        raan = 360 - (math.degrees(math.acos(nJ / nVector)))
    # Argument of Perigee
    if eK < 0:
        aPer = (math.degrees(math.acos(
            ((nJ * eI) + (nI * eJ) + (nK * eK)) / (
                nVector * ecc))))
    else:
        aPer = (360 - math.degrees(math.acos(
            ((nJ * eI) + (nI * eJ) + (nK * eK)) / (
                nVector * ecc))))
    # True Anomaly
    if dotVector > 0:
        trueAnom = math.degrees(math.acos((((eI * rI) + (eJ * rJ) + (
            eK * rK)) / (eVector * rVector))))
    else:
        trueAnom = 360 - math.degrees(math.acos((((eI * rI) + (eJ * rJ) + (
            eK * rK)) / (eVector * rVector))))
    RV2COE_out = ("Semi-Major Axis: %09.7f \nEccentricity: %09.7f \nInclination: %09.7f \nRAAN: %09.7f \nArgument of Perigee: %09.7f \nTrue Anomaly: %09.7f" % (semiMajorAxis, ecc, incl, raan, aPer, trueAnom))
    return RV2COE_out

def Hohman(HohmanOrbit1_Input, HohmanOrbit2_Input):
    # You have to add some significant digits to get Python to properly compute REALLY small numbers
    Orb1 = HohmanOrbit1_Input + 0.000000000000000000000
    Orb2 = HohmanOrbit2_Input + 0.000000000000000000000
    xferSMA = ((Orb1 + Orb2) / 2)
    SpMechEngy = ((-1) * ((mu / (xferSMA * 2))))
    Orb1Engy = ((-1) * ((mu / (Orb1 * 2))))
    Orb1Vel = math.sqrt(2 * ((mu / Orb1) + Orb1Engy))
    xferVel1 = math.sqrt(2 * ((mu / Orb1) + SpMechEngy))
    dV1 = (math.fabs(xferVel1 - Orb1Vel)) * 1000
    xferVel2 = math.sqrt(2 * ((mu / Orb2) + SpMechEngy))
    Orb2Engy = ((-1) * ((mu / (Orb2 * 2))))
    Orb2Vel = math.sqrt(2 * ((mu / Orb2) + Orb2Engy))
    dV2 = (math.fabs(Orb2Vel - xferVel2)) *1000
    dVcombo = (dV1 + dV2)
    TOF = (math.pi * math.sqrt((math.pow(xferSMA, 3)) / mu))
    TOFhms = datetime.timedelta(seconds=TOF)
    Hohman_out = ("Hohman Transfer elements are: \nDelta-V 1: %09.7f m/s \nDelta-V 2: %09.7f  m/s \nDelta-V Combined: %09.7f \nTime of Flight: %09.7f seconds \nTime of Flight: %s hh:mm:ss.ms" % (dV1, dV2, dVcombo, TOF, TOFhms))
    return Hohman_out

def PlaneChange(PlaneChangeOrbitRadius, PlaneChangeInitialInclination, PlaneChangeFinalInclination):
    OrbRad = PlaneChangeOrbitRadius + 0.0000000000
    Ii = PlaneChangeInitialInclination + 0.0000000000
    If = PlaneChangeFinalInclination + 0.0000000000
    SpMechEngy = ((-1) * (mu / (OrbRad * 2)))
    InitOrbVel = math.sqrt(2 * ((mu / OrbRad) + SpMechEngy))
    PlaneChg = math.fabs(If - Ii)
    dVsimple = (2 * (InitOrbVel) * (math.sin((PlaneChg * math.pi / 180) / 2)))*1000
    PlaneChange_out = "Plane Change: \nTotal Inclination Change: %09.7f deg \nDeltaV Simple: %09.7f m/s" % (PlaneChg, dVsimple)
    return PlaneChange_out

def Rendezvous(RendezvousInterceptRadius, RendezvousTargetRadius, RendezvousAngularSeperation):
    intRad = RendezvousInterceptRadius + 0.0000000000
    targRad = RendezvousTargetRadius + 0.0000000000
    angle = RendezvousAngularSeperation + 0.0000000000
    intAngle = angle * (math.pi / 180)
    xferSMA = (intRad + targRad) / 2
    TOF = math.pi * (math.sqrt((math.pow(xferSMA, 3)) / mu))
    intAngVel = math.sqrt(mu / (math.pow(intRad, 3)))
    targAngVel = math.sqrt(mu / (math.pow(targRad, 3)))
    leadAngle = targAngVel * TOF
    phaseAngle = math.pi - leadAngle
    wait = (phaseAngle - intAngle) / (targAngVel - intAngVel)
    waitHms = (datetime.timedelta(seconds=wait))
    SpMechEngy = ((-1) * ((mu / (xferSMA * 2))))
    Orb1Engy = ((-1) * ((mu / (intRad * 2))))
    Orb1Vel = math.sqrt(2 * ((mu / intRad) + Orb1Engy))
    xferVel1 = math.sqrt(2 * ((mu / intRad) + SpMechEngy))
    dV1 = math.fabs(xferVel1 - Orb1Vel)
    xferVel2 = math.sqrt(2 * ((mu / targRad) + SpMechEngy))
    Orb2Engy = ((-1) * ((mu / (targRad * 2))))
    Orb2Vel = math.sqrt(2 * ((mu / targRad) + Orb2Engy))
    dV2 = math.fabs(Orb2Vel - xferVel2)
    dVcombo = (dV1 + dV2)
    TOFhms = (datetime.timedelta(seconds=TOF))
    Rendezvous_out =  "Rendezvous Transfer elements are: " \
                      "\nDelta-V 1:  %09.7f " \
                      "\nDelta-V 2: %09.7f " \
                      "\nDelta-V Combined: %09.7f " \
                      "\nTime of Flight: %09.7f seconds " \
                      "\nTime of Flight: %s hh:mm:ss.ms " \
                      "\nWait Time: %09.7f " \
                      "\nWait Time: %s hh:mm:ss.ms" \
                      % (dV1, dV2, dVcombo, TOF,
                         TOFhms, wait, waitHms)
    return Rendezvous_out

def SMA2Drift(DriftRelGeo):
    SMA2Drift_sma = geoSMA + DriftRelGeo
    SMA2Drift_n = math.sqrt(mu / (math.pow(SMA2Drift_sma, 3.000000000)))
    SMA2Drift_drift = (-1) * (360 - (SMA2Drift_n * radSec2degDay * sidrealDay))
    if SMA2Drift_sma > geoSMA:
        SMA2Drift_drift = (360 - (SMA2Drift_n * radSec2degDay * sidrealDay))
        SMA2Drift_str = "deg/day West"
    else:
        SMA2Drift_str = "deg/day East"
    SMA2Drift_drift_out = "%09.7f %s" % (SMA2Drift_drift, SMA2Drift_str)
    return SMA2Drift_drift_out

def Drift2SMA(Drift2SMArate):
    Drift2SMA_d = Drift2SMArate / radSec2degDay
    Drift2SMA_w = (0.0000729211585530)  #rad/sol sec
    Drift2SMA_a = math.pow(((mu) / (math.pow((Drift2SMA_d + Drift2SMA_w), 2))), (1.00000 / 3.00000))
    if Drift2SMA_a > 42164.154054:
        Drift2SMA_abvbel = "above"
    else:
        Drift2SMA_abvbel = "below"
    Drift2SMA_aDif = math.fabs(42164.154054 - Drift2SMA_a)
    Drift2SMA_out = "Semi-Major Axis is %09.7f \n %09.7f km %s GEO" % (Drift2SMA_a, Drift2SMA_aDif, Drift2SMA_abvbel)
    return Drift2SMA_out

def MaxRSS(MaxRSSVehicleSemiMajorAxis, MaxRSSTargetSemiMajorAxis, MaxRSSLongitudeDifferance, MaxRSSVehicleInclination, MaxRSSTargetInclination):
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
    MaxRSS_out = ("Worst Case Max Distance: %09.7f Km \nBest Case Max Distance: %09.7f Km" % (WorstRSS, BestRSS))
    return MaxRSS_out

def Rate2Arrive(Rate2ArriveHowManyDegreesAway, Rate2ArriveHowmanyDaystoArrive):
    Rate2Arrive_AngDist = Rate2ArriveHowManyDegreesAway
    Rate2Arrive_Days = Rate2ArriveHowmanyDaystoArrive
    Rate2Arrive_rate = Rate2Arrive_AngDist / Rate2Arrive_Days
    Rate2Arrive_halfDaySeconds = (sidreal / 2)
    Rate2Arrive_early = Rate2Arrive_AngDist / (Rate2Arrive_Days * (sidreal - Rate2Arrive_halfDaySeconds)) * sidreal
    Rate2Arrive_ontime = Rate2Arrive_AngDist / (Rate2Arrive_Days * (sidreal)) * sidreal
    Rate2Arrive_late = Rate2Arrive_AngDist / (Rate2Arrive_Days * (sidreal + Rate2Arrive_halfDaySeconds)) * sidreal
    Rate2Arrive_ahead = Rate2ArriveHowmanyDaystoArrive - 1
    Rate2Arrive_out = "To arrive in %09.7f day(s) and 12 hours, drift at %09.7f deg/day \nTo arrive on time, drift at %09.7f deg/day \nTo arrive in %09.7f day(s) and 12 hours, drift at %09.7f deg/day" \
                      % (Rate2Arrive_ahead, Rate2Arrive_early, Rate2Arrive_ontime,
                         Rate2ArriveHowmanyDaystoArrive, Rate2Arrive_late)
    return Rate2Arrive_out

def DriftDvCalc(DriftDvCurrentDriftRate, DriftDvTargetDriftRate):
    DriftDvCalc_w = 0.0000729211585530  #rad/sol sec
    DriftDvCalc_SVd = DriftDvCurrentDriftRate / radSec2degDay
    DriftDvCalc_SVa = math.pow(((mu) / (math.pow((DriftDvCalc_SVd + DriftDvCalc_w), 2))), (1.00000 / 3.00000))
    DriftDvCalc_Targd = DriftDvTargetDriftRate / radSec2degDay
    DriftDvCalc_Targa = math.pow(((mu) / (math.pow((DriftDvCalc_Targd + DriftDvCalc_w), 2))), (1.00000 / 3.00000))
    DriftDvCalc_Orb1 = DriftDvCalc_SVa + 0.000000000000000000000
    DriftDvCalc_Orb2 = DriftDvCalc_Targa + 0.000000000000000000000
    DriftDvCalc_xferSMA = ((DriftDvCalc_Orb1 + DriftDvCalc_Orb2) / 2)
    DriftDvCalc_SpMechEngy = ((-1) * ((mu / (DriftDvCalc_xferSMA * 2))))
    DriftDvCalc_Orb1Engy = ((-1) * ((mu / (DriftDvCalc_Orb1 * 2))))
    DriftDvCalc_Orb1Vel = math.sqrt(2 * ((mu / DriftDvCalc_Orb1) + DriftDvCalc_Orb1Engy))
    DriftDvCalc_xferVel1 = math.sqrt(2 * ((mu / DriftDvCalc_Orb1) + DriftDvCalc_SpMechEngy))
    DriftDvCalc_dV1 = (math.fabs(DriftDvCalc_xferVel1 - DriftDvCalc_Orb1Vel))*1000
    DriftDvCalc_xferVel2 = math.sqrt(2 * ((mu / DriftDvCalc_Orb2) + DriftDvCalc_SpMechEngy))
    DriftDvCalc_Orb2Engy = ((-1) * ((mu / (DriftDvCalc_Orb2 * 2))))
    DriftDvCalc_Orb2Vel = math.sqrt(2 * ((mu / DriftDvCalc_Orb2) + DriftDvCalc_Orb2Engy))
    DriftDvCalc_dV2 = (math.fabs(DriftDvCalc_Orb2Vel - DriftDvCalc_xferVel2))*1000
    DriftDvCalc_dVcombo = (DriftDvCalc_dV1 + DriftDvCalc_dV2)
    DriftDvCalc_TOF = (math.pi * math.sqrt((math.pow(DriftDvCalc_xferSMA, 3)) / mu))
    DriftDvCalc_TOFhms = (datetime.timedelta(seconds=DriftDvCalc_TOF))
    DriftDvCalc_out = "DriftDvCalc Transfer elements are: " \
                      "\nStarting SMA: %09.7f \nTarget SMA: %09.7f \nDelta-V 1:  %09.7f m/s " \
                      "\nDelta-V 2:  %09.7f m/s \nDelta-V Combined: %09.7f m/s " \
                      "\nTime of Flight: %09.7f seconds \nTime of Flight: %s hh:mm:ss.ms" \
                      % (DriftDvCalc_Targa, DriftDvCalc_SVa, DriftDvCalc_dV1, DriftDvCalc_dV2,
                         DriftDvCalc_dVcombo, DriftDvCalc_TOF, DriftDvCalc_TOFhms)
    return DriftDvCalc_out

def Covariance(covAssetPosX, covAssetPosY, covAssetPosZ, covConjPosX, covConjPosY, covConjPosZ,
               covAssetMat00, covAssetMat01, covAssetMat02,covAssetMat10, covAssetMat11, covAssetMat12,
               covAssetMat20, covAssetMat21, covAssetMat22,  covConjMat00, covConjMat01, covConjMat02,
               covConjMat10, covConjMat11, covConjMat12, covConjMat20, covConjMat21, covConjMat22,
               covSamples, covCombRadi):

    #Created by David RC Dayton (http://www.github.com/David-RC-Dayton)
    default_sigma = 1.0
    default_samples = 10000

    def emulate_covariance(error, sigma=default_sigma,
                           n_sim=default_samples):
        error = float(error)
        sigma = float(sigma)
        n_sim = int(n_sim)

        # calculate identity values
        cov = 1 / sigma * (error / math.sqrt(2 * math.log(n_sim))) ** 2

        return [[x * cov for x in y] for y in [[1, 0, 0], [0, 1, 0], [0, 0, 1]]]

    def collision_prob(ap, sp, ac, sc,
                       sigma=default_sigma, hbr=20.0,
                       n_sim=default_samples):
        # normalize input arguments
        ap = [float(x) for x in ap]
        sp = [float(x) for x in sp]
        ac = [[float(x) for x in y] for y in ac]
        sc = [[float(x) for x in y] for y in sc]
        sigma = float(sigma)
        hbr = float(hbr)
        n_sim = int(n_sim)

        random.seed(0)  # set seed for consistent results
        rand_vec = lambda: [random.gauss(0, 1) for _ in range(3)]
        # scale covariance to match sigma & find Cholesky decomposition
        asset_sig = [[x * sigma for x in y] for y in ac]
        satellite_sig = [[x * sigma for x in y] for y in sc]
        asset_chol = numpy.linalg.cholesky(asset_sig)
        satellite_chol = numpy.linalg.cholesky(satellite_sig)
        # shift sampled points from spacecraft position & store calculated distance
        euclid_dist = lambda a, b: \
            math.sqrt(sum([(x - y) ** 2 for x, y in zip(a, b)]))
        hit = 0
        for _ in range(n_sim):
            asset_gauss = rand_vec()
            satellite_gauss = rand_vec()
            asset_shift = numpy.dot(asset_chol, asset_gauss).tolist()
            satellite_shift = numpy.dot(satellite_chol, satellite_gauss).tolist()
            asset_point = [x + y for x, y in zip(asset_shift, ap)]
            satellite_point = [x + y for x, y in zip(satellite_shift, sp)]
            if euclid_dist(asset_point, satellite_point) <= hbr:
                hit += 1
        # find probability of collision
        return float(hit) / n_sim

    asset_pos = [covAssetPosX, covAssetPosY, covAssetPosZ]
    satellite_pos = [covConjPosX, covConjPosY, covConjPosZ]
    asset_cov = [[covAssetMat00, covAssetMat01, covAssetMat02],
                 [covAssetMat10, covAssetMat11, covAssetMat12],
                 [covAssetMat20, covAssetMat21, covAssetMat22]]
    satellite_cov = [[covConjMat00, covConjMat01, covConjMat02],
                     [covConjMat10, covConjMat11, covConjMat12],
                     [covConjMat20, covConjMat21, covConjMat22]]

    covRss = math.sqrt((math.pow((covAssetPosX - covConjPosX), 2) + (math.pow((covAssetPosY - covConjPosY), 2)) + (
        math.pow((covAssetPosZ - covConjPosZ), 2))))
    #covRssDef =  "Distance between the center of the two error elipsoids is:", covRss, "meters\n"
    covSigma1 = collision_prob(asset_pos, satellite_pos, asset_cov, satellite_cov, 1, covCombRadi, covSamples)
    covSigma2 = collision_prob(asset_pos, satellite_pos, asset_cov, satellite_cov, 2, covCombRadi, covSamples)
    covSigma3 = collision_prob(asset_pos, satellite_pos, asset_cov, satellite_cov, 3, covCombRadi, covSamples)
    if covSigma1 > 0:
        covSigma1_prob =  " (1 in %d chance)" % collision_prob(asset_pos, satellite_pos, asset_cov, satellite_cov, 1, covCombRadi, covSamples) ** -1
    else:
        covSigma1_prob =  'There is a 0% probability of collision at 1 sigma'
    if covSigma2 > 0:
        covSigma2_prob = "(1 in %d chance)" % collision_prob(asset_pos, satellite_pos, asset_cov, satellite_cov, 2, covCombRadi, covSamples) ** -1
    else:
        covSigma2_prob = "There is a 0% probability of collision at 2 sigma"
    if covSigma3 > 0:
        covSigma3_prob = "(1 in %d chance)" % collision_prob(asset_pos, satellite_pos, asset_cov, satellite_cov, 3, covCombRadi, covSamples) ** -1
    else:
        covSigma3_prob = "There is a 0% probability of collision at 3 sigma"
    covSigma_out = "Distance between the center of the two error elipsoids is: %09.7f meters \n1 Sigma Probibility: %s %s \n2 Sigma Probibility: %s %s \n3 Sigma Probibility: %s %s"\
                   % (covRss, covSigma1, covSigma1_prob, covSigma2, covSigma2_prob, covSigma3, covSigma3_prob)
    return covSigma_out


class OrbitCalcGTK:

    def on_window1_destroy(self, object, data=None):
        print "quit with cancel"
        gtk.main_quit()

    def on_gtk_quit_activate(self, menuitem, data=None):
        print "quit from menu"
        gtk.main_quit()

    def __init__(self):
        self.gladefile = "OrbitCalc.glade"
        self.builder = gtk.Builder()
        self.builder.add_from_file(self.gladefile)
        self.builder.get_objects()
        self.builder.connect_signals(self)
        self.window = self.builder.get_object("window1")
        self.window.show()

    def on_quit_clicked(self, object, data=None):
        gtk.main_quit()

    def on_ComputeRV2COE_clicked(self, object, data=None):
        rI_Input = float(self.builder.get_object("rI").get_text())
        rJ_Input = float(self.builder.get_object("rJ").get_text())
        rK_Input = float(self.builder.get_object("rK").get_text())
        vI_Input = float(self.builder.get_object("vI").get_text())
        vJ_Input = float(self.builder.get_object("vJ").get_text())
        vK_Input = float(self.builder.get_object("vK").get_text())
        self.builder.get_object("textview1").get_buffer().set_text(str(RV2COE(rI_Input, rJ_Input, rK_Input, vI_Input, vJ_Input, vK_Input)))

    def on_Hohman__clicked(self, object, data=None):
        HohmanOrbit1_Input = float(self.builder.get_object("HohmanOrbit1").get_text())
        HohmanOrbit2_Input = float(self.builder.get_object("HohmanOrbit2").get_text())
        self.builder.get_object("textview1").get_buffer().set_text(str(Hohman(HohmanOrbit1_Input, HohmanOrbit2_Input)))

    def on_PlaneChange_clicked(self, object, data=None):
        PlaneChangeOrbitRadius = float(self.builder.get_object("PlaneChangeOrbitRad").get_text())
        PlaneChangeInitialInclination = float(self.builder.get_object("PlaneChangeInitIncl").get_text())
        PlaneChangeFinalInclination = float(self.builder.get_object("PlaneChangeFinalIncl").get_text())
        self.builder.get_object("textview1").get_buffer().set_text(PlaneChange(PlaneChangeOrbitRadius, PlaneChangeInitialInclination, PlaneChangeFinalInclination))

    def on_Rendezvous_clicked(self, object, data=None):
        RendezvousInterceptRadius = float(self.builder.get_object("RendezvousInterceptRad").get_text())
        RendezvousTargetRadius = float(self.builder.get_object("RendezvousTargetRad").get_text())
        RendezvousAngularSeperation = float(self.builder.get_object("RendezvousAng").get_text())
        self.builder.get_object("textview1").get_buffer().set_text(Rendezvous(RendezvousInterceptRadius, RendezvousTargetRadius, RendezvousAngularSeperation ))

    def on_SMA2Drift_clicked(self, object, data=None):
        DriftRelGeo = float(self.builder.get_object("DriftRel2Geo").get_text())
        self.builder.get_object("textview1").get_buffer().set_text(SMA2Drift(DriftRelGeo))

    def on_Drift2SMA_clicked(self, object, data=None):
        Drift2SMArate = float(self.builder.get_object("Drift2SMArte").get_text())
        self.builder.get_object("textview1").get_buffer().set_text(Drift2SMA(Drift2SMArate))

    def on_MaxRSS_clicked(self, object, data=None):
        MaxRSSVehicleSemiMajorAxis = float(self.builder.get_object("MaxRSSVehicleSMA").get_text())
        MaxRSSTargetSemiMajorAxis = float(self.builder.get_object("MaxRSSTargetSMA").get_text())
        MaxRSSLongitudeDifferance = float(self.builder.get_object("MaxRSSLong").get_text())
        MaxRSSVehicleInclination = float(self.builder.get_object("MaxRSSVehicleIncl").get_text())
        MaxRSSTargetInclination = float(self.builder.get_object("MaxRSSTargetIncl").get_text())
        self.builder.get_object("textview1").get_buffer().set_text(MaxRSS(MaxRSSVehicleSemiMajorAxis, MaxRSSTargetSemiMajorAxis, MaxRSSLongitudeDifferance, MaxRSSVehicleInclination, MaxRSSTargetInclination))

    def on_Rate2Arrive_clicked(self, object, data=None):
        Rate2ArriveHowManyDegreesAway = float(self.builder.get_object("Rate2ArriveHowManyDeg").get_text())
        Rate2ArriveHowmanyDaystoArrive = float(self.builder.get_object("Rate2ArriveHowManyDay").get_text())
        self.builder.get_object("textview1").get_buffer().set_text(Rate2Arrive(Rate2ArriveHowManyDegreesAway, Rate2ArriveHowmanyDaystoArrive))

    def on_DriftDvCalc_clicked(self, object, data=None):
        DriftDvCurrentDriftRate = float(self.builder.get_object("DriftDvCur").get_text())
        DriftDvTargetDriftRate = float(self.builder.get_object("DriftDvTar").get_text())
        self.builder.get_object("textview1").get_buffer().set_text(DriftDvCalc(DriftDvCurrentDriftRate, DriftDvTargetDriftRate))

    def on_Covariance_clicked(self, object, data=None):
        covAssetPosX = float(self.builder.get_object("AssetPosX").get_text())
        covAssetPosY = float(self.builder.get_object("AssetPosY").get_text())
        covAssetPosZ = float(self.builder.get_object("AssetPosZ").get_text())
        covConjPosX = float(self.builder.get_object("ConjPosX").get_text())
        covConjPosY = float(self.builder.get_object("ConjPosY").get_text())
        covConjPosZ = float(self.builder.get_object("ConjPosZ").get_text())
        covAssetMat00 = float(self.builder.get_object("AssetMat00").get_text())
        covAssetMat01 = float(self.builder.get_object("AssetMat01").get_text())
        covAssetMat02 = float(self.builder.get_object("AssetMat02").get_text())
        covAssetMat10 = float(self.builder.get_object("AssetMat10").get_text())
        covAssetMat11 = float(self.builder.get_object("AssetMat11").get_text())
        covAssetMat12 = float(self.builder.get_object("AssetMat12").get_text())
        covAssetMat20 = float(self.builder.get_object("AssetMat20").get_text())
        covAssetMat21 = float(self.builder.get_object("AssetMat21").get_text())
        covAssetMat22 = float(self.builder.get_object("AssetMat22").get_text())
        covConjMat00 = float(self.builder.get_object("ConjMat00").get_text())
        covConjMat01 = float(self.builder.get_object("ConjMat01").get_text())
        covConjMat02 = float(self.builder.get_object("ConjMat02").get_text())
        covConjMat10 = float(self.builder.get_object("ConjMat10").get_text())
        covConjMat11 = float(self.builder.get_object("ConjMat11").get_text())
        covConjMat12 = float(self.builder.get_object("ConjMat12").get_text())
        covConjMat20 = float(self.builder.get_object("ConjMat20").get_text())
        covConjMat21 = float(self.builder.get_object("ConjMat21").get_text())
        covConjMat22 = float(self.builder.get_object("ConjMat22").get_text())
        covSamples = float(self.builder.get_object("covSample").get_text())
        covCombRadi = float(self.builder.get_object("covCombRad").get_text())
        self.builder.get_object("textview1").get_buffer().set_text(Covariance(covAssetPosX, covAssetPosY, covAssetPosZ, covConjPosX, covConjPosY, covConjPosZ,covAssetMat00, covAssetMat01, covAssetMat02,covAssetMat10, covAssetMat11, covAssetMat12, covAssetMat20, covAssetMat21, covAssetMat22,  covConjMat00, covConjMat01, covConjMat02, covConjMat10, covConjMat11, covConjMat12, covConjMat20, covConjMat21, covConjMat22, covSamples, covCombRadi))

if __name__ == "__main__":
    main = OrbitCalcGTK()
    gtk.main()