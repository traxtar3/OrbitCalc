# Built by John W. Harms ##
# Version 0.01 -- Initial Build ##
# Version 0.02 -- Refactored to be added as module to different project ##
# Version 0.05 -- Split to separate files and refactored ##

import gtk
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


class OrbitCalcGTK:

    def on_window1_destroy(self, object, data=None):
        print "quit with cancel"
        gtk.main_quit()

    def on_quit_clicked(self, object, data=None):
        gtk.main_quit()

    def __init__(self):
        self.gladefile = "OrbitCalc_v2.glade"
        self.builder = gtk.Builder()
        self.builder.add_from_file(self.gladefile)
        self.builder.get_objects()
        self.builder.connect_signals(self)
        self.window = self.builder.get_object("window1")
        self.window.show()

            # the liststore
        self.liststore = gtk.ListStore(int,str)
        self.liststore.append([0,"Select an Item:"])
        self.liststore.append([1,"HTSA"])
        self.liststore.append([2,"Row 2"])
        self.liststore.append([3,"Row 3"])
        self.liststore.append([4,"Row 4"])
        self.liststore.append([5,"Row 5"])

        # the combobox
        self.combobox = self.builder.get_object("combobox1")
        self.combobox.set_model(self.liststore)
        self.cell = gtk.CellRendererText()
        self.combobox.pack_start(self.cell, True)
        self.combobox.add_attribute(self.cell, 'text', 1)
        self.combobox.set_active(0)

        #self.window = self.builder.get_object("window1")
        #self.window1.show()

    def on_combobox1_changed(self, widget, data=None):
        self.index = widget.get_active()
        self.model = widget.get_model()
        self.item = self.model[self.index][1]
        print "ComboBox Active Text is", self.item
        # site_selected = self.item
        # print "ComboBox Active Index is", self.index
        # self.builder.get_object("label1").set_text(self.item)
        # return site_selected


    def on_ComputeRV2COE_clicked(self, object, data=None):
        rI_Input = float(self.builder.get_object("rI").get_text())
        rJ_Input = float(self.builder.get_object("rJ").get_text())
        rK_Input = float(self.builder.get_object("rK").get_text())
        vI_Input = float(self.builder.get_object("vI").get_text())
        vJ_Input = float(self.builder.get_object("vJ").get_text())
        vK_Input = float(self.builder.get_object("vK").get_text())
        self.builder.get_object("textview1").get_buffer().set_text(str(RV2COE.RV2COE(
            rI_Input, rJ_Input, rK_Input, vI_Input, vJ_Input, vK_Input)))

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
            covAssetMat20, covAssetMat21, covAssetMat22,  covConjMat00, covConjMat01, covConjMat02,
            covConjMat10, covConjMat11, covConjMat12, covConjMat20, covConjMat21, covConjMat22,
            covSamples, covCombRadi))

    def on_los_clicked(self, object, data=None):
        site_selected = str(self.builder.get_object("site_box"))
        tle_line1 = str(self.builder.get_object("tle1").get_text())
        tle_line2 = str(self.builder.get_object("tle2").get_text())
        self.builder.get_object("textview1").get_buffer().set_text(los.los(site_selected, tle_line1, tle_line2))

if __name__ == "__main__":
    main = OrbitCalcGTK()
    gtk.main()
