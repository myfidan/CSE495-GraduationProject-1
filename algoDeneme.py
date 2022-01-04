
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget, QApplication
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys, random
import random
import math
import time


globalFileName = ""

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.points = []
        self.hexagons = []
        self.marked_hexagons = []
        self.NUMBER_OF_POINTS = 200
        self.X_MIN_AREA = 0
        self.Y_MIN_AREA = 0
        self.X_MAX_AREA = 800
        self.Y_MAX_AREA = 800
        self.r = 10
        self.printPoint = False
        self.printDisk = False
        for i in range(0,self.NUMBER_OF_POINTS):
            x = random.randint(self.X_MIN_AREA,self.X_MAX_AREA)
            y = random.randint(self.Y_MIN_AREA,self.Y_MAX_AREA)
            self.points.append([x,y])
        self.initUI()
        

    def initUI(self):
        self.setGeometry(300, 300, 1200, 800)
        self.setWindowTitle('MGDC Solver')
        self.drawMenuPanels()
        self.show()

        

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        
        self.drawPlaneRect(qp)
        if(self.printPoint):
            self.drawPoints(qp)
        if(self.printDisk):
            self.drawCircles(qp)
        self.drawMenuPlane(qp)

        qp.setPen(QPen(Qt.black))
        qp.setFont(QFont('Times', 12))
        
        qp.drawText(QPoint(820,90), "Points:")
        qp.drawText(QPoint(820,155), "Plane Size:")
        qp.drawLine(800,250,1200,250)
        qp.drawText(QPoint(820,300), "Radius Value:")
        qp.drawText(QPoint(820,360), "Algorithm:")
        qp.drawLine(800,450,1200,450)
        qp.drawText(QPoint(820,580), "Log Messages:")
        
        qp.end()
        

    def drawPoints(self, qp):
        
        qp.setPen(Qt.green)
        
        size = self.size()

        if size.height() <= 1 or size.height() <= 1:
            return
        
        for i in self.points:

            qp.drawPoint(i[0], i[1])
           
    def drawCircles(self,qp):
        #Check this
        self.printDisk = False
        ###
        self.Regular_Tessellation()
        self.Minimum_Geometric_Disk_Cover()
        qp.setPen(QPen(Qt.red,  0.5, Qt.SolidLine))
        
        
        size = self.size()
 
        if size.height() <= 1 or size.height() <= 1:
            return

        for i in self.marked_hexagons:
            cent = QPointF(i[0],i[1]) 
            qp.drawEllipse(cent, self.r, self.r)
        
        
    def drawPlaneRect(self,qp):
        brush = QBrush(Qt.SolidPattern)
        qp.setBrush(brush)
        qp.drawRect(0, 0, 800, 800)
        brush = QBrush()
        qp.setBrush(brush)

    def drawMenuPlane(self,qp):
        brush = QBrush(Qt.white)
        qp.setBrush(brush)
        qp.drawRect(800, 0, 400, 800)
        brush = QBrush(Qt.SolidPattern)
        qp.setBrush(brush)

    def drawMenuPanels(self):

        self.textbox = QtWidgets.QLineEdit(self)
        self.textbox.move(950, 65)
        self.textbox.resize(200,40)

        self.textbox2 = QtWidgets.QLineEdit(self)
        self.textbox2.move(950, 130)
        self.textbox2.resize(200,40)

        self.textbox3 = QtWidgets.QLineEdit(self)
        self.textbox3.move(950, 275)
        self.textbox3.resize(200,40)
        

        self.button = QtWidgets.QPushButton('Create Points', self)
        self.button.resize(200,40)
        self.button.move(950,195)
        self.button.setToolTip('This is an example button')
        self.button.clicked.connect(self.on_click)

        self.combo = QtWidgets.QComboBox(self)
        self.combo.addItem("Hexagon I")
        self.combo.addItem("Hexagon II")
        self.combo.addItem("Greedy Max")
        self.combo.resize(200,25)
        self.combo.move(950,340)

        self.button2 = QtWidgets.QPushButton('Find Disks', self)
        self.button2.resize(200,40)
        self.button2.move(950,390)
        self.button2.setToolTip('This is an example button')
        self.button2.clicked.connect(self.on_click_find_disks)

        self.button3 = QtWidgets.QPushButton('Reset', self)
        self.button3.resize(150,40)
        self.button3.move(830,475)
        self.button3.setToolTip('This is an example button')
        self.button3.clicked.connect(self.on_click_reset)

        self.button4 = QtWidgets.QPushButton('Read From File', self)
        self.button4.resize(150,40)
        self.button4.move(1020,475)
        self.button4.setToolTip('This is an example button')
        self.button4.clicked.connect(self.on_click_read_file)

        self.textEdit = QtWidgets.QTextEdit(self)
        self.textEdit.document().setPlainText("Log messages")
        self.textEdit.setReadOnly(True)
        self.textEdit.resize(400,200)
        self.textEdit.move(800,600)

    @pyqtSlot()
    def on_click(self):
        print(self.textbox.text()) 
        print(str(self.combo.currentText()))
        self.textEdit.document().setPlainText("aaaa")
        self.points = []
        self.hexagons = []
        self.marked_hexagons = []
        self.NUMBER_OF_POINTS = int(self.textbox.text())
        self.X_MIN_AREA = 0
        self.Y_MIN_AREA = 0
        self.X_MAX_AREA = 800
        self.Y_MAX_AREA = 800
        self.planeSizeText = int(self.textbox2.text())
        self.r = 10
        print(self.planeSizeText)
        for i in range(0,self.NUMBER_OF_POINTS):
            x = random.randint(self.X_MIN_AREA,self.X_MAX_AREA)
            y = random.randint(self.Y_MIN_AREA,self.Y_MAX_AREA)
            self.points.append([x,y])     
        self.printPoint = True
        self.printDisk = False
        self.update() 



    def on_click_find_disks(self):
        self.r = int(self.textbox3.text())*(800/self.planeSizeText)
        self.textEdit.document().setPlainText("<<Disks Created>>")
        self.printDisk = True
        self.update() 

    def on_click_reset(self):
        self.printDisk = False
        self.printPoint = False;
        self.textEdit.document().setPlainText("<<Reset Button Clicked>>")
        self.update()

    def on_click_read_file(self):
        self.textEdit.document().setPlainText("<<Read From File Button Clicked>>")
        self.exPopup = PopUp("readFile")
        self.exPopup.setGeometry(500,500,350,100)
        self.exPopup.setAttribute(Qt.WA_DeleteOnClose)
        self.exPopup.show()

        loop = QEventLoop()
        self.exPopup.destroyed.connect(loop.quit)
        loop.exec()

        ## read file points and plane
        self.read_file_points()

        self.update() 

    def read_file_points(self):
        global globalFileName

        file = open(globalFileName, 'r')
        Lines = file.readlines()
        

        self.points = []
        self.hexagons = []
        self.marked_hexagons = []
        self.NUMBER_OF_POINTS = 200

        count = 0
        for line in Lines:
            if(count == 0):
                self.planeSizeText = int(line)
                count += 1
            else:
                
                arr = line.split(',')
                xPart = int(arr[0])
                yPart = int(arr[1])
                self.points.append([xPart,yPart])
        self.NUMBER_OF_POINTS = len(self.points)
        self.printPoint = True
        self.update()        

