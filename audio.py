import sys
from PyQt5 import QtGui, QtCore, QtWidgets
import numpy as np
import pyqtgraph as pg

#Initialization Variables
region = pg.LinearRegionItem()
minX = 0
maxX = 0
vb = []
data1 = 0 
data2 = 0
dataPosX = 0

#Cross hair generation in terms of vertical and horizontal line
vLine = pg.InfiniteLine(angle = 90, movable = False)
hLine = pg.InfiniteLine(angle = 90, movable = False)

Colors_Set = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120), (44, 160, 44), (152, 223, 138)]

#Naming the curves in major Legend
majors = ["Sine", "Cosine"]

#Controlling Background Colors
pg.setConfigOption("background", "w")

#Major Class Definition
class pyshine_plot(QtGui.QWidget):
    def __init__(self):
        global dataPosX
        super(pyshine_plot, self).__init__()
        self.amplitude = 10
        self.init_ui()
        self.t = 0
        self.qt_connections()
        self.num_of_curves = 2

        plotCurveIds = ["%d" % x for x in np.arange(self.num_of_curves)]
        curvePointsIds = ["%d" % x for x in np.arange(self.num_of_curves)]
        textIds = ["%d" % x for x in np.arange(self.num_of_curves)]
        arrowIds = ["%d" % x for x in np.arange(self.num_of_curves)]
        dataIds = ["%d" % x for x in np.arange(self.num_of_curves)]

        self.plotcurves = plotCurveIds
        self.curvePoints = curvePointsIds
        self.texts = textIds
        self.arrows = arrowIds
        self.data = dataIds


    # Iteration of the num of Curves
        for k in range (self.num_of_curves):
            self.plotcurves[k] = pg.PlotCurveItem()
    
    # Here we can call an update plot functions
        self.updateplot()
    
    # Here we can again use the for loop for the rest of the items 
        for k in range (self.num_of_curves):
            self.plotwidget.addItem(self.plotcurves[k])
            self.curvePoints[k] = pg.CurvePoint(self.plotcurves[k])
            self.plotwidget.addItem(self.curvePoints[k])
            self.texts[k] = pg.TextItem(str(k), color = Colors_Set[k], anchor = (0.5, -1.0))
            self.texts[k].setParentItem(self.curvePoints[k])
            self.arrows[k] = pg.ArrowItem(angle = 60, pen = Colors_Set[k], brush = Colors_Set[k])
            self.arrows[k].setParentItem(self.curvePoints[k])

    # Proxy Signal 
        self.proxy = pg.SignalProxy(self.plotwidget.scene().sigMouseMoved, rateLimit = 60, slot = self.MouseMoved)
        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.moveplot)
        self.timer.start(1000)

    # Init_ui Functions
    def init_ui(self):
        global region
        global minX
        global maxX
        global vLine
        global hLine
        global vb
        self.setWindowTitle("PyShine")
        self.label = pg.LabelItem(justify = "left")
        hbox = QtGui.QVBoxLayout()

        self.setLayout(hbox)
        self.plotwidget = pg.PlotWidget()
        self.plotwidget.addItem(vLine, ignoreBounds = True)
        self.vb = self.plotwidget.plotItem.vb
        self.plotwidget.addItem(self.label)
        hbox.addWidget(self.plotwidget)
        self.increasebutton = QtGui.QPushButton("Increase Amplitude")
        self.decreasebutton = QtGui.QPushButton("Decrease Amplitude")

        #Add Buttons to the horizontal box hbox
        hbox.addWidget(self.increasebutton)
        hbox.addWidget(self.decreasebutton)
        self.show()
    
    #Mouse Moved Function
    def MouseMoved(self, evt): #Here evt means event
        global hLine
        global vLine
        global data1
        global data2
        global dataPosX
        pos = evt[0] # Using proxy signal we get the original arguments in a tuple

        if self.plotwidget.sceneBoundingRect().contains(pos):
            mousePoint = self.vb.mapSceneToView(pos)
            index = int(mousePoint.x())
            if index >= 0 and index < len(self.data[0]):
                dataPosX = mousePoint.x()
                # for loop for each curve to set the Pos

                for m in range(self.num_of_curves):
                    self.curvePoints[m].setPos(float(index)/(len(self.data[m])-1))
                    T = majors[m] # Get the respective text string of the Legend
                    self.texts[m].setText("[%0.1f, %0.1f]:"%(dataPosX, self.data[m][index])+str(T))
            # Now we can set Pos of the vLine and hLine as the mousePoint
            vLine.setPos(mousePoint.x())
            hLine.setPos(mousePoint.y())
    # qt_connections function for the buttons
    def qt_connections(self):
        self.increasebutton.clicked.connect(self.on_increasebutton_clicked)
        self.decreasebutton.clicked.connect(self.on_decreasebutton_clicked)
    
    # Another function to update plot
    def moveplot(self):
        self.updateplot()
    
    # Update the data on plot
    def updateplot(self):
        global data1 
        global data2

        # Sine and Cosine plot functions
        self.data[0] = self.amplitude*np.sin(np.linspace(0, 2*np.pi, 201) + self.t) # A single sine wave from 0 to 2 pi consisting of 201 points
        self.data[1] = self.amplitude*np.cos(np.linspace(0, 2*np.pi, 201) + self.t) # A single cosine wave from 0 to 2 pi consisting of 201 points
        for j in range(self.num_of_curves):
            pen = pg.mkPen(color = Colors_Set[j], width =5)
            self.plotcurves[j].setData(self.data[j], pen = pen, clickable = True)
            # pen is for the color and plot curves get the data

    # Button functions to increment and decrement the amplitude 
    def on_increasebutton_clicked(self):
        self.amplitude += 1 
        self.updateplot()

    def on_decreasebutton_clicked(self):
        self.amplitude -= 1 
        self.updateplot()

# Main function to run the app
def main ():
    import sys
    app = QtGui.QApplication(sys.argv)
    app.setApplicationName("Sinewave")
    ex = pyshine_plot()
    if(sys.flags.interactive != 1) or not hasattr(QtCore, "PYQT_VERSION"):
        sys.exit(app.exec_())
if __name__ == "__main__":
    main()




        



