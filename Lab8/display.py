# Erica Lei
# CS251 Spring2017
# project 7
# Clustering


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
		self.PCAfilelist = []
		self.Clusterfilelist = []
		self.meanpoints=[]
		# a list of colors used for clustering/classification; discriminative
		self.color_discriminative = ['deep sky blue','gold','thistle', 'SlateBlue2','LightBlue3',
									'SpringGreen2','DarkGoldenRod1','brown4','pink3','purple1',
									'aquamarine','tomato','LemonChiffon2','SteelBlue4','turquoise2',
									'DarOliveGreen3','sienna4','coral1','VioletRed2','gray7' 
									]
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
		menutext = [ [ 'Open...  \u2318-O', "-",'Open PCA File  \u2318-P',  "-",'Save Canvas  \u2318-S', "-",'Quit  \u2318-Q' ] ]

		# menu callback functions
		menucmd = [ [self.handleOpen,None,self.handlePCAOpen, None, self.handleSave, None, self.handleQuit]  ]
		
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
		self.canvas.create_window(450, 20, window=label_x_ind)
		self.x_axis_label = tk.StringVar()
		label_x = tk.Label(self.canvas, textvariable = self.x_axis_label, relief = tk.RAISED, justify = tk.LEFT)
		label_x.pack()
		self.canvas.create_window(550, 20,  window = label_x)

		label_y_ind = tk.Label(self.canvas, text = "y-axis data:",)
		label_y_ind.pack()
		self.canvas.create_window(450, 40, window=label_y_ind)
		self.y_axis_label = tk.StringVar()
		label_y = tk.Label(self.canvas, textvariable = self.y_axis_label, relief = tk.RAISED, justify = tk.LEFT)
		label_y.pack()
		self.canvas.create_window(550, 40, window = label_y)

		label_z_ind = tk.Label(self.canvas, text = "z-axis data:",)
		label_z_ind.pack()
		self.canvas.create_window(450, 60, window=label_z_ind)
		self.z_axis_label = tk.StringVar()
		label_z = tk.Label(self.canvas, textvariable = self.z_axis_label, relief = tk.RAISED, justify = tk.LEFT)
		label_z.pack()
		self.canvas.create_window(550, 60,  window = label_z)

		label_color_ind = tk.Label(self.canvas, text = "color axis data:",)
		label_color_ind.pack()
		self.canvas.create_window(450, 80, window=label_color_ind)
		self.color_axis_label = tk.StringVar()
		label_color = tk.Label(self.canvas, textvariable = self.color_axis_label, relief = tk.RAISED, justify = tk.LEFT)
		label_color.pack()
		self.canvas.create_window(550, 80,  window = label_color)

		label_size_ind = tk.Label(self.canvas, text = "size axis data:",)
		label_size_ind.pack()
		self.canvas.create_window(450, 100, window=label_size_ind)
		self.size_axis_label = tk.StringVar()
		label_size = tk.Label(self.canvas, textvariable = self.size_axis_label, relief = tk.RAISED, justify = tk.LEFT)
		label_size.pack()
		self.canvas.create_window(550, 100,  window = label_size)
		return

	# build a frame and put controls in it
	def buildControls(self):
		# make a control frame
		self.cntlframe = tk.Frame(self.root)
		self.cntlframe.pack(side=tk.RIGHT, padx=2, pady=2, fill=tk.Y)
		#separation of cntlframe and canvas
		sep = tk.Frame( self.root, height=self.initDy, width=2, bd=1, relief=tk.SUNKEN )
		sep.pack( side=tk.RIGHT, padx = 2, pady = 2, fill=tk.Y)
		# make a frame at the right
		self.frame2 = tk.Frame(self.cntlframe)
		self.frame2.pack(side = tk.RIGHT, padx=2, pady=2, fill =tk.Y)


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
		label = tk.Label(self.cntlframe, text= "Linear Regression", width = 25, font=("Times New Roman", 16), bg="salmon1")
		label.pack(side=tk.TOP)
		self.buttons.append(('plot regression line', tk.Button(self.cntlframe, text = "Run Regression", command =self.handleLinearRegression, width = 15 )))		
		self.buttons[-1][1].pack(side=tk.TOP)
		
		# run PCA button 
		label = tk.Label(self.cntlframe, text= "Principle Component Analysis", width =25,font=("Times New Roman", 16), bg="salmon1")
		label.pack(side=tk.TOP)
		self.buttons.append(('Principle Component Analysis', tk.Button(self.cntlframe, text = "Plot PCA", command =self.handlePlotPCA, width = 10 )))
		self.buttons[-1][1].pack( side = tk.TOP)
		self.buttons.append(('Delete Entry', tk.Button(self.cntlframe, text = "Delete Entry", command=self.deleteEntry)))
		self.buttons[-1][1].pack( side = tk.TOP)
		self.buttons.append(('Show Details', tk.Button(self.cntlframe, text = "Show Details", command=self.handleShowDetails)))
		self.buttons[-1][1].pack( side = tk.TOP)		

		#list that stores the PCA result
		self.PCA_result_listbox = tk.Listbox(self.cntlframe)
		self.PCA_result_listbox.pack(side =tk.TOP, pady=5)

		# control over the interaction constants
		label = tk.Label(self.cntlframe, text= "Interaction Options", width =25,font=("Times New Roman", 16), bg="salmon1")
		label.pack(side=tk.TOP)
		
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
		# self.buttons.append(( 'x-y plane', tk.Button( self.cntlframe, text="x-y plane", command=self.handleXY, width=5) ) )
		# self.buttons[-1][1].pack(side=tk.TOP)
		# self.buttons.append(( 'x-z plane', tk.Button( self.cntlframe, text="x-z plane", command=self.handleXZ, width=5) ) )
		# self.buttons[-1][1].pack(side=tk.TOP)
		# self.buttons.append(( 'y-z plane', tk.Button( self.cntlframe, text="y-z plane", command=self.handleYZ, width=5) ) )
		# self.buttons[-1][1].pack(side=tk.TOP)

		# label with mouse coords 
		self.c = tk.StringVar()
		label4 = tk.Label(self.cntlframe, textvariable = self.c, relief = tk.RAISED)
		label4.pack(side=tk.BOTTOM, pady=4)
		# label "mouse position"
		label4 = tk.Label(self.cntlframe, text = "Mouse Position (x,y)", relief = tk.RAISED)
		label4.pack(side=tk.BOTTOM)

		# clustering controls
		label5 = tk.Label(self.frame2, text= "Clustering", width =25,font=("Times New Roman", 16), bg="salmon1")
		label5.grid(row=0, column=0)
		self.buttons.append(('Find Clusters', tk.Button(self.frame2, text = "Find Clusters", command = self.handleClustering, width = 10 )))
		self.buttons[-1][1].grid( row=1, column = 0)
		self.buttons.append(('Delete Entry', tk.Button(self.frame2, text = "Delete Entry", command=self.deleteClusterEntry)))
		self.buttons[-1][1].grid( row=3, column = 0)
		self.buttons.append(('Show Cluster Details', tk.Button(self.frame2, text = "Show Cluster Details", command=self.handleShowClusterDetails)))
		self.buttons[-1][1].grid( row=4, column = 0)		

		#list that stores the cluster result
		self.Cluster_result_listbox = tk.Listbox(self.frame2)
		self.Cluster_result_listbox.grid( row=2, column = 0)
		return
	
	def setBindings(self):
		self.root.bind( '<Button-1>', self.handleButton1 )
		self.root.bind( '<Button-2>', self.handleButton2 )
		self.root.bind( '<Button-3>', self.handleButton3 )
		self.root.bind( '<B1-Motion>', self.handleButton1Motion )
		self.root.bind( '<B2-Motion>', self.handleButton2Motion )
		self.root.bind( '<B3-Motion>', self.handleButton3Motion )
		self.root.bind( '<Control-q>', self.handleQuit )
		self.root.bind( '<Control-p>', self.handlePCAOpen)
		self.root.bind( '<Control-o>', self.handleModO )
		self.root.bind( '<Control-s>', self.handleSave)
		self.root.bind( '<Control-r>', self.handleLinearRegression )
		self.root.bind( '<Control-Button-1>', self.handleButton2 )
		self.root.bind( '<Control-B1-Motion>', self.handleButton2Motion ) 
		self.root.bind( '<Control-Shift-Button-1>', self.handleButton3 )
		self.root.bind( '<Control-Shift-B1-Motion>', self.handleButton3Motion)
		self.root.bind( '<Shift-Button-1>', self.displayInfo )
		self.canvas.bind( '<Configure>', self.handleResize )
		self.canvas.bind( '<Motion>', self.trackMouse)
		return
	# track the mouse's coords
	def trackMouse(self, event):
		string = str(event.x)+" , "+str(event.y)
		self.c.set(string)
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
	# show data point values when hold shift and click
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
				if str(selections[3]) != "CurrentClusterResult":
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
		for rec in self.meanpoints:
			self.canvas.delete(rec)
		self.meanpoints = []
		# reset orientation
		self.vobj = view.View().clone()
		self.updateAxes()
		self.updateLabels()

		self.data = analysis.normalize_columns_separately(self.headernames, self.dobj)

		s = self.Cluster_result_listbox.curselection()[0]
		if s!= None:		
			self.curkobj = self.Clusterfilelist[s]
		# 	self.meandata= self.curkobj.get_means()
		# 	print("MEAN,", self.meandata)
		# 	k=self.curkobj.get_numeric_points()
		# 	self.dobj.addRow(self.meandata)
			# self.data = analysis.normalize_columns_separately(self.headernames, self.dobj, datatype = 0)
			# self.meandata = self.data[::-1]
			# self.meandata = self.meandata[0:k]
			# self.data = self.data[0:self.data.shape[0]-k]
			# self.meandata = self.meandata[::-1]

		if len(self.headernames) == 2:
			# add a column of 0's and homogeneous coordinate
			self.coords = np.hstack((self.data, self.data.shape[0]*[[0]], self.data.shape[0]*[[1]]))
			# if s!= None:
				# self.meancoords = np.hstack((self.meandata, self.meandata.shape[0]*[[0]], self.meandata.shape[0]*[[1]]))
			self.y_axis_label.set(self.headernames[1])
			self.z_axis_label.set(None)
		
		elif len(self.headernames) == 3:
			# add only homogeneous coordinate
			self.coords = np.hstack((self.data, self.data.shape[0]*[[1]]))
			# if s!=None:
			# 	self.meancoords = np.hstack((self.meandata, self.meandata.shape[0]*[[1]]))		
			self.y_axis_label.set(self.headernames[1])
			self.z_axis_label.set(self.headernames[2])

		if self.color_axis == "CurrentClusterResult":
			self.colors = self.curkobj.get_c()
			self.curkobj.add_c_means()
		elif (self.color_axis!= "CurrentClusterResult") and (self.color_axis != None) :
			# normalize color axis
			self.colors = []
			norm_colors = analysis.normalize_columns_separately([self.color_axis], self.dobj)
			for i in range(self.data.shape[0]):
				alpha = float(norm_colors[i,0])
				rgb = '#%02x%02x%02x'%(int(alpha *255), int((1-alpha)*255), 0)
				self.colors.append(rgb)
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
			x0= ptcoords[0,i]- 2*float(self.sizes[i,0])-1
			y0= ptcoords[1,i]- 2*float(self.sizes[i,0])-1
			x1= ptcoords[0,i]+ 2*float(self.sizes[i,0])+1
			y1= ptcoords[1,i]+ 2*float(self.sizes[i,0])+1
			
			point = self.canvas.create_oval( x0,y0,x1,y1, 
											fill=self.colors[i],
											outline='' )
			self.objects.append(point)

		# if s!=None:
		# 	meancoords = vtm * self.meancoords.T
		# 	meancolors=self.curkobj.get_c_means()
		# 	for j in range(meancoords.shape[1]):
		# 		x0= meancoords[0,j]- 2*float(self.sizes[j,0]) -1
		# 		y0= meancoords[1,j]- 2*float(self.sizes[j,0]) -1 
		# 		x1= meancoords[0,j]+ 2*float(self.sizes[j,0]) +1
		# 		y1= meancoords[1,j]+ 2*float(self.sizes[j,0]) +1 
		# 		meanp = self.canvas.create_rectangle( x0,y0,x1,y1, 
		# 										fill= meancolors[j],
		# 										outline='black' )
		# 		self.meanpoints.append(meanp)
	# update the location of each point
	def updatePoints(self):
		if len(self.objects) == 0:
			pass
		else:
			vtm = self.vobj.build()
			ptcoords = vtm * self.coords.T
			i = 0
			for pt in self.objects:
				x0= ptcoords[0,i]- 2*float(self.sizes[i,0]) -1
				y0= ptcoords[1,i]- 2*float(self.sizes[i,0]) -1
				x1= ptcoords[0,i]+ 2*float(self.sizes[i,0]) +1
				y1= ptcoords[1,i]+ 2*float(self.sizes[i,0]) +1
				self.canvas.coords(pt,x0,y0,x1,y1)
				i += 1
	# update the means for clustering
	def updateMeans(self):
		if len(self.meanpoints)==0:
			pass
		else:
			vtm = self.vobj.build()
			ptcoords = vtm * self.meancoords.T
			i = 0
			for pt in self.meanpoints:
				x0= ptcoords[0,i]- 2*float(self.sizes[i,0]) -1
				y0= ptcoords[1,i]- 2*float(self.sizes[i,0]) -1
				x1= ptcoords[0,i]+ 2*float(self.sizes[i,0]) +1
				y1= ptcoords[1,i]+ 2*float(self.sizes[i,0]) +1
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
		self.baseClick1 = (event.x, event.y)
		for t in self.txt:
			self.canvas.delete(t)
		self.txt = []
	# rotation initiation
	def handleButton2(self, event):
		self.baseClick3 = (event.x, event.y)
		self.originalview = self.vobj.clone()
	# scaling initiation
	def handleButton3(self, event):
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
		self.updateMeans()
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
		self.updateMeans()
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
		self.updateMeans()
		self.updateFits()
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

	''' ----- linear regression stuff ----- '''
	# prepare for linear regressions
	def handleLinearRegression(self, event = None):
		dialogWindow2 = MyDialogRegression(self.root, self.dobj, title = "Choose Axes for Regression")
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

	''' ----- PCA stuff ----- '''
	#Open PCA file and select headers
	def handlePCAOpen(self, event=None):
		self.handleOpen()
		#select axes from dialog window
		dialogWindow3 = MyDialogPCAAxes(self.root, self.dobj, title = "Choose Axes")
		if dialogWindow3.userCancelled() == True :
			print("user cancelled")
			return
		else:
			selections = dialogWindow3.getSelection()
			self.normcheck = dialogWindow3.getChecked()
			if self.normcheck == True:
				pca_dobj = analysis.pca(self.dobj, selections, True)
			else:
				pca_dobj = analysis.pca(self.dobj, selections, False)
			self.PCAfilelist.append(pca_dobj)
			# name the analysis file
			NameDialog = MyDialogNamePCA(self.root,  dobj = None, title = "Name the PCA result")
			if NameDialog.userCancelled == True:
				return
			else:
				file = NameDialog.getFilename()
				self.PCA_result_listbox.insert(tk.END,file)
	#delete entry of a named PCA
	def deleteEntry(self, event = None):
		s = self.PCA_result_listbox.curselection()[0]
		self.PCA_result_listbox.delete(s)
		del self.PCAfilelist[s]
	#when press the button of run PCA, do the following
	def handlePlotPCA(self, event = None):
		self.handleChoosePCAAxes()
		for bar in self.bars:
			self.canvas.delete(bar)
		self.bars= []
		self.buildPCAPoints()
		self.buildLabels()
	# let users choose axes to plot and save headers selected
	def handleChoosePCAAxes(self, event =None):
		s = self.PCA_result_listbox.curselection()[0]
		self.PCAobj = self.PCAfilelist[s]

		dialogWindow4 = MyDialog(self.root, self.PCAobj, title = "Choose Axes to Plot PCA")
		if dialogWindow4.userCancelled() ==True :
			return
		else:
			selections =  dialogWindow4.getSelection()
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
			self.y_axis_label.set(self.headernames[1])
			self.z_axis_label.set(self.headernames[2])
			self.color_axis_label.set(self.color_axis)
			self.size_axis_label.set(self.size_axis)
	# view data projected on to the first 3 eigenvectors
	def buildPCAPoints(self,event = None):
		# clear all data
		for pt in self.objects:
			self.canvas.delete(pt)
		self.objects = []

		# reset orientation
		self.vobj = view.View().clone()
		self.updateAxes()
		self.updateLabels()

		self.raw = self.PCAobj.get_data(self.rawheaders)
		self.data = analysis.normalize_columns_together(self.rawheaders, self.PCAobj,1)
		# add only homogeneous coordinate
		self.coords = np.hstack((self.data[:,[0,1,2]], self.data.shape[0]*[[1]]))
		
		if self.color_axis != None:
			self.colors = self.data[:,3]
		else:
			# if not specified, use 1
			self.colors = np.matrix([[1]]*self.data.shape[0])

		if self.size_axis != None:
			self.sizes = self.data[:,4]
		else:
			# if not specified, use 5
			self.sizes = np.matrix([[3]]*self.data.shape[0])
		# draw points
		vtm = self.vobj.build()
		ptcoords = vtm * self.coords.T
		for i in range(ptcoords.shape[1]):
			x0= ptcoords[0,i]- 2*float(self.sizes[i,0]) -1
			y0= ptcoords[1,i]- 2*float(self.sizes[i,0]) -1
			x1= ptcoords[0,i]+ 2*float(self.sizes[i,0]) +1
			y1= ptcoords[1,i]+ 2*float(self.sizes[i,0]) +1
			alpha = float(self.colors[i,0])
			rgb = (int(alpha *255), int((1-alpha)*255), 0)
			point = self.canvas.create_oval( x0,y0,x1,y1, 
											fill='#%02x%02x%02x'%rgb,
											outline='' )
			self.objects.append(point)
	# display information of PCA
	def handleShowDetails(self,event = None):
		if len(self.PCA_result_listbox.curselection()) > 0:
			s = self.PCA_result_listbox.curselection()[0]
			PCAobj_selected = self.PCAfilelist[s]
			dialogWindow5 = MyDialogPCAInfo(self.root, PCAobj_selected, title = "Information of PCA")
			if dialogWindow5.userCancelled() ==True :
				return

	''' ----- Clustering stuff ----- ''' 
	# handle Clustering
	def handleClustering(self, event = None):
		self.handleChooseClusterAxes()
		for bar in self.bars:
			self.canvas.delete(bar)
		self.bars= []
	# create smooth color palette (gray scale)
	def color_smooth(self,n):
		step = 256/(n)
		ret = []
		r=1
		g=1
		b=1
		for i in range(0,n):
			r += int(step)
			g += int(step)
			b += int(step)
			ctuple = (int(0.21*r+0.72*g+0.07*b),int(0.21*r+0.72*g+0.07*b), int(0.21*r+0.72*g+0.07*b))
			color = '#%02x%02x%02x' % ctuple
			ret.append(color)
		return ret
	# select axes from dialog window, and only save selections 
	def handleChooseClusterAxes(self, event = None):
		
		try:
			dialogWindow6 = MyDialogKmeans(self.root, self.dobj, title = "Choose columns for clustering projection")
			if dialogWindow6.userCancelled() ==True :
				return
			else:
				selections = dialogWindow6.getSelection()#[headers, self.dm, self.k, self.palette ]
				whiten = dialogWindow6.getChecked()
				self.dm = int(selections[-3])
				self.k = int(selections[-2])
				self.palette = int(selections[-1])
				headers = selections[0:-3]
				# build the kmeans object
				self.kobj = analysis.getkobj(self.dobj, headers, self.k, self.dm, whiten)
				# set description length
				MDL = analysis.kmeans_quality(self.kobj.get_errors(), self.k, self.dobj.get_num_points())
				self.kobj.set_quality(MDL)

				if self.palette== 0:
					self.Clustercolors = self.color_smooth(self.k)
				else:
					if self.k<=20:
						self.Clustercolors = self.color_discriminative 
					else: 
						add = []
						for i in range(self.k-21):
							color = "#%02x%02x%02x" %(random.randrange(255),random.randrange(255),random.randrange(255))
							add.append(color)
						self.Clustercolors = self.color_discriminative+add
				self.kobj.add_c(self.Clustercolors)
				self.Clusterfilelist.append(self.kobj)
				# name clustering results
				NameDialog = MyDialogNameKmeans(self.root,  dobj = None, title = "Name the clustering result")
				if NameDialog.userCancelled == True:
					return
				else:
					file = NameDialog.getFilename()
					self.Cluster_result_listbox.insert(tk.END,file)

		except AttributeError:
			tk.messagebox.showwarning("No File Open", "Please open a file from the menu.")
			return
	# delete one cluster entry form the listbox 
	def deleteClusterEntry(self, event = None):
		s = self.Cluster_result_listbox.curselection()[0]
		self.Cluster_result_listbox.delete(s)
		del self.Clusterfilelist[s]
	# show detils of cluster information and legend
	def handleShowClusterDetails(self, event = None):
		if len(self.Cluster_result_listbox.curselection()) > 0:
			s = self.Cluster_result_listbox.curselection()[0]
			Clusterobj_selected = self.Clusterfilelist[s]
			print(s, Clusterobj_selected)
			dialogWindow7 = MyDialogClusterInfo(self.root, Clusterobj_selected, title = "Information of Clustering")
			if dialogWindow7.userCancelled() ==True :
				return

	def main(self):
		print('Entering main loop')
		self.root.mainloop()

