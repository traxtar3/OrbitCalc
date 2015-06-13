# Built by John W. Harms ##
# Version 0.01 -- Initial Build ##
# Version 0.02 -- Refactored to be added as module to different project ##
# Version 0.05 -- Split to separate files and refactored ##
# Version 0.06 -- Completely overhauled GUI ##
# Version 0.07 -- Added Line of Sight tab ##

# Last Change 8 June 15

import sys

try:
 	import pygtk
  	pygtk.require("2.0")
except:
  	pass
try:
	import gtk
  	import gtk.glade
except:
	sys.exit(1)

class OrbitCalcGTK:
    def __init__(self):
		#Set the Glade file
		self.gladefile = "OrbitCalc.glade"
	        self.wTree = gtk.glade.XML(self.gladefile)
		#Get the Main Window, and connect the "destroy" event
		self.window = self.wTree.get_widget("Window1")
		if (self.window):
			self.window.connect("destroy", gtk.main_quit)
