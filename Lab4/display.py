# Erica Lei
# CS251 Spring2017
# Project 3 Viewing
# due 5 March 2018

import tkinter as tk
from tkinter import filedialog
import math
import random
import numpy as np
import view
import sys
import data


# create a class to build and manage the display
class DisplayApp:

    def __init__(self, width, height, argv):

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
        
        
        self.buildPts()
        self.buildAxes()
        self.buildLabels()

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
        menutext = [ [ 'Open...  \xE2\x8C\x98-O', 'Plot Data  \xE2\x8C\x98-P','-', 'Quit  \xE2\x8C\x98-Q' ] ]

        # menu callback functions
        menucmd = [ [self.handleOpen, self.handlePlotData ,None, self.handleQuit]  ]
        
        # build the menu elements and callbacks
        for i in range( len( self.menulist ) ):
            for j in range( len( menutext[i]) ):
                if menutext[i][j] != '-':
                    self.menulist[i].add_command( label = menutext[i][j], command=menucmd[i][j] )
                else:
                    self.menulist[i].add_separator()

    # create the canvas object
    def buildCanvas(self):
        self.canvas = tk.Canvas( self.root, width=self.initDx, height=self.initDy, background= "#ffa07a" )
        self.canvas.pack( expand=tk.YES, fill=tk.BOTH )
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
        self.buttons.append( ( 'reset', tk.Button( self.cntlframe, text="Reset", command=self.handleResetButton, width=5 ) ) )
        self.buttons[-1][1].pack(side=tk.TOP)  # default side is top

        # EXTENSION
        # control over the interaction constants
        label1 = tk.Label(self.cntlframe, text = "Translation Speed", width = 20)
        label1.pack (side = tk.TOP
            )
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

        # EXTENSION
        # buttons that show 3 planes
        self.buttons.append(( 'x-y plane', tk.Button( self.cntlframe, text="x-y plane", command=self.handleXY, width=10 ) ) )
        self.buttons[-1][1].pack(side=tk.BOTTOM)
        self.buttons.append(( 'x-z plane', tk.Button( self.cntlframe, text="x-z plane", command=self.handleXZ, width=10 ) ) )
        self.buttons[-1][1].pack(side=tk.BOTTOM)
        self.buttons.append(( 'y-z plane', tk.Button( self.cntlframe, text="y-z plane", command=self.handleYZ, width=10 ) ) )
        self.buttons[-1][1].pack(side=tk.BOTTOM)
        return

    # create the axis line objects in their default location
    def buildAxes(self):
       
        vtm = self.vobj.build()
        pts = (vtm * self.axes.T).T
        self.xAxis = self.canvas.create_line(pts[0,0],pts[0,1],pts[1,0],pts[1,1], fill = "black", width = 3)
        self.yAxis = self.canvas.create_line(pts[2,0],pts[2,1],pts[3,0],pts[3,1], fill = "yellow", width = 3)
        self.zAxis = self.canvas.create_line(pts[4,0],pts[4,1],pts[5,0],pts[5,1], fill = "blue", width = 3)
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
    
    # handle plotting data - enable the user to select which columns of data to ploton which axes
    # then builds the data
    def handlePlotData(self):
        self.plotData = []
        pass


    #EXTENSION
    # create the data points
    def buildPts(self):
        # vtm = self.vobj.build()
        # ptcoords = vtm * self.data.T
        # for i in range(ptcoords.shape[1]):
        #     point = self.canvas.create_oval(ptcoords[0,i]-5,  ptcoords[1,i]-5,ptcoords[0,i]+5, ptcoords[1,i]+5, fill="#"+("%06x"%random.randint(0,16777215)), outline='' )
        #     self.objects.append(point)
        pass

    # update the location of each point
    def updatePts(self):
        # vtm = self.vobj.build()
        # ptcoords = vtm * self.data.T
        # i = 0
        # for pt in self.objects:
        #     self.canvas.coords(pt, ptcoords[0,i]-5,  ptcoords[1,i]-5,ptcoords[0,i]+5, ptcoords[1,i]+5)
        #     i += 1
        pass

    #EXTENSION
    # create axis labels
    def buildLabels(self):
        vtm = self.vobj.build()
        pts = (vtm * self.axes.T).T
        self.xLabel = self.canvas.create_text(pts[1,0]+ 10, pts[1,1], text = "X", fill = "black", width = 3)
        self.yLabel = self.canvas.create_text(pts[3,0]+ 10, pts[3,1], text = "Y", fill = "yellow", width = 3)
        self.zLabel = self.canvas.create_text(pts[5,0]+ 10, pts[5,1], text = "Z", fill = "blue", width = 3)
        self.labels.extend([self.xLabel,self.yLabel,self.zLabel])


    # update axis labels
    def updateLabels(self):
        vtm = self.vobj.build()
        pts = (vtm * self.axes.T).T
        # for each line object
            # update the coordinates of the object
        i = 0
        for label in self.labels:
            self.canvas.coords(label, pts[i+1,0] + 10 ,pts[i+1,1] )
            i += 2

    def setBindings(self):
        self.root.bind( '<Button-1>', self.handleButton1 )
        self.root.bind( '<Button-2>', self.handleButton2 )
        self.root.bind( '<Button-3>', self.handleButton3 )
        self.root.bind( '<B1-Motion>', self.handleButton1Motion )
        self.root.bind( '<B2-Motion>', self.handleButton2Motion )
        self.root.bind( '<B3-Motion>', self.handleButton3Motion )
        self.root.bind( '<Control-q>', self.handleQuit )
        self.root.bind( '<Control-o>', self.handleModO )
        self.root.bind( '<Control-Button-1>', self.handleButton2 )
        self.root.bind( '<Control-B1-Motion>', self.handleButton2Motion ) 
        self.root.bind( '<Control-Shift-Button-1>', self.handleButton3 )
        self.root.bind( '<Control-Shift-B1-Motion>', self.handleButton3Motion)
        self.root.bind( '<Command-O>', self.handleOpen )
        self.canvas.bind( '<Configure>', self.handleResize )

        return

    def handleResize(self, event=None):
        pass

    def handleOpen(self):
        print('handleOpen')
        fn = filedialog.askopenfilename( parent=self.root, title='Choose a data file', initialdir='.' )
        self.data = data.Data().read(fn)
        self.data = np.hstack((self.data, self.data.shape[0]*[[1]]))

    def handleModO(self, event):
        self.handleOpen()

    def handleQuit(self, event=None):
        print('Terminating')
        self.root.destroy()

    # clicking reset button
    def handleResetButton(self):
        print('handling reset button')
        self.vobj = view.View().clone()
        self.updateAxes()
        self.updatePts()
        self.updateLabels()

    # translation initiation
    def handleButton1(self, event):
        print('handle button 1: %d %d' % (event.x, event.y))
        self.baseClick1 = (event.x, event.y)

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

        self.vobj.vrp = (delta0 * self.vobj.u) + (delta1 * self.vobj.vup)
        self.updateAxes()
        self.updatePts()
        self.updateLabels()

 
    # rotation
    def handleButton2Motion(self, event):
        #delta0: rotate around U
        #delta1: rotate around VUP
        print('handle button 2 motion: %d %d' % (event.x, event.y) )
        delta1 = -( ((event.x - float(self.rotationOption.get()) *self.baseClick3[0]))/200)*math.pi
        delta0 = ( ((event.y - float(self.rotationOption.get()) *self.baseClick3[1]))/200)*math.pi

        self.vobj = self.originalview.clone()
        self.vobj.rotateVRC(delta0, delta1)
        self.updateAxes()
        self.updatePts()
        self.updateLabels()


    # scaling
    def handleButton3Motion( self, event):
        print('handle button 3 motion: %d %d' % (event.x, event.y) )

        movey = event.y - self.baseClick2[1]
        delta = 1+(float(self.scalingOption.get())*(movey)/100)

        for i in range(len(self.viewextent)):
            self.vobj.extent[i] = delta*self.viewextent[i]
        
        self.updateAxes()
        self.updatePts()
        self.updateLabels()

    # EXTENSION
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
        self.updatePts()
        self.updateLabels()


    def handleXZ(self):
        original = view.View().clone()
        #delta0: rotate around U
        #delta1: rotate around VUP

        delta0 = -0.5*math.pi
        delta1 = 0

        self.vobj = original.clone()
        self.vobj.rotateVRC(delta0, delta1)
        self.updateAxes()
        self.updatePts()
        self.updateLabels()

    def handleYZ(self):
        original = view.View().clone()
        #delta0: rotate around U
        #delta1: rotate around VUP

        delta0 = 0
        delta1 = -0.5*math.pi

        self.vobj = original.clone()
        self.vobj.rotateVRC(delta0, delta1)
        self.updateAxes()
        self.updatePts()
        self.updateLabels()



    def main(self):
        print('Entering main loop')
        self.root.mainloop()

if __name__ == "__main__":
    dapp = DisplayApp(1024, 600, sys.argv)
    dapp.main()


