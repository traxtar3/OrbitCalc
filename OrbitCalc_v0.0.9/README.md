
Package of Python modules and a main class with GUI

Instructions: Download all files and place them in the same directory run $ python OrbitCalc.py

Dependencies: Python 2.7 or higher

Modules required: numpy math datetime GTK3+

Can perform the following: Tab1: RV2COE Converts Cartesian ECI R&V state values to Keplerian ElSet (Common Orbital Elements)

Tab1: Converts R&V Values to Keplerian Elset  

Tab2: Hohman Transfers Calculates the delta-V necessary to transfer to higher or lower orbit -assumes circular orbit with no plane change

Tab2: Plane Change Calculates the delta-V necessary to change satellite inclination -assumes circular orbit

Tab2: Rendezvous Calculates the delta-V necessary to transfer to higher or lower orbit to meet a target

Tab3: SMA to Drift Rate calculates the drift rate given a Semi-Major Axis relative to GEO e.g -78 km = ~1deg/day Eastward drift

Tab3: Drift Rate to SMA calculates the Semi-Major Axis given a drift rate relative to GEO e.g( ~-1deg/day Eastward drift = SMA of 42242 km, 78 km below the GEO belt

Tab1:Distance to Target calculates the minimum and maximum miss distance between 2 satellites given SMA, angular separation, and inclination

Tab1: Drift Rate / delta-V calculates the optimum drift rate to arrive at target location calculates the delta-V required to achieve a given drift rate

Tab1: Collision Probability Given 2 assets' position and covariance matrix (error ellipsoid), calculates 1,2, & 3 sigma probability of collision

Things TODO: -change # of significant digits for some of the items -make the GUI more aesthetically pleasing

Big thanks to Dave, Jake and Pat for all the help on my first big Python project!

Check out Dave's repository here: https://github.com/david-rc-dayton