#---------------- 
# a dialog window (parent)
class Dialog(tk.Toplevel):
	def __init__(self, parent, dobj, title = None):

		tk.Toplevel.__init__(self,parent)
		self.transient(parent)
		
		self.hitcancel = True
		if title:
			self.title(title)

		self.parent = parent

		self.result = None
		self.var1 = tk.IntVar()
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
		self.HList = dobj.get_headers()
		self.listbox1 = tk.Listbox(master, exportselection = 0) 
		for i in self.HList:
			self.listbox1.insert(tk.END, i)
		# self.listbox1.selection_set(0)
		self.listbox1.grid(row = 1, column =0)

		self.listbox2 = tk.Listbox(master, exportselection = 0) 
		for i in self.HList:
			self.listbox2.insert(tk.END, i)
		self.listbox2.grid(row = 1, column =1)

		self.listbox3 = tk.Listbox(master, exportselection = 0) 
		for i in self.HList:
			self.listbox3.insert(tk.END, i)
		self.listbox3.grid(row = 1, column =2)

		self.listbox4 = tk.Listbox(master, exportselection = 0 ) 
		self.listbox4.insert(tk.END, "CurrentClusterResult")
		for i in self.HList:
			self.listbox4.insert(tk.END, i)
		self.listbox4.grid(row = 1, column =3)

		self.listbox5 = tk.Listbox(master, exportselection = 0 ) 
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
		if self.color[0] == 0:
			color_s = "CurrentClusterResult"
		else:
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
#---------------- 
#Dialog for chossing axes to run PCA
class MyDialogPCAAxes(Dialog):
	def __init__(self, parent, dobj, title):
		Dialog.__init__(self, parent, dobj, title)
		

	def body(self, master, dobj):
		#choose axes
		tk.Label(master, text = "Choose PCA Headers").grid(row = 0, column=0)
		self.headers = dobj.get_num_headers()
		self.listbox = tk.Listbox(master, exportselection = 0, height = len(self.headers), selectmode=tk.EXTENDED) 
		for i in self.headers:
			self.listbox.insert(tk.END, i)
		self.listbox.grid(row = 1, column =0)
		#choose if normalize
		tk.Checkbutton(master, text="Normalize", variable=self.var1).grid(row=3, column=0)

	# determine if the information provided by the user is sufficient and valid
	def validate(self):
		self.idx = self.listbox.curselection()
		if len(self.idx)<3 :
			tk.messagebox.showwarning("Illegal Value","Plase select at least 3 eigenvectors to run PCA")
			return False
		else:
			return True
	
	def apply(self):
		self.norm = self.var1.get()
		self.hitcancel = False

	# accessor method; return headers of these dimensions
	def getSelection(self):
		selected = []
		for i in self.idx:
			s = self.headers[i]
			selected.append(s)
		return selected
	# accessor; return if the Normalized option is chosen
	def getChecked(self):
		if self.norm == 0:
			return False
		else:
			return True

	def userCancelled(self):
		return self.hitcancel
