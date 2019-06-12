# Erica Lei
# CS251 Spring 2017
# Lab 3

import numpy as np
import math

# hold the current viewing parameters and 
# build a view transformation matrix [VTM] based on the parameters.
class View: 
	def __init__(self):
		# assume the data is all located inside the unit cube with one corner on the origin.
		self.vrp =  np.matrix([0.5, 0.5, 1])
		self.vpn = np.matrix([0, 0, -1])
		self.vup = np.matrix([0, 1, 0])
		self.u = np.matrix([-1, 0, 0])
		self.extent = [1.,1.,1.]
		self.screen = [400., 400.]
		self.offset = [20., 20.]


	def build(self):
		# the basis for the view matrix
		vtm = np.identity(4,float)
		# move the VRP to origin, then
		# premultiply the vtm by the translation matrix
		t1 = np.matrix( [[1, 0, 0, -self.vrp[0, 0]],
                    [0, 1, 0, -self.vrp[0, 1]],
                    [0, 0, 1, -self.vrp[0, 2]],
                    [0, 0, 0, 1] ] )

		vtm = t1 * vtm

		tu = np.cross(self.vup,self.vpn)
		tvup = np.cross(self.vpn,tu)
		tvpn = self.vpn.copy()
		# Normalize the view axes tu, tvup, and tvpn to unit length.
		ntu = self.normalize(tu)
		ntvup = self.normalize(tvup)
		ntvpn = self.normalize(tvpn)
		# Copy the orthonormal axes back
		self.u =ntu.copy()
		self.vup = ntvup.copy()
		self.vpn = ntvpn.copy()

		# use the normalized axes to generate the rotation matrix
		# to align the view reference axes 
		r1 = np.matrix( [[ ntu[0, 0], ntu[0, 1], ntu[0, 2], 0.0 ],
                    [ ntvup[0, 0], ntvup[0, 1], ntvup[0, 2], 0.0 ],
                    [ ntvpn[0, 0], ntvpn[0, 1], ntvpn[0, 2], 0.0 ],
                    [ 0.0, 0.0, 0.0, 1.0 ] ] )

		# premultiply M by the rotation
		vtm = r1 * vtm

		# Translate the lower left corner of the view space to the origin.
		# (a translation by half the extent of the view volume in the X and Y view axes.)
		vtm =np.matrix( [[1, 0, 0, 0.5*self.extent[0]],
                    [0, 1, 0, 0.5*self.extent[1]],
                    [0, 0, 1, 0,],
                    [0, 0, 0, 1] ]  ) * vtm

		# scale to the screen
		vtm = np.matrix( [[-self.screen[0]/self.extent[0],0,0,0],
					[0, -self.screen[1]/self.extent[1],0,0],
					[0,0, 1.0/self.extent[2],0],
					[0,0,0,1]]) * vtm

		# translate the lower left corner to the origin,
		# add the view offset (gives a little buffer around the top and left edges of the window.)
		vtm = np.matrix([[1,0,0,self.screen[0] + self.offset[0]],
					[0,1,0,self.screen[1] + self.offset[1]],
					[0,0,1,0],
					[0,0,0,1]]) * vtm

		return vtm

	#Normalize to unit length
	def normalize(self, vector):
		length = np.linalg.norm(vector)
		return vector/length

	# makes a duplicate View object and returns it
	def clone(self):
		newView = View()
		newView.vrp = self.vrp.copy()
		newView.vpn = self.vpn.copy()
		newView.vup = self.vup.copy()
		newView.u = self.u.copy()
		newView.extent = self.extent.copy()
		newView.screen = self.screen.copy()
		newView.offset = self.offset.copy()
		return newView

	def main(self):
		print(self.build())

if __name__ == "__main__":
	view = View()
	view.main()
