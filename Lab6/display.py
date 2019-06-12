# Erica Lei
# CS251 Spring2017
# project5


import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import math
import random
import numpy as np
import view
import sys
import data
import analysis


# create a class to build and manage the display
class DisplayApp:

	def __init__(self, width, height):

		# create a tk object, which is the root window
		self.root = tk.Tk()
		# width and height of the window
		self.initDx = width
		self.initDy = height
		# set up the geometry for the window
		self.root.geometry( "%dx%d+50+30" % (self.initDx, self.initDy) )
		# set the title of the window
		self.root.title("Viewing Axes")
		# set the maximum size of the window for resizing
		self.root.maxsize( 1024, 768 )
		# bring the window to the front
		self.root.lift()
		# setup the menus
		self.buildMenus()
		# build the controls
		self.buildControls()
		# build the objects on the Canvas
		self.buildCanvas()
		self.root.update_idletasks()
		# set up the key bindings
		self.setBindings()

		# Create a View object and set up the default parameters
		self.vobj = view.View()
		
		# Create the axes fields and build the axes
		self.axes = np.matrix([[0,0,0,1],
								[1,0,0,1],
								[0,0,0,1],
								[0,1,0,1],
								[0,0,0,1],
								[0,0,1,1]])

		# set up the application state

		self.lines = []
		self.objects = []
		self.labels = []
		self.bars = []
		self.txt = []
		self.regressionobj = []
		self.regressionpos = [[],[None]]
		self.buildAxes()
	
	def buildMenus(self): 
		# create a new menu
		self.menu = tk.Menu(self.root)

		# set the root menu to our new menu
		self.root.config(menu = self.menu)

		# create a variable to hold the individual menus
		self.menulist = []

		# create a file menu
		filemenu = tk.Menu( self.menu )
		self.menu.add_cascade( label = "File", menu = filemenu )
		self.menulist.append(filemenu)


		# menu text for the elements
		# "Open" method is not used in project3
		menutext = [ [ 'Open...  \u2318-O','Save Canvas  \u2318-S', "-",'Quit  \u2318-Q' ] ]

		# menu callback functions
		menucmd = [ [self.handleOpen,self.handleSave, None, self.handleQuit]  ]
		
		# build the menu elements and callbacks
		for i in range( len( self.menulist ) ):
			for j in range( len( menutext[i]) ):
				if menutext[i][j] != '-':
					self.menulist[i].add_command( label = menutext[i][j], command=menucmd[i][j] )
				else:
					self.menulist[i].add_separator()

	# create the canvas object
	def buildCanvas(self):
		self.canvas = tk.Canvas( self.root, width=self.initDx, height=self.initDy )
		self.canvas.pack( expand=tk.YES, fill=tk.BOTH )
		
		# axes labels
		label_x_ind = tk.Label(self.canvas, text = "x-axis data:",)
		label_x_ind.pack()
		self.canvas.create_window(550, 20, window=label_x_ind)
		self.x_axis_label = tk.StringVar()
		label_x = tk.Label(self.canvas, textvariable = self.x_axis_label, relief = tk.RAISED, justify = tk.LEFT)
		label_x.pack()
		self.canvas.create_window(650, 20,  window = label_x)

		label_y_ind = tk.Label(self.canvas, text = "y-axis data:",)
		label_y_ind.pack()
		self.canvas.create_window(550, 40, window=label_y_ind)
		self.y_axis_label = tk.StringVar()
		label_y = tk.Label(self.canvas, textvariable = self.y_axis_label, relief = tk.RAISED, justify = tk.LEFT)
		label_y.pack()
		self.canvas.create_window(650, 40, window = label_y)

		label_z_ind = tk.Label(self.canvas, text = "z-axis data:",)
		label_z_ind.pack()
		self.canvas.create_window(550, 60, window=label_z_ind)
		self.z_axis_label = tk.StringVar()
		label_z = tk.Label(self.canvas, textvariable = self.z_axis_label, relief = tk.RAISED, justify = tk.LEFT)
		label_z.pack()
		self.canvas.create_window(650, 60,  window = label_z)

		label_color_ind = tk.Label(self.canvas, text = "color axis data:",)
		label_color_ind.pack()
		self.canvas.create_window(550, 80, window=label_color_ind)
		self.color_axis_label = tk.StringVar()
		label_color = tk.Label(self.canvas, textvariable = self.color_axis_label, relief = tk.RAISED, justify = tk.LEFT)
		label_color.pack()
		self.canvas.create_window(650, 80,  window = label_color)

		label_size_ind = tk.Label(self.canvas, text = "size axis data:",)
		label_size_ind.pack()
		self.canvas.create_window(550, 100, window=label_size_ind)
		self.size_axis_label = tk.StringVar()
		label_size = tk.Label(self.canvas, textvariable = self.size_axis_label, relief = tk.RAISED, justify = tk.LEFT)
		label_size.pack()
		self.canvas.create_window(650, 100,  window = label_size)
		return

	# build a frame and put controls in it
	def buildControls(self):
		# make a control frame
		self.cntlframe = tk.Frame(self.root)
		self.cntlframe.pack(side=tk.RIGHT, padx=2, pady=2, fill=tk.Y)

		sep = tk.Frame( self.root, height=self.initDy, width=2, bd=1, relief=tk.SUNKEN )
		sep.pack( side=tk.RIGHT, padx = 2, pady = 2, fill=tk.Y)

		# make a cmd 1 button in the frame
		self.buttons = []

		# reset file
		self.buttons.append( ( 'reset file', tk.Button( self.cntlframe, text="Reset File", command=self.handleResetFileButton, width=10 ) ) )
		self.buttons[-1][1].pack(side=tk.TOP)

		# reset the objects
		self.buttons.append( ( 'reset position', tk.Button( self.cntlframe, text="Reset Position", command=self.handleResetButton, width=10 ) ) )
		self.buttons[-1][1].pack(side=tk.TOP)

		# plot all data button
		self.buttons.append(('plot all data', tk.Button(self.cntlframe, text = "Plot Data", command =self.handlePlotData, width = 15 )))
		self.buttons[-1][1].pack(side=tk.TOP)

		# plot regression line button
		self.buttons.append(('plot regression line', tk.Button(self.cntlframe, text = "Run Regression", command =self.handleLinearRegression, width = 15 )))		
		self.buttons[-1][1].pack(side=tk.TOP)

		# EXTENSION
		# control over the interaction constants
		label1 = tk.Label(self.cntlframe, text = "Translation Speed", width = 20)
		label1.pack (side = tk.TOP)

		self.translationOption = tk.StringVar( self.root )
		self.translationOption.set("1.0")
		transMenu = tk.OptionMenu(self.cntlframe, self.translationOption,
									"1.0", "2.0", "3.0", "4.0", "5.0")
		transMenu.pack(side = tk.TOP)

		label2 = tk.Label(self.cntlframe, text = "Scaling Speed", width = 20)
		label2.pack (side = tk.TOP)

		self.scalingOption= tk.StringVar( self.root )
		self.scalingOption.set("1.0")
		scaleMenu = tk.OptionMenu(self.cntlframe, self.scalingOption,
									"1.0", "2.0", "3.0", "4.0", "5.0")
		scaleMenu.pack(side = tk.TOP)

		label3 = tk.Label(self.cntlframe, text = "Rotation Speed", width = 20)
		label3.pack(side = tk.TOP)

		self.rotationOption = tk.StringVar(self.root) 
		self.rotationOption.set("1.0")
		rotateMenu = tk.OptionMenu(self.cntlframe, self.rotationOption,
									"1.0", "2.0", "3.0", "4.0", "5.0")
		rotateMenu.pack(side = tk.TOP)


		# buttons that show 3 planes directly
		self.buttons.append(( 'x-y plane', tk.Button( self.cntlframe, text="x-y plane", command=self.handleXY, width=10 ) ) )
		self.buttons[-1][1].pack(side=tk.BOTTOM)
		self.buttons.append(( 'x-z plane', tk.Button( self.cntlframe, text="x-z plane", command=self.handleXZ, width=10 ) ) )
		self.buttons[-1][1].pack(side=tk.BOTTOM)
		self.buttons.append(( 'y-z plane', tk.Button( self.cntlframe, text="y-z plane", command=self.handleYZ, width=10 ) ) )
		self.buttons[-1][1].pack(side=tk.BOTTOM)
		return
	
	def setBindings(self):
		self.root.bind( '<Button-1>', self.handleButton1 )
		self.root.bind( '<Button-2>', self.handleButton2 )
		self.root.bind( '<Button-3>', self.handleButton3 )
		self.root.bind( '<B1-Motion>', self.handleButton1Motion )
		self.root.bind( '<B2-Motion>', self.handleButton2Motion )
		self.root.bind( '<B3-Motion>', self.handleButton3Motion )
		self.root.bind( '<Control-q>', self.handleQuit )
		self.root.bind( '<Control-o>', self.handleModO )
		self.root.bind( '<Control-s>', self.handleSave)
		self.root.bind( '<Control-r>', self.handleLinearRegression )
		self.root.bind( '<Control-Button-1>', self.handleButton2 )
		self.root.bind( '<Control-B1-Motion>', self.handleButton2Motion ) 
		self.root.bind( '<Control-Shift-Button-1>', self.handleButton3 )
		self.root.bind( '<Control-Shift-B1-Motion>', self.handleButton3Motion)
		self.root.bind( '<Shift-Button-1>', self.displayInfo )
		self.canvas.bind( '<Configure>', self.handleResize )
		return

	# save a postscript file
	def handleSave(self, event = None):
		PicDialog = SavePicDialog(self.root, dobj = None, title = "Set File Name")
		if PicDialog.userCancelled == True:
			return
		else:
			self.canvas.postscript(file= PicDialog.getFilename()+".ps") 

	# change window size -> change axes size
	def handleResize(self, event=None):
		w = self.canvas.winfo_width()
		h = self.canvas.winfo_height()
		short = min(w, h)
		self.vobj.screen = [short - 200, short - 200]
		self.updateAxes()
		self.updatePoints()

	# show data point values
	def displayInfo(self, event):
		for t in self.txt:
			self.canvas.delete(t)
		self.txt = []
		idx = -1;
		baseClick0 = (event.x, event.y)
		for pt in self.objects:
			idx += 1
			loc = self.canvas.coords(pt)
			# if mouse is over the data point
			if loc[0] <= event.x + 2 and loc[2] >= event.x - 2:
				if loc[1] <= event.y + 2 and loc[3] >= event.y - 2:
					string = "["
					d = self.raw.tolist()[idx]
					for n in d:
						string += str(n)+","
					string += "]"
					string = self.canvas.create_text(event.x, event.y, fill="DodgerBlue4", text=string)
					self.txt.append(string)
					break

	# open file and save it to data matrix
	def handleModO(self, event = None):
		self.handleOpen()

	# open a file and save it to data matrix
	def handleOpen(self,event = None):
		try:
			fn = filedialog.askopenfilename( parent=self.root, title='Choose a data file', initialdir='.' )
		except FileNotFoundError:
			print("cancelled")
		else:
			self.dobj = data.Data(fn)

	# quit program
	def handleQuit(self, event=None):
		print('Terminating')
		self.root.destroy()

	# clicking reset file button
	def handleResetFileButton(self):
		self.handleOpen()
		self.canvas.delete(tk.ALL)
		self.lines = []
		self.objects = []
		self.labels = []
		self.bars = []
		self.txt = []
		self.regressionobj=[]
		self.buildAxes()

	# clicking reset position button
	def handleResetButton(self):
		print('handling reset button')
		self.vobj = view.View().clone()
		self.updateAxes()
		self.updatePoints()
		self.updateLabels()
		self.updateFits()

	# handle plotting data - enable the user to select which columns of data to ploton which axes
	# then builds the data
	def handlePlotData(self):
		self.handleChooseAxes()
		if len(self.headernames)== 1:
			self.y_axis_label.set("Quantity")
			self.z_axis_label.set(None)
			self.buildHistogram()
			self.buildLabels()
		else:
			for bar in self.bars:
				self.canvas.delete(bar)
			self.bars= []
			self.buildPoints()
			self.buildLabels()
		
	#choose the axes to plot
	def handleChooseAxes(self):
		#select axes from dialog window
		dialogWindow1 = MyDialog(self.root, self.dobj, title = "Choose Axes")
		if dialogWindow1.userCancelled() ==True :
			print("user cancelled")
			return
		else:
			selections = dialogWindow1.getSelection()
			self.headernames = []
			self.rawheaders = []
			for i in selections[0:3]:
				if i!='':
					self.headernames.append(i)
					self.rawheaders.append(i)
			if selections[3] != '':
				self.color_axis = str(selections[3] )
				self.rawheaders.append(selections[3] )
			else:
				self.color_axis = None
			if selections[4] != '':
				self.size_axis = str(selections[4])
				self.rawheaders.append(selections[4])
			else:
				self.size_axis = None
			# update label 
			self.x_axis_label.set(self.headernames[0])
			self.color_axis_label.set(self.color_axis)
			self.size_axis_label.set(self.size_axis)

	def buildPoints(self):
		# clear all data
		for pt in self.objects:
			self.canvas.delete(pt)
		self.objects = []

		# reset orientation
		self.vobj = view.View().clone()
		self.updateAxes()
		self.updateLabels()

		self.raw = self.dobj.getNumCol(self.rawheaders)
		self.data = analysis.normalize_columns_separately(self.headernames, self.dobj)

		if len(self.headernames) == 2:
			# add a column of 0's and homogeneous coordinate
			self.coords = np.hstack((self.data, self.data.shape[0]*[[0]], self.data.shape[0]*[[1]]))

			self.y_axis_label.set(self.headernames[1])
			self.z_axis_label.set(None)
		
		elif len(self.headernames) == 3:
			# add only homogeneous coordinate
			self.coords = np.hstack((self.data, self.data.shape[0]*[[1]]))
			self.y_axis_label.set(self.headernames[1])
			self.z_axis_label.set(self.headernames[2])

		if self.color_axis != None:
			# normalize color axis
			self.colors = analysis.normalize_columns_separately([self.color_axis], self.dobj)
		else:
			# if not specified, use 1
			self.colors = np.matrix([[1]]*self.data.shape[0])

		if self.size_axis != None:
			# normalize size axis
			self.sizes = analysis.normalize_columns_separately([self.size_axis], self.dobj)
		else:
			# if not specified, use 5
			self.sizes = np.matrix([[3]]*self.data.shape[0])

		# draw points
		vtm = self.vobj.build()
		ptcoords = vtm * self.coords.T
		for i in range(ptcoords.shape[1]):
			x0= ptcoords[0,i]- float(self.sizes[i,0])
			y0= ptcoords[1,i]- float(self.sizes[i,0])
			x1= ptcoords[0,i]+ float(self.sizes[i,0])
			y1= ptcoords[1,i]+ float(self.sizes[i,0])
			alpha = float(self.colors[i,0])
			rgb = (int(alpha *255), int((1-alpha)*255), 0)
			point = self.canvas.create_oval( x0,y0,x1,y1, 
											fill='#%02x%02x%02x'%rgb,
											outline='' )
			self.objects.append(point)

	# update the location of each point
	def updatePoints(self):
		if len(self.objects) == 0:
			pass
		else:
			vtm = self.vobj.build()
			ptcoords = vtm * self.coords.T
			i = 0
			for pt in self.objects:
				x0= ptcoords[0,i]- float(self.sizes[i,0])
				y0= ptcoords[1,i]- float(self.sizes[i,0])
				x1= ptcoords[0,i]+ float(self.sizes[i,0])
				y1= ptcoords[1,i]+ float(self.sizes[i,0])
				self.canvas.coords(pt,x0,y0,x1,y1)
				i += 1

	# if only one axis is selected, create a histogram showing the distribution
	def buildHistogram(self):
		for rec in self.bars:
			self.canvas.delete(rec)
		self.bars = []
		self.updateLabels()
		# draw bars
		vtm = self.vobj.build()
		selected = analysis.normalize_columns_separately(self.headernames,self.dobj)

		axes = (vtm * self.axes.T).T
		binw = int((axes[1,0]-axes[0,0])/10)
		one_h = (axes[2,1]-axes[3,1])/selected.shape[0]
		ten_pct = 0
		twenty_pct = 0
		thirty_pct = 0
		fourty_pct = 0
		fifty_pct = 0
		sixty_pct = 0
		seventy_pct = 0
		eighty_pct = 0
		ninety_pct = 0
		hundred_pct = 0
		for i in range(selected.shape[0]):
			if selected[i,0]<0.1:
				ten_pct+=1
			elif 0.1<=selected[i,0]<0.2:
				twenty_pct+=1
			elif 0.2<=selected[i,0]<0.3:
				thirty_pct+=1
			elif 0.3<=selected[i,0]<0.4:
				fourty_pct+=1
			elif 0.4<=selected[i,0]<0.5:
				fifty_pct+=1
			elif 0.5<=selected[i,0]<0.6:
				sixty_pct+=1
			elif 0.6<=selected[i,0]<0.7:
				seventy_pct+=1
			elif 0.7<=selected[i,0]<0.8:
				eighty_pct+=1
			elif 0.8<=selected[i,0]<0.9:
				ninety_pct+=1
			elif 0.9<=selected[i,0]<=1:
				hundred_pct+=1
		i=0
		for j in [ten_pct,twenty_pct,thirty_pct,fourty_pct,fifty_pct,sixty_pct,seventy_pct,eighty_pct,ninety_pct,hundred_pct]:
			x0 = axes[0,0]+i*binw
			y0 = axes[2,1]-j*one_h
			x1 = axes[0,0]+(i+1)*binw
			y1 = axes[2,1]
			i+=1        
			rec=self.canvas.create_rectangle(x0,y0,x1,y1, fill="dark orange")
			self.bars.append(rec)

	# create the axis line objects in their default location
	def buildAxes(self):
		vtm = self.vobj.build()
		pts = (vtm * self.axes.T).T
		self.xAxis = self.canvas.create_line(pts[0,0],pts[0,1],pts[1,0],pts[1,1], fill = "black", width = 3)
		self.yAxis = self.canvas.create_line(pts[2,0],pts[2,1],pts[3,0],pts[3,1], fill = "yellow", width = 3)
		self.zAxis = self.canvas.create_line(pts[4,0],pts[4,1],pts[5,0],pts[5,1], fill = "green", width = 3)
		self.lines.extend([self.xAxis,self.yAxis,self.zAxis])

	# modify the endpoints of the axes to their new location
	def updateAxes(self):
		vtm = self.vobj.build()
		pts = (vtm * self.axes.T).T
		# for each line object
			# update the coordinates of the object
		i = 0
		for line in self.lines:
			self.canvas.coords(line, pts[i,0],pts[i,1],pts[i+1,0],pts[i+1,1] )
			i += 2

	# create axis labels
	def buildLabels(self):
		for lb in self.labels:
			self.canvas.delete(lb)
		self.labels = []
		vtm = self.vobj.build()
		pts = (vtm * self.axes.T).T
		y = self.y_axis_label.get()
		z = self.z_axis_label.get()

		self.xLabel = self.canvas.create_text(pts[1,0]+ 20, pts[1,1], text = self.headernames[0])
		self.yLabel = self.canvas.create_text(pts[3,0], pts[3,1] - 20, text = y)
		self.zLabel = self.canvas.create_text(pts[5,0]- 20, pts[5,1], text = z)
		self.labels.extend([self.xLabel, self.yLabel, self.zLabel])

	# update axis labels
	def updateLabels(self):
		vtm = self.vobj.build()
		pts = (vtm * self.axes.T).T
		# for each label object
			# update the coordinates of the object
		i = 0
		for label in self.labels[0:3]:
			self.canvas.coords(label, pts[i+1,0] + 10 ,pts[i+1,1] )
			i += 2

	# translation initiation
	def handleButton1(self, event):
		print('handle button 1: %d %d' % (event.x, event.y))
		self.baseClick1 = (event.x, event.y)
		for t in self.txt:
			self.canvas.delete(t)
		self.txt = []
	# rotation initiation
	def handleButton2(self, event):
		print('handle button 2: %d %d' % (event.x, event.y))
		self.baseClick3 = (event.x, event.y)
		self.originalview = self.vobj.clone()
	# scaling initiation
	def handleButton3(self, event):
		print('handle button 3: %d %d' % (event.x, event.y))
		self.baseClick2 = (event.x, event.y)
		self.viewextent = self.vobj.clone().extent

	# translation
	def handleButton1Motion(self, event):
		print('handle button 1 motion: %d %d' % (event.x, event.y) )
		dx = event.x - self.baseClick1[0]
		dy = event.y - self.baseClick1[1]

		vx = self.canvas.winfo_width()
		vy = self.canvas.winfo_height()

		delta0 = float(self.translationOption.get()) * (dx/vx)*self.vobj.extent[0]
		delta1 = float(self.translationOption.get()) * (dy/vy)*self.vobj.extent[1]

		self.vobj.vrp += (delta0 * self.vobj.u) + (delta1 * self.vobj.vup)
		self.baseClick1 = (event.x, event.y)
		self.updateAxes()
		self.updateLabels()
		self.updatePoints()
		self.updateFits()
	# rotation
	def handleButton2Motion(self, event):
		#delta0: rotate around U
		#delta1: rotate around VUP
		print('handle button 2 motion: %d %d' % (event.x, event.y) )
		delta1 = -(event.x - self.baseClick3[0])*float(self.rotationOption.get())/200*math.pi
		delta0 = (event.y - self.baseClick3[1])*float(self.rotationOption.get())/200*math.pi

		self.vobj = self.originalview.clone()
		self.vobj.rotateVRC(delta0, delta1)
		self.updateAxes()
		self.updateLabels()
		self.updatePoints()
		self.updateFits()
	# scaling
	def handleButton3Motion( self, event):
		print('handle button 3 motion: %d %d' % (event.x, event.y) )

		movey = event.y - self.baseClick2[1]
		delta = 1+(float(self.scalingOption.get())*(movey)/100)

		for i in range(len(self.viewextent)):
			self.vobj.extent[i] = delta*self.viewextent[i]
		
		self.updateAxes()
		self.updateLabels()
		self.updatePoints()
		self.updateFits()
	# prepare for linear regressions
	def handleLinearRegression(self, event = None):
		dialogWindow2 = MyDialogRegression(self.root, self.dobj, title = "Choose Axes")
		if dialogWindow2.userCancelled() == True:
			return
		else:
			self.regressionselections = dialogWindow2.getSelection()
			for pt in self.objects:
				self.canvas.delete(pt)
			self.objects = []
			for obj in self.regressionobj:
				self.canvas.delete(obj)
			self.regressionobj = []
			self.vobj = view.View().clone()
			self.updateAxes()
			self.buildLinearRegression()

	# run linear regressions
	def buildLinearRegression(self, event= None):

		self.headernames = self.regressionselections
		self.rawheaders = self.headernames
		self.buildLabels()
		self.color_axis = None
		self.size_axis = None
		self.x_axis_label.set(self.headernames[0])
		self.color_axis_label.set(self.color_axis)
		self.size_axis_label.set(self.size_axis)

		self.buildPoints()
		self.buildLabels()
		# single linear regression
		if len(self.headernames) == 2:
			# (slope, intercept, r_value, p_value, std_err, minind, mindep, maxind, maxdep)
			results = analysis.single_linear_regression(self.dobj, self.headernames[0], self.headernames[1])
			xmin=results[5]
			xmax=results[7]
			ymin=results[6]
			ymax=results[8]
			m=results[0]
			b=results[1]

			rvalue = results[2]
			# calculating coordinates
			x_r_0 = 0.0
			x_r_1 = 1.0
			y_r_0 = ((xmin * m + b) - ymin)/(ymax - ymin)
			y_r_1 = ((xmax * m + b) - ymin)/(ymax - ymin)
			self.lncoords = np.matrix([[x_r_0,y_r_0,0,1],[x_r_1,y_r_1,0,1]])
			vtm = self.vobj.build()
			lncoords = vtm* self.lncoords.T
			regline = self.canvas.create_line(lncoords[0,0], lncoords[1,0], lncoords[0,1],lncoords[1,1], fill = 'blue', width=2)
			self.regressionobj.append(regline)

			# labels showing all the information
			self.r_value_label = self.canvas.create_text(150, 20, text = "R-Value: " + str(rvalue))
			self.slope_label = self.canvas.create_text(150, 40, text = "Slope: " + str(m))
			self.y_intercept_label = self.canvas.create_text(150, 60, text = "Y-Intercept: " + str(b))
			self.labels.extend([self.r_value_label, self.slope_label,self.y_intercept_label])
		# 3 dimension linear regression
		elif len(self.headernames) == 3:
			# m0, m1, fit (b), minind1, minind2, mindep, maxind2,maxind2, maxdep, r^2
			results = analysis.linear_regression_extension(self.dobj, [self.headernames[0],self.headernames[2]],self.headernames[1])
			x0min = results[3]
			x1min = results[4]
			ymin = results[5]
			x0max = results[6]
			x1max = results[7]
			ymax = results[8]
			m0 = results[0]
			m1= results[1]
			b = results[2]
			
			rvalue = results[0]
			x_r_0 = 0.0
			x_r_1 = 1.0
			x_r_2 = 0.0
			x_r_3 = 1.0

			z_r_0 = 0.0
			z_r_1 = 0.0
			z_r_2 = 1.0
			z_r_3 = 1.0

			y_r_0 = (((x0min * m0) + (x1min * m1) + b) - ymin)/(ymax - ymin)
			y_r_1 = (((x0max * m0) + (x1min * m1) + b) - ymin)/(ymax - ymin)
			y_r_2 = (((x0min * m0) + (x1max * m1) + b) - ymin)/(ymax - ymin)
			y_r_3 = (((x0max * m0) + (x1max * m1) + b) - ymin)/(ymax - ymin)


			self.lncoords = np.matrix([[x_r_0,y_r_0,z_r_0,1],[x_r_1,y_r_1,z_r_1,1],[x_r_3,y_r_3,z_r_3,1], [x_r_2,y_r_2,z_r_2,1] ])
			vtm = self.vobj.build()
			plcoords = (vtm* self.lncoords.T).T

			# self.canvas.create_line(plcoords[0,0], plcoords[0,1], plcoords[1,0], plcoords[1,1])

			regplane = self.canvas.create_polygon([plcoords[0,0],plcoords[0,1],plcoords[1,0], plcoords[1,1], plcoords[2,0],plcoords[2,1],plcoords[3,0], plcoords[3,1]], 
						fill = "thistle", stipple="gray25")

			self.regressionobj.append(regplane)

			# labels showing all the information
			self.r_value_label = self.canvas.create_text(150, 20, text = "R-Value: " + str(rvalue))
			self.slope_label = self.canvas.create_text(150, 40, text = "Slopes: " + str(m0) +"\n" +str(m1))
			self.labels.extend([self.r_value_label, self.slope_label])

	# enable the linear fit to move along with the data
	def updateFits(self):
		try:
			vtm = self.vobj.build()
			coords = (vtm * self.lncoords.T).T
		except AttributeError:
			pass
		else:
			if len(self.headernames) == 2:
				self.canvas.coords(self.regressionobj[0], coords[0,0],coords[0,1],coords[1,0],coords[1,1] )


			elif len(self.headernames) == 3:
				self.canvas.coords(self.regressionobj[0],[coords[0,0],coords[0,1], coords[1,0],coords[1,1], coords[2,0],coords[2,1], coords[3,0],coords[3,1]])

	# automatically transfer to plane views
	def handleXY(self):
		original = view.View().clone()
		#delta0: rotate around U
		#delta1: rotate around VUP
		delta0 = 0
		delta1 = 0

		self.vobj = original.clone()
		self.vobj.rotateVRC(delta0, delta1)
		self.updateAxes()
		self.updateLabels()
		self.updatePoints()
		self.updateFits()
	def handleXZ(self):
		original = view.View().clone()
		#delta0: rotate around U
		#delta1: rotate around VUP

		delta0 = -0.5*math.pi
		delta1 = 0

		self.vobj = original.clone()
		self.vobj.rotateVRC(delta0, delta1)
		self.updateAxes()
		self.updateLabels()
		self.updatePoints()
		self.updateFits()
	def handleYZ(self):
		original = view.View().clone()
		#delta0: rotate around U
		#delta1: rotate around VUP
		delta0 = 0
		delta1 = -0.5*math.pi

		self.vobj = original.clone()
		self.vobj.rotateVRC(delta0, delta1)
		self.updateAxes()
		self.updateLabels()
		self.updatePoints()
		self.updateFits()

	def main(self):
		print('Entering main loop')
		self.root.mainloop()