#---------------- 
#Dialog for saving PCA result
class MyDialogNamePCA(Dialog):
	def __init__(self, parent, dobj, title):
		Dialog.__init__(self, parent, None, title)

	def body(self, master, dobj=None):
		l = tk.Label(master, text = "Save PCA Result - File name:").grid(row=0)
		self.beginVar = tk.StringVar()
		self.beginVar.set("PCA result")
		self.e = tk.Entry(master, textvariable = self.beginVar)
		self.e.focus_set()
		self.e.selection_range( 0, tk.END)
		self.e.grid(row = 0, column =1)

	# determine if the information provided by the user is sufficient and valid
	def validate(self):
		return True
	# 
	def apply(self):
		self.PCAname = self.e.get()
		self.hitcancel = False

	# accessor method; returns the numberof points the user wants to plot. 
	def getFilename(self):
		return self.PCAname

	# returns True if the user hit the Cancel button.
	def userCancelled(self):
		return self.hitcancel
#---------------- 
#Dialog for displaying PCA information
class MyDialogPCAInfo(Dialog):
	def __init__(self, parent, dobj, title):
		Dialog.__init__(self, parent, dobj, title)
		
	def body(self, master, dobj):
		self.d = dobj		
		tk.Label(master, text="E-vec", borderwidth=3).grid(row = 0, column = 0)
		first = 1
		for h in self.d.get_headers():
			tk.Label(master, text=h, borderwidth=3).grid(row=first, column=0)
			first += 1 #1st col

		tk.Label(master, text = "E-val", borderwidth=3).grid(row = 0, column = 1)
		second = 1
		sumV = 0
		for v in self.d.get_eigenvalues():
			sumV += v
			tk.Label(master, text=str('%.4f' % v), borderwidth=3).grid(row=second, column=1)
			second += 1 #2nd col

		third = 1
		percentSum = 0
		tk.Label(master, text="Cumulative", borderwidth=3).grid(row=0, column=2)
		for v in self.d.get_eigenvalues():
			percentSum += v/sumV
			tk.Label(master, text=str('%.4f' % percentSum), borderwidth=2).grid(row=third, column=2)
			third += 1 #3rd col

		other = 3
		for h in self.d.get_original_headers():
			tk.Label(master, text=h, borderwidth=3).grid(row=0, column=other)
			other += 1
		eigvec = self.d.get_eigenvectors()
		for r in range(0, len(eigvec)):
			for c in range(len(self.d.get_eigenvectors())):
				tk.Label(master, text=str('%.4f' % eigvec.item(r,c)), borderwidth=2).grid(row=r+1, column=c+3) # all other cols


	# determine if the information provided by the user is sufficient and valid
	def validate(self):
		return True
	# 
	def apply(self):
		self.hitcancel = False

	# returns True if the user hit the Cancel button.
	def userCancelled(self):
		return self.hitcancel