### Reguler tesselation Algos
    
    def Regular_Tessellation(self):
        hex_x_coord = self.r/2
        hex_y_coord = self.r/2*math.sqrt(3)
        
    
        hexagon_x_index = 0
        ## X cord
        while True:

            if(hexagon_x_index % 2 == 0):
                hex_y_coord = self.r/2*math.sqrt(3)
            else:
                hex_y_coord = 0

            self.hexagons.append([])
            ## Y cord
            while True:
                self.hexagons[hexagon_x_index].append([hex_x_coord,hex_y_coord])
                if(hex_y_coord >= self.Y_MAX_AREA):
                    break
                hex_y_coord += self.r*math.sqrt(3)

            hexagon_x_index += 1
            if(hex_x_coord + self.r/2 > self.X_MAX_AREA):
                break
            hex_x_coord += 3*self.r/2

    def Minimum_Geometric_Disk_Cover(self):
        
        for i in self.points:
            x_rank = int(i[0]/(self.r*3/2))
            y_rank = 0
            if(x_rank % 2 == 0):
                y_rank = int(i[1]/(self.r*math.sqrt(3)))
            else:
                y_rank = int((i[1]+(math.sqrt(3)/2*self.r))/(self.r*math.sqrt(3)))
            
            #Find the hexagon containing 𝑝 by comparing the distances from 𝑝 to the centers of hexagons with indices
            #(𝑥 rank, 𝑦 rank), (𝑥 rank + 1, 𝑦 rank), and [(𝑥 rank + 1, 𝑦 rank + 1) if 𝑥 rank is even or (𝑥 rank + 1, 𝑦 rank − 1)
            #if 𝑥 rank is odd]. Ties are broken in favor of the marked hexagon, otherwise broken arbitrary
            self.Find_Hexagon(i,x_rank,y_rank)

    def Find_Hexagon(self,p,x_rank,y_rank):
        
        p_x_coord = p[0]
        p_y_coord = p[1]

        #check (x rank, y rank)
        hex = self.hexagons[x_rank][y_rank]
        hex_x = hex[0]
        hex_y = hex[1]
        result = math.sqrt(((p_x_coord-hex_x)**2) + ((p_y_coord-hex_y)**2))
        if(result <= self.r):
            if self.hexagons[x_rank][y_rank] in self.marked_hexagons:
                return
            else:
                self.marked_hexagons.append(self.hexagons[x_rank][y_rank])
                return

        #check (𝑥 rank + 1, 𝑦 rank)
        hex = self.hexagons[x_rank+1][y_rank]
        hex_x = hex[0]
        hex_y = hex[1]
        result = math.sqrt(((p_x_coord-hex_x)**2) + ((p_y_coord-hex_y)**2))
        if(result <= self.r):
            if self.hexagons[x_rank+1][y_rank] in self.marked_hexagons:
                return
            else:
                self.marked_hexagons.append(self.hexagons[x_rank+1][y_rank])
                return

        if(x_rank % 2 == 0):
            #check (𝑥 rank + 1, 𝑦 rank + 1)
            hex = self.hexagons[x_rank+1][y_rank+1]
            hex_x = hex[0]
            hex_y = hex[1]
            result = math.sqrt(((p_x_coord-hex_x)**2) + ((p_y_coord-hex_y)**2))
            if(result <= self.r):
                if self.hexagons[x_rank+1][y_rank+1] in self.marked_hexagons:
                    return
                else:
                    self.marked_hexagons.append(self.hexagons[x_rank+1][y_rank+1])
                    return
        else:
            #check (𝑥 rank + 1, 𝑦 rank − 1)
            hex = self.hexagons[x_rank+1][y_rank-1]
            hex_x = hex[0]
            hex_y = hex[1]
            result = math.sqrt(((p_x_coord-hex_x)**2) + ((p_y_coord-hex_y)**2))
            if(result <= self.r):
                if self.hexagons[x_rank+1][y_rank-1] in self.marked_hexagons:
                    return
                else:
                    self.marked_hexagons.append(self.hexagons[x_rank+1][y_rank-1])
                    return



class PopUp(QWidget):
    def __init__(self, name):
        super().__init__()

        self.name = name

        self.initUI()

    def initUI(self):
        self.lblName = QLabel("File Name:", self)
        self.lblName.move(30,10)
        
        self.fileBox = QtWidgets.QLineEdit(self)
        self.fileBox.move(30, 35)
        self.fileBox.resize(200,40)

        self.button = QtWidgets.QPushButton('Read File', self)
        self.button.resize(80,40)
        self.button.move(250,35)
        self.button.setToolTip('This is an example button')
        self.button.clicked.connect(self.on_click_read)

    @pyqtSlot()
    def on_click_read(self):
        global globalFileName
        globalFileName = str(self.fileBox.text())
        self.close()
        

def main():
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()