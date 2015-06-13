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