#---------------- 
#Dialog for axes and Kmeans, return [selections of cols, self.dm, self.k,self.palette ]
class MyDialogKmeans(Dialog):
	def __init__(self, parent, dobj, title):
		Dialog.__init__(self, parent, dobj,title)
	def body(self, master, dobj):
		tk.Label(master, text = "Cluster Dimensions").grid(row = 0, column=0)

		self.headers = dobj.get_num_headers()
		self.listbox = tk.Listbox(master, exportselection = 0, height = len(self.headers), selectmode=tk.EXTENDED) 
		for i in self.headers:
			self.listbox.insert(tk.END, i)
		self.listbox.grid(row = 1, column =0)

		# for entering K means 
		tk.Label(master, text = "Number of Clusters (K)").grid(row = 0, column=1)
		self.e = tk.Entry(master)
		self.e.grid(row = 1, column =1)

		# for selecting distance metrics
		self.Dist_Metrics = dict([("L2 Norm",0),("L1 Norm", 1),("Correlation", 2),("Hamming", 3), ("Cosine", 4)])
		tk.Label(master, text = "Distance Metric:").grid(row = 2, column=0)
		self.listbox5 = tk.Listbox(master, exportselection = 0)
		self.listbox5.selection_set(0)
		for k,v in self.Dist_Metrics.items():
			self.listbox5.insert(tk.END, k)
		self.listbox5.grid(row = 3, column=0)

		# for selecting color schemes
		tk.Label(master, text = "Color Scheme:").grid(row = 2, column=1)
		self.listbox6 = tk.Listbox(master, exportselection = 0)
		self.listbox6.selection_set(1)	
		self.listbox6.insert(tk.END, "Smooth Color Palette")
		self.listbox6.insert(tk.END, "Discrimitive Color Palette")
		self.listbox6.grid(row = 3, column=1)
		#choose if whiten
		tk.Checkbutton(master, text="Whiten", variable=self.var1).grid(row=0, column=2)


	# determine if the information provided by the user is sufficient and valid
	def validate(self):
		self.idx = self.listbox.curselection()
		self.dm =self.listbox5.curselection()
		self.cs = self.listbox6.curselection()
		self.k = self.e.get()
		self.whiten = self.var1.get()
		if len(self.idx)==0 or len(self.dm)==0 or(self.cs)==0 :
			tk.messagebox.showwarning("Illegal Value","Please select data for at least X axis and Distance Metric")
			return False
		elif len(self.k)==0:
			tk.messagebox.showwarning("Empty K","Please enter numer of clusters to predict")
			return False
		else:
			return True
	# 
	def apply(self):

		self.hitcancel = False

	# accessor method; return headers of these dimensions
	def getSelection(self):
		selected = []
		for i in self.idx:
			s = self.headers[i]
			selected.append(s)	
		return selected+[self.dm[0],self.k,self.cs[0]]

	def getChecked(self):
		if self.whiten == 0:
			return False
		else:
			return True

	def userCancelled(self):
		return self.hitcancel