#---------------- 
# a dialog window 
# from effbor page

class Dialog(tk.Toplevel):
	def __init__(self, parent, dobj, title = None):

		tk.Toplevel.__init__(self,parent)
		self.transient(parent)
		
		self.hitcancel = True
		if title:
			self.title(title)

		self.parent = parent
		self.result = None

		body = tk.Frame(self)
		self.initial_focus = self.body(body, dobj)
		body.pack(padx=5, pady=5)
		self.buttonbox()
		self.grab_set()
		if not self.initial_focus:
			self.initial_focus = self
		self.protocol("WM_DELETE_WINDOW", self.cancel)
		self.geometry("+%d+%d" % (parent.winfo_rootx()+50,
								  parent.winfo_rooty()+50))

		# focus_set to move the keyboard focus to the appropriate widget 
		#(usually the widget returned by the -body- method)
		self.initial_focus.focus_set()
		self.wait_window(self)
	# construction hooks
	def body(self, master):
		# create dialog body.  return widget that should have
		# initial focus.  this method should be overridden
		pass

	def buttonbox(self):
		# add standard button box. override if you don't want the
		# standard buttons

		box = tk.Frame(self)

		w = tk.Button(box, text="OK", width=10, command=self.ok, default=tk.ACTIVE)
		w.pack(side=tk.LEFT, padx=5, pady=5)

		w = tk.Button(box, text="Cancel", width=10, command =self.cancel)
		w.pack(side=tk.LEFT, padx=5, pady=5)

		self.bind("<Return>", self.ok)
		self.bind("<Escape>", self.cancel)

		box.pack()

	# standard button semantics
	def ok(self, event=None):
		if not self.validate() :
			self.initial_focus.focus_set() # put focus back
			return

		self.withdraw()
		self.update_idletasks()
		self.apply()
		self.cancel()		

	def cancel(self, event=None):
		# put focus back to the parent window
		self.parent.focus_set()
		self.destroy()

	# command hooks
	def validate(self):
		return 1 #override

	def apply(self):
		pass #override

