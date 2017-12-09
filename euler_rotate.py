"""
    usage 
    > python sat_antenna_rotate.py 0 20 45
    paramter: roll, pitch, yaw of antenna
    
"""
import argparse
import matplotlib as mpl
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import math
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.pyplot as plt
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
#from PyQt4.QtGui import *
from PyQt5 import QtCore
#from PyQt4 import QtCore
from PyQt5.QtCore import QObject, pyqtSignal
#from PyQt4.QtCore import QObject, pyqtSignal
import sys
import time
import transforms3d as td

# Antenna euler angle 'rzyx'
sx = 0
sy = -45
sz = 195

       
        
class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()
        self.sphere = EulerSphere(self.fig)
        self.yaw_float = 0.0
        self.pitch_float = 0.0
        self.roll_float = 0.0

    def setupUI(self):
        self.setGeometry(600, 50, 1200, 1000)
        self.setWindowTitle("Accumulative Euler Rotate")
        
        # Yaw Roll, Pitch
        xyzLabel =   QLabel(" xyz:  ", self)
        yawLabel =   QLabel(" Yaw:  ", self)
        pitchLabel = QLabel(" Pitch:", self)
        rollLabel =  QLabel(" Roll: ", self)
        self.combo_xyz = QComboBox(self)
        methods = ['rxyz', 'rxzy', 'ryxz', 'ryzx', 'rzxy', 'rzyx', \
                   'sxyz', 'sxzy', 'syxz', 'syzx', 'szxy', 'szyx']  
        for m in methods:
            self.combo_xyz.addItem(m)
        self.combo_xyz.setCurrentIndex(5)
        self.combo_xyz.activated.connect(self.OnSpinChanged)
        self.spin_yaw = QDoubleSpinBox(self)
        self.spin_yaw.setMinimum(-180)
        self.spin_yaw.setMaximum(180)
        self.spin_yaw.valueChanged.connect(self.OnSpinChanged)
        self.spin_pitch = QDoubleSpinBox(self)
        self.spin_pitch.setMinimum(-180)
        self.spin_pitch.setMaximum(180)
        self.spin_pitch.valueChanged.connect(self.OnSpinChanged)
        self.spin_roll = QDoubleSpinBox(self)
        self.spin_roll.setMinimum(-180)
        self.spin_roll.setMaximum(180)
        self.spin_roll.valueChanged.connect(self.OnSpinChanged)
        self.scroll_yaw = QScrollBar(1)
        self.scroll_yaw.setMinimum(-180)
        self.scroll_yaw.setMaximum(180)
        self.scroll_yaw.valueChanged.connect(self.OnScrollChanged)
        self.scroll_pitch = QScrollBar(1)
        self.scroll_pitch.setMinimum(-180)
        self.scroll_pitch.setMaximum(180)
        self.scroll_pitch.valueChanged.connect(self.OnScrollChanged)
        self.scroll_roll = QScrollBar(1)
        self.scroll_roll.setMinimum(-180)
        self.scroll_roll.setMaximum(180)
        self.scroll_roll.valueChanged.connect(self.OnScrollChanged)
        self.btn_reset=QPushButton('Reset')
        self.btn_reset.clicked.connect(self.OnResetCliked)
        self.btn_rotate=QPushButton('Rotate')
        self.btn_rotate.clicked.connect(self.OnRotateCliked)

        # Figure
        self.fig = plt.Figure()
        self.canvas = FigureCanvas(self.fig)

        leftLayout = QVBoxLayout()
        leftLayout.addWidget(self.canvas)

        # Right Layout
        rightLayout = QVBoxLayout()
        rYPRLayout = QGridLayout()
        rYPRLayout.addWidget(yawLabel, 0,0)
        rYPRLayout.addWidget(self.spin_yaw, 0,1)
        rYPRLayout.addWidget(self.scroll_yaw, 1,0,1,2)
        rYPRLayout.addWidget(pitchLabel, 2,0,)
        rYPRLayout.addWidget(self.spin_pitch, 2,1)
        rYPRLayout.addWidget(self.scroll_pitch, 3,0,1,2)
        rYPRLayout.addWidget(rollLabel, 4,0)
        rYPRLayout.addWidget(self.spin_roll, 4,1)
        rYPRLayout.addWidget(self.scroll_roll, 5,0,1,2)
        rYPRLayout.addWidget(xyzLabel, 6,0)
        rYPRLayout.addWidget(self.combo_xyz, 6,1)        
        
        rightLayout.addLayout(rYPRLayout)
        rightLayout.addWidget(self.btn_reset)
        rightLayout.addWidget(self.btn_rotate)
        rightLayout.addStretch(1)

        layout = QHBoxLayout()
        layout.addLayout(leftLayout)
        layout.addLayout(rightLayout)
        layout.setStretchFactor(leftLayout, 1)
        layout.setStretchFactor(rightLayout, 0)

        self.setLayout(layout)
        
    def OnScrollChanged(self):
        # get scrollbar value
        yaw = self.scroll_yaw.value()
        pitch = self.scroll_pitch.value()
        roll = self.scroll_roll.value()
        #change inteter to float
        yaw = yaw + self.yaw_float
        pitch = pitch + self.roll_float
        roll = roll + self.roll_float
        # set scroll bar
        self.spin_yaw.setValue(yaw)
        self.spin_pitch.setValue(pitch)
        self.spin_roll.setValue(roll)
        self.sphere.rotate([roll, pitch, yaw], method=self.combo_xyz.currentText())     
        self.canvas.draw()
        
    def OnSpinChanged(self):
        # get spin value
        yaw = self.spin_yaw.value()
        pitch = self.spin_pitch.value()
        roll = self.spin_roll.value()
        self.yaw_float = yaw - int(yaw)
        self.pitch_float = pitch - int(pitch)
        self.rollw_float = roll - int(roll)
        #set scrollber
        self.scroll_yaw.setValue(int(yaw))
        self.scroll_pitch.setValue(int(pitch))
        self.scroll_roll.setValue(int(roll))
        self.sphere.rotate([roll, pitch, yaw], method=self.combo_xyz.currentText())  
        self.canvas.draw()

    def Reset(self):
        self.spin_yaw.setValue(0)
        self.spin_pitch.setValue(0)
        self.spin_roll.setValue(0)
        self.scroll_yaw.setValue(0)
        self.scroll_pitch.setValue(0)
        self.scroll_roll.setValue(0)
        self.yaw_float = 0.0
        self.pitch_float = 0.0
        self.roll_float = 0.0   

    def OnResetCliked(self):
        self.Reset()
        self.sphere.rotate([0, 0, 0], method=self.combo_xyz.currentText())  
    
    def OnRotateCliked(self):
        # rotate poligon antenna
        yaw = self.spin_yaw.value()
        pitch = self.spin_pitch.value()
        roll = self.spin_roll.value()
        self.sphere.rotateSave([roll, pitch, yaw], method=self.combo_xyz.currentText())  
        self.canvas.draw()
        self.Reset()
       
    def closeEvent(self, event):
        print ("Closing GUI")
        sys.exit()

