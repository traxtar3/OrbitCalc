# Built by John W. Harms ##
# Version 0.0.1 -- Initial Build ##
# Version 0.0.2 -- Refactored to be added as module to different project ##
# Version 0.0.5 -- Split to separate files and refactored ##
# Version 0.0.7 -- Added Line of Sight tab
# Version 0.0.8 -- Renamed Line of Sight tab to "TLE Tools"
#               -- Added TLE to Keplerian Elements calculation (tlekep.py)
#               -- Added "Use Current Time" checkbox
#               -- Changed GUI
# Version 0.1.0 -- Added R&V propagator
#               -- cleaned up RV2COE code

# Last Change 12 June 15

import gtk
from datetime import datetime
import RV2COE
import Hohman
import PlaneChange
import Rendezvous
import Drift2SMA
import SMA2Drift
import MaxRSS
import Rate2Arrive
import DriftDvCalc
import Covariance
import los
import cities

import tlekep
import rvprop


class OrbitCalcGTK:
    def on_window1_destroy(self, object, data=None):
        print "quit with cancel"
        gtk.main_quit()

    def on_quit_clicked(self, object, data=None):
        gtk.main_quit()

    def __init__(self):
        self.gladefile = "OrbitCalc.glade"
        self.builder = gtk.Builder()
        self.builder.add_from_file(self.gladefile)
        self.builder.get_objects()
        self.builder.connect_signals(self)
        self.window = self.builder.get_object("window1")
        self.window.show()

        self.liststore = gtk.ListStore(str)
        for k in sorted(cities.location.keys()):
            self.liststore.append([k])
        self.combobox = self.builder.get_object("combobox1")
        self.combobox.set_model(self.liststore)
        self.cell = gtk.CellRendererText()
        self.combobox.pack_start(self.cell, True)
        self.combobox.add_attribute(self.cell, 'text', 0)
        self.combobox.set_active(0)


    def on_combobox1_changed(self, widget, data=None):
        self.index = widget.get_active()
        self.model = widget.get_model()
        self.item = self.model[self.index][0]


    def on_ComputeRV2COE_clicked(self, object, data=None):
        rI_Input = float(self.builder.get_object("rI").get_text())
        rJ_Input = float(self.builder.get_object("rJ").get_text())
        rK_Input = float(self.builder.get_object("rK").get_text())
        vI_Input = float(self.builder.get_object("vI").get_text())
        vJ_Input = float(self.builder.get_object("vJ").get_text())
        vK_Input = float(self.builder.get_object("vK").get_text())
        r = [rI_Input, rJ_Input, rK_Input]
        v = [vI_Input, vJ_Input, vK_Input]
        self.builder.get_object("textview1").get_buffer().set_text(str(RV2COE.rv2coe(r, v)))

    def on_Hohman__clicked(self, object, data=None):
        HohmanOrbit1_Input = float(self.builder.get_object("HohmanOrbit1").get_text())
        HohmanOrbit2_Input = float(self.builder.get_object("HohmanOrbit2").get_text())
        self.builder.get_object("textview1").get_buffer().set_text(str(Hohman.Hohman(
            HohmanOrbit1_Input, HohmanOrbit2_Input)))

    def on_PlaneChange_clicked(self, object, data=None):
        PlaneChangeOrbitRadius = float(self.builder.get_object("PlaneChangeOrbitRad").get_text())
        PlaneChangeInitialInclination = float(self.builder.get_object("PlaneChangeInitIncl").get_text())
        PlaneChangeFinalInclination = float(self.builder.get_object("PlaneChangeFinalIncl").get_text())
        self.builder.get_object("textview1").get_buffer().set_text(PlaneChange.PlaneChange(
            PlaneChangeOrbitRadius, PlaneChangeInitialInclination, PlaneChangeFinalInclination))

    def on_Rendezvous_clicked(self, object, data=None):
        RendezvousInterceptRadius = float(self.builder.get_object("RendezvousInterceptRad").get_text())
        RendezvousTargetRadius = float(self.builder.get_object("RendezvousTargetRad").get_text())
        RendezvousAngularSeperation = float(self.builder.get_object("RendezvousAng").get_text())
        self.builder.get_object("textview1").get_buffer().set_text(Rendezvous.Rendezvous(
            RendezvousInterceptRadius, RendezvousTargetRadius, RendezvousAngularSeperation))

    def on_SMA2Drift_clicked(self, object, data=None):
        DriftRelGeo = float(self.builder.get_object("DriftRel2Geo").get_text())
        self.builder.get_object("textview1").get_buffer().set_text(SMA2Drift.SMA2Drift(DriftRelGeo))

    def on_Drift2SMA_clicked(self, object, data=None):
        Drift2SMArate = float(self.builder.get_object("Drift2SMArte").get_text())
        self.builder.get_object("textview1").get_buffer().set_text(Drift2SMA.Drift2SMA(Drift2SMArate))

    def on_MaxRSS_clicked(self, object, data=None):
        MaxRSSVehicleSemiMajorAxis = float(self.builder.get_object("MaxRSSVehicleSMA").get_text())
        MaxRSSTargetSemiMajorAxis = float(self.builder.get_object("MaxRSSTargetSMA").get_text())
        MaxRSSLongitudeDifferance = float(self.builder.get_object("MaxRSSLong").get_text())
        MaxRSSVehicleInclination = float(self.builder.get_object("MaxRSSVehicleIncl").get_text())
        MaxRSSTargetInclination = float(self.builder.get_object("MaxRSSTargetIncl").get_text())
        self.builder.get_object("textview1").get_buffer().set_text(MaxRSS.MaxRSS(
            MaxRSSVehicleSemiMajorAxis, MaxRSSTargetSemiMajorAxis, MaxRSSLongitudeDifferance,
            MaxRSSVehicleInclination, MaxRSSTargetInclination))

    def on_Rate2Arrive_clicked(self, object, data=None):
        Rate2ArriveHowManyDegreesAway = float(self.builder.get_object("Rate2ArriveHowManyDeg").get_text())
        Rate2ArriveHowmanyDaystoArrive = float(self.builder.get_object("Rate2ArriveHowManyDay").get_text())
        self.builder.get_object("textview1").get_buffer().set_text(Rate2Arrive.Rate2Arrive(
            Rate2ArriveHowManyDegreesAway, Rate2ArriveHowmanyDaystoArrive))

    def on_DriftDvCalc_clicked(self, object, data=None):
        DriftDvCurrentDriftRate = float(self.builder.get_object("DriftDvCur").get_text())
        DriftDvTargetDriftRate = float(self.builder.get_object("DriftDvTar").get_text())
        self.builder.get_object("textview1").get_buffer().set_text(DriftDvCalc.DriftDvCalc(
            DriftDvCurrentDriftRate, DriftDvTargetDriftRate))

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
        self.builder.get_object("textview1").get_buffer().set_text(Covariance.Covariance(
            covAssetPosX, covAssetPosY, covAssetPosZ, covConjPosX, covConjPosY, covConjPosZ,
            covAssetMat00, covAssetMat01, covAssetMat02, covAssetMat10, covAssetMat11, covAssetMat12,
            covAssetMat20, covAssetMat21, covAssetMat22, covConjMat00, covConjMat01, covConjMat02,
            covConjMat10, covConjMat11, covConjMat12, covConjMat20, covConjMat21, covConjMat22,
            covSamples, covCombRadi))

    def on_los_angles_clicked(self, object, data=None):
        site_selected = self.builder.get_object("combobox1").get_active_text()
        tle_line1 = str(self.builder.get_object("tle1").get_text())
        tle_line2 = str(self.builder.get_object("tle2").get_text())
        self.currenttime = self.builder.get_object("use_current_time")
        if self.currenttime.get_active():
            timeset = str(datetime.utcnow())
        else:
            timeset =  str(self.builder.get_object("los_time").get_text())

        line1err = ("The Two-Line Element (TLE) format was designed for punch cards and is\n"
                    "therefore very strict about the position of every space and digit in a\n"
                    "TLE line.  Your line does not quite match.  Here is the official format\n"
                    "for line 1 followed by the line you provided:\n\n"
                    "1 25544U 98067A   15159.73191137  .00006600  00000-0  10229-3 0  9992\n"
                    "2 25544  51.6431 126.2443 0004739  37.0689  24.1172 15.55345846946721")

        if (tle_line1.count('') + tle_line2.count('')) == 143:
            self.builder.get_object("textview1").get_buffer().set_text(
                los.los(site_selected, tle_line1, tle_line2, timeset))
        elif (tle_line1.count('') + tle_line2.count('')) == 142:
            self.builder.get_object("textview1").get_buffer().set_text(
                los.los(site_selected, tle_line1, tle_line2, timeset))
        elif (tle_line1.count('') + tle_line2.count('')) == 141:
            self.builder.get_object("textview1").get_buffer().set_text(
                los.los(site_selected, tle_line1, tle_line2, timeset))
        elif (tle_line1.count('') + tle_line2.count('')) == 140:
            self.builder.get_object("textview1").get_buffer().set_text(
                los.los(site_selected, tle_line1, tle_line2, timeset))
        else:
            self.builder.get_object("textview1").get_buffer().set_text(line1err)

    def on_los_kep_clicked(self, object, data=None):
        self.currenttime = self.builder.get_object("use_current_time")

        if self.currenttime.get_active():
            timeset = str(datetime.utcnow())
        else:
            timeset =  str(self.builder.get_object("los_time").get_text())

        tle_line1 = str(self.builder.get_object("tle1").get_text())
        tle_line2 = str(self.builder.get_object("tle2").get_text())

        line1err = ("The Two-Line Element (TLE) format was designed for punch cards and is\n"
            "therefore very strict about the position of every space and digit in a\n"
            "TLE line.  Your line does not quite match.  Here is the official format\n"
            "for line 1 followed by the line you provided:\n\n"
            "1 25544U 98067A   15159.73191137  .00006600  00000-0  10229-3 0  9992\n"
            "2 25544  51.6431 126.2443 0004739  37.0689  24.1172 15.55345846946721")

        if (tle_line1.count('') + tle_line2.count('')) == 143:
            self.builder.get_object("textview1").get_buffer().set_text(tlekep.tlekep(tle_line1, tle_line2, timeset))
        elif (tle_line1.count('') + tle_line2.count('')) == 142:
            self.builder.get_object("textview1").get_buffer().set_text(tlekep.tlekep(tle_line1, tle_line2, timeset))
        elif (tle_line1.count('') + tle_line2.count('')) == 141:
            self.builder.get_object("textview1").get_buffer().set_text(tlekep.tlekep(tle_line1, tle_line2, timeset))
        elif (tle_line1.count('') + tle_line2.count('')) == 140:
            self.builder.get_object("textview1").get_buffer().set_text(tlekep.tlekep(tle_line1, tle_line2, timeset))
        else:
            self.builder.get_object("textview1").get_buffer().set_text(line1err)

    def on_rvprop_clicked(self, object, data=None):
        self.rv_currenttime = self.builder.get_object("rvprop_now")
        if self.rv_currenttime.get_active():
            stoptime = str(datetime.utcnow())
        else:
            stoptime =  str(self.builder.get_object("rv_stoptime").get_text())
        starttime = self.builder.get_object("rv_starttime").get_text()
        starttime = str(self.builder.get_object("rv_starttime").get_text())
        rvrI_Input = float(self.builder.get_object("rv_rI").get_text())
        rvrJ_Input = float(self.builder.get_object("rv_rJ").get_text())
        rvrK_Input = float(self.builder.get_object("rv_rK").get_text())
        rvvI_Input = float(self.builder.get_object("rv_vI").get_text())
        rvvJ_Input = float(self.builder.get_object("rv_vJ").get_text())
        rvvK_Input = float(self.builder.get_object("rv_vK").get_text())
        ri = [rvrI_Input, rvrJ_Input, rvrK_Input]
        vi = [rvvI_Input, rvvJ_Input, rvvK_Input]


        self.builder.get_object("textview1").get_buffer().set_text(str(rvprop.twobody2(starttime, stoptime, ri, vi)))
        # self.builder.get_object("textview1").get_buffer().set_text(str(starttime))






if __name__ == "__main__":
    main = OrbitCalcGTK()
    gtk.main()

# OrbitCalcGTK.los_use_current_time_selected()