#----------------
#Dialog for choosing axes
class MyDialog(Dialog):

	def __init__(self, parent, dobj, title):
		Dialog.__init__(self, parent, dobj,title)
		

	def body(self, master, dobj):

		tk.Label(master, text = "X-Axis Data:").grid(row = 0, column=0)
		tk.Label(master, text = "Y-Axis Data:").grid(row = 0, column=1)
		tk.Label(master, text = "Z-Axis Data:").grid(row = 0, column=2)
		tk.Label(master, text = "Color Data:").grid(row = 0, column=3)
		tk.Label(master, text = "Size Data:").grid(row = 0, column=4)
		self.HList = dobj.get_num_headers()
		self.listbox1 = tk.Listbox(master, exportselection = 0, height = len(self.HList)) 
		for i in self.HList:
			self.listbox1.insert(tk.END, i)
		# self.listbox1.selection_set(0)
		self.listbox1.grid(row = 1, column =0)

		self.listbox2 = tk.Listbox(master, exportselection = 0, height = len(self.HList)) 
		for i in self.HList:
			self.listbox2.insert(tk.END, i)
		self.listbox2.grid(row = 1, column =1)

		self.listbox3 = tk.Listbox(master, exportselection = 0, height = len(self.HList)) 
		for i in self.HList:
			self.listbox3.insert(tk.END, i)
		self.listbox3.grid(row = 1, column =2)

		self.listbox4 = tk.Listbox(master, exportselection = 0, height = len(self.HList)) 
		for i in self.HList:
			self.listbox4.insert(tk.END, i)
		self.listbox4.grid(row = 1, column =3)

		self.listbox5 = tk.Listbox(master, exportselection = 0, height = len(self.HList)) 
		for i in self.HList:
			self.listbox5.insert(tk.END, i)
		self.listbox5.grid(row = 1, column =4)


	# determine if the information provided by the user is sufficient and valid
	def validate(self):
		self.x = self.listbox1.curselection()
		if len(self.x)==0 :
			tk.messagebox.showwarning("Illegal Value","Plase select data for at least X axis.")
			return False

		else:
			return True
	# 
	def apply(self):
		self.x = self.listbox1.curselection()
		if len(self.listbox2.curselection())>0:
			self.y = self.listbox2.curselection()
		else:
			self.y = (-1,)
		
		if len(self.listbox3.curselection())>0:
			self.z = self.listbox3.curselection()
		else:
			self.z = (-1,)

		if len(self.listbox4.curselection())>0:
			self.color = self.listbox4.curselection()
		else:
			self.color =(-1,)
	   
		if len(self.listbox5.curselection())>0:
			self.size = self.listbox5.curselection()
		else:
			self.size = (-1,)
		self.hitcancel = False

	# accessor method; return headers of these dimensions
	def getSelection(self):
		self.HList.append('')
		select_list = self.HList
		x_s = select_list[self.x[0]]
		y_s = select_list[self.y[0]]
		z_s = select_list[self.z[0]]
		color_s = select_list[self.color[0]]
		size_s = select_list[self.size[0]]
		return [x_s, y_s, z_s, color_s, size_s]
	def userCancelled(self):
		return self.hitcancel