class PolyData():
    def __init__(self):
        super().__init__()
        self.polies = {}
        self.count = 0
        x = [-0.7,0.7,1,0.7,-0.7]
        y = [-0.7,-0.7,0,0.7,0.7]
        z = [0,0,0,0,0]
        lb, lu, ru, ze, rb = (zip(x, y,z))
        vert = [lb, lu, ru, ze, rb]
        p = [1,0,0]
        rot = [[1,0,0],[0,1,0],[0,0,1]]
        poly = {'vert':vert, 'p':p, 'rot':rot}
        self.polies[self.count] = poly
        self.vert = vert
        self.p = p
        self.rot = rot
        self.vert_org = vert
        self.p_org = [1,0,0]

    def update(self, vert, p, rot):
        self.vert = vert
        self.p = p
        self.rot = rot
        
    def add(self):
        poly = {'vert':self.vert, 'p':self.p, 'rot':self.rot}
        self.count += 1
        self.polies[self.count] = poly

    def get(self):
        poly = self.polies[self.count]
        return poly['vert'], poly['p'], poly['rot']
        
        
class EulerSphere():
    def __init__(self, fig, parent=None):
        self.fig = fig   
        self.ax = self.fig.gca(projection='3d', aspect='equal')    
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        self.colors = "gbrcmy"
        self.xyz = [1,1,1]
        self.collection = None
        self.quiver = None
        self.method = 'rzyx'
        self.poly = PolyData()
        self.draw_bg()

    def draw_bg(self):    
        ###### draw sphere
        u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
        x = np.cos(u)*np.sin(v)
        y = np.sin(u)*np.sin(v)
        z = np.cos(v)
        self.ax.plot_wireframe(x, y, z, color='#d8dcd6')  ##fdfdfe:pale gray
     
        ###### draw circle
        elev = 0.0
        rot = 90.0 / 180 * np.pi
        #calculate vectors for "vertical" circle
        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, np.pi, 100)
        a = np.array([-np.sin(elev / 180 * np.pi), 0, np.cos(elev / 180 * np.pi)])
        b = np.array([0, 1, 0])
        b = b * np.cos(rot) + np.cross(a, b) * np.sin(rot) + a * np.dot(a, b) * (1 - np.cos(rot))
        horiz_front = np.linspace(0, np.pi, 100)
        vert_front = np.linspace(np.pi / 2, 3 * np.pi / 2, 100)
        self.ax.plot(np.sin(horiz_front),np.cos(horiz_front),0,color='k')
        self.ax.plot(a[0] * np.sin(u) + b[0] * np.cos(u), b[1] * np.cos(u), a[2] * np.sin(u) + b[2] * np.cos(u),color='k', linestyle = 'dashed')
        self.ax.plot(a[0] * np.sin(vert_front) + b[0] * np.cos(vert_front), b[1] * np.cos(vert_front), a[2] * np.sin(vert_front) + b[2] * np.cos(vert_front),color='k')
        self.ax.view_init(elev = elev, azim = 0)
        self.ax.plot(np.sin(u),np.cos(u),0,color='k', linestyle = 'dashed')

        # draw the arrow of satellite
        rots = td.euler.euler2mat(np.radians(sz),np.radians(sy),np.radians(sx), 'rzyx')
        ps = np.dot(rots, [1,0,0])
        self.ax.quiver(0,0,0,ps[0],ps[1],ps[2],length=1.0, color='k')
        self.ax.scatter([ps[0]], [ps[1]], [ps[2]], color="r", s=100)
        self.ax.text(ps[0], ps[1], ps[2], "  satellite", ps, color='red')
        
        # draw basement        
        vert, p, rot = self.poly.get()
        collection = Poly3DCollection([vert], linewidths=1, alpha=0.5)
        collection.set_facecolor('g')
        self.ax.add_collection3d(collection)
        self.ax.quiver(0,0,0,p[0],p[1],p[2],length=1.0, color='g')   

    def calPoly(self, xyz, method='rzyx'): 
        roll    = xyz[0]
        pitch   = xyz[1]
        yaw     = xyz[2]  
        vert, p, rot = self.poly.get()
        
        if method[1] == 'x':
            first = roll
        elif method[1] == 'y':
            first = pitch
        else:
            first = yaw
            
        if method[2] == 'x':
            second = roll
        elif method[2] == 'y':
            second = pitch
        else:
            second = yaw

        if method[3] == 'x':
            third = roll
        elif method[3] == 'y':
            third = pitch
        else:
            third = yaw
        
        rot1 = td.euler.euler2mat(np.radians(first),np.radians(second),np.radians(third), method)
        rot_r = np.dot(rot, rot1)
        vert_r = []
        for v in self.poly.vert_org:
            a = np.dot(rot_r, v)
            vert_r.append(a)
        p_r = np.dot(rot_r, self.poly.p_org)        
        return vert_r, p_r, rot_r
        
    def rotate(self, xyz, method='rzyx'):
        if self.xyz == xyz and self.method == method:
            return
        else:
           self.xyz = xyz
           self.method = method
        # remove previouse rotate  
        vert_r, p_r, rot_r = self.calPoly(xyz, method)
        if self.collection:
            self.ax.collections.remove(self.collection)
        if self.quiver:
            self.quiver.remove()
        color = self.colors[(self.poly.count+1)%5]
        self.collection = Poly3DCollection([vert_r], linewidths=1, alpha=0.5)
        self.collection.set_facecolor(color)     
        self.ax.add_collection3d(self.collection)
        self.quiver = self.ax.quiver(0,0,0,p_r[0],p_r[1],p_r[2],length=1.0, color=color)
        self.poly.update(vert_r, p_r, rot_r)
        
    def rotateSave(self, xyz, method='rzyx', color=None):
        self.xyz = xyz
        self.method = method
        self.collection = None
        self.quiver = None
        vert_r, p_r, rot_r = self.calPoly(xyz, method)        
        self.poly.update(vert_r, p_r, rot_r)
        self.poly.add()

    def asSpherical(self, xyz):
        #takes list xyz (single coord)
        x       = xyz[0]
        y       = xyz[1]
        z       = xyz[2]
        r       =  math.sqrt(x*x + y*y + z*z)
        theta   =  math.acos(z/r)*180/ np.pi #to degrees
        phi     =  math.atan2(y,x)*180/ np.pi    
        return [r,theta,phi]
        

if __name__ == '__main__':
    # create parser
    parser = argparse.ArgumentParser(description="Accumulative Euler Rotate")
    # add expected arguments
    # parse args
    args = parser.parse_args()    
    #main(args.xyz[0], args.xyz[1], args.xyz[2])
    app = QApplication(sys.argv)
    w = MyWidget()
    w.show()    
    sys.exit(app.exec_())