#---------------- 
#Dialog for saving cluster data result
class MyDialogNameKmeans(Dialog):
	def __init__(self, parent, dobj, title):
		Dialog.__init__(self, parent, None, title)

	def body(self, master, dobj=None):
		l = tk.Label(master, text = "Save Cluster Result - File name:").grid(row=0)
		self.beginVar = tk.StringVar()
		self.beginVar.set("Cluster result")
		self.e = tk.Entry(master, textvariable = self.beginVar)
		self.e.focus_set()
		self.e.selection_range( 0, tk.END)
		self.e.grid(row = 0, column =1)

	# determine if the information provided by the user is sufficient and valid
	def validate(self):
		return True
	# 
	def apply(self):
		self.Clustername = self.e.get()
		self.hitcancel = False

	# accessor method; 
	def getFilename(self):
		return self.Clustername

	# returns True if the user hit the Cancel button.
	def userCancelled(self):
		return self.hitcancel
#---------------- 
#Dialog for displaying cluster information
class MyDialogClusterInfo(Dialog):
	def __init__(self, parent, dobj, title):
		Dialog.__init__(self, parent, dobj, title)
		
	def body(self, master, dobj):
		colors = dobj.get_c_means()
		means = np.round(dobj.get_means(),2)
		des_len = dobj.get_quality()
		tk.Label(master, text="Description Length:  ", font=("Times", 15, "bold")).grid(row = 0, column = 0)
		tk.Label(master, text=str('%.4f' % des_len), font=("Times", 15, "bold")).grid(row = 0, column = 1)
		row =1
		col = 0
		i=0
		for color in colors:
			tk.Label(master, text="", background= color, width = 5).grid(row = row, column = col)
			tk.Label(master, text=means[i,:] ).grid(row=row+1, column=col)
			i+=1
			col += 1
			if (col>7):
				col = 0
				row += 2

	# determine if the information provided by the user is sufficient and valid
	def validate(self):
		return True
	# 
	def apply(self):
		self.hitcancel = False

	# returns True if the user hit the Cancel button.
	def userCancelled(self):
		return self.hitcancel

if __name__ == "__main__":
	dapp = DisplayApp(1400, 675)
	dapp.main()