#---------------- 
#Dialog for choosing regression data
class MyDialogRegression(Dialog):

	def __init__(self, parent, dobj, title):
		Dialog.__init__(self, parent, dobj, title)

	def body(self, master, dobj):

		tk.Label(master, text = "independent variable:").grid(row = 0, column=0)
		tk.Label(master, text = "dependent variable").grid(row = 0, column=1)
		tk.Label(master, text = "INDEPENDENT variable2").grid(row = 0, column=2)

		self.HList = dobj.get_num_headers()
		self.listbox1 = tk.Listbox(master, exportselection = 0, height = len(self.HList)) 
		for i in self.HList:
			self.listbox1.insert(tk.END, i)
		# self.listbox1.selection_set(0)
		self.listbox1.grid(row = 1, column =0)

		self.listbox2 = tk.Listbox(master, exportselection = 0, height = len(self.HList)) 
		for i in self.HList:
			self.listbox2.insert(tk.END, i)
		self.listbox2.grid(row = 1, column =1)

		self.listbox3 = tk.Listbox(master, exportselection = 0, height = len(self.HList)) 
		for i in self.HList:
			self.listbox3.insert(tk.END, i)
		self.listbox3.grid(row = 1, column =2)

	# determine if the information provided by the user is sufficient and valid
	def validate(self):
		self.ind = self.listbox1.curselection()
		self.dep = self.listbox2.curselection()
		self.ind2 = self.listbox3.curselection()
		if len(self.ind)==0 or len(self.dep)==0  :
			tk.messagebox.showwarning("Illegal Value","Plase select data for two variables.")
			return False
		else:
			return True
	# 
	def apply(self):
		self.ind = self.listbox1.curselection()
		self.dep = self.listbox2.curselection()
		self.ind2 = self.listbox3.curselection()
		self.hitcancel = False

	# accessor method; return headers of these dimensions
	def getSelection(self):
		try:
			ind_s = self.HList[self.ind[0]]
			dep_s = self.HList[self.dep[0]]
		except AttributeError:
			pass
		else:
			ind_s = self.HList[self.ind[0]]
			dep_s = self.HList[self.dep[0]]
			if (len(self.ind2) !=0):
				ind_s2= self.HList[self.ind2[0]]
				return [ind_s,  dep_s, ind_s2]
			else:
				return [ind_s, dep_s]	

	def userCancelled(self):
		return self.hitcancel
#---------------- 
#Dialog for saving pictures
class SavePicDialog(Dialog):
	def __init__(self, parent, dobj, title):
		Dialog.__init__(self, parent, None, title)

	def body(self, master, dobj=None):
		l = tk.Label(master, text = "Save Picture - File name:").grid(row=0)
		self.beginVar = tk.StringVar()
		self.beginVar.set("canvas")
		self.e = tk.Entry(master, textvariable = self.beginVar)
		self.e.focus_set()
		self.e.selection_range( 0, tk.END)
		self.e.grid(row = 0, column =1)

	# determine if the information provided by the user is sufficient and valid
	def validate(self):
		return True
	# 
	def apply(self):
		self.name = self.e.get()
		self.hitcancel = False

	# accessor method; returns the numberof points the user wants to plot. 
	def getFilename(self):
		return self.name

	# returns True if the user hit the Cancel button.
	def userCancelled(self):
		return self.hitcancel



if __name__ == "__main__":
	dapp = DisplayApp(1200, 675)
	dapp.main()


