import sys
import matplotlib
matplotlib.use("Qt5Agg")
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from os import listdir, remove
from os.path import isfile, join, dirname
# pip install pyqt5
from PyQt5.QtWidgets import QApplication, QLineEdit, QSizePolicy, QComboBox, QWidget, QMainWindow, QMenu, QVBoxLayout, QSpinBox, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt
from scipy.interpolate import CubicSpline, interp1d
from scipy.stats import linregress
import glob


hPlanck = 6.62607015e-34 / (2*np.pi) # постоянная планка
n = 7e15 # концентрация 
e = 1.6e-19 # заряд электрона

def tempChecker(name):
    sym = 1
    temp = ''
    while name[-sym] != 'T':
        if name[-sym] != ',':
            temp +=name[-sym]
        else:
            temp+='.'
        sym+=1
    return float(temp[::-1])

class MyMplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=10, height=7, dpi=200):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        self.axes.plot()
        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

class MyStaticMplCanvas(MyMplCanvas):
    """Simple canvas with a sine plot."""
    def update_figure(self, files, path):
        self.axes.cla()
        for name in files:
            f = open(path+'/'+name, 'r')
            data = np.loadtxt(f, delimiter = '\t', usecols=(0,1))
            B = data[:, 0]
            V = data[:, 1]
            start = 0 # выделение нужной части данных
            end = -1
            B = B[start:end]
            V = V[start:end]
            #V = V - V[np.argmin(np.abs(B))]
            B_filtered = B#[B > 0]
            V_filtered = V#[B > 0]
            dc = (1e6)*2*np.sqrt(2*np.pi*n)*hPlanck/(e*B_filtered)
            self.axes.plot(dc, V_filtered)#, '.')
        self.axes.set_xlim(-10, 10)
        self.draw()
    
    def suppressCurve(self, files, path, curveName, temps, Lee1):
        self.update_figure(files, path)
        f = open(path + '/' + curveName, 'r')
        data = np.loadtxt(f, delimiter = '\t', usecols=(0,1))
        B = data[:, 0]
        V = data[:, 1]
        B_filtered = B[B > 0]
        V_filtered = V[B > 0]
        dc = (1e6)*2*np.sqrt(2*np.pi*n)*hPlanck/(e*B_filtered)
        for t in temps:
            print(Lee1/t**2)
            suppressedV = V_filtered * np.exp(-np.pi*np.abs(dc) * (t**2 - tempChecker(curveName)**2) / (2*Lee1))
            self.axes.plot(dc, suppressedV, 'b', linestyle='dashed')
        self.draw()


class linearGraphCanvas(FigureCanvas):
    def __init__(self, parent=None, width=10, height=7, dpi=200):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        self.axes.plot()
        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

class staticLinearGraphCanvas(linearGraphCanvas):
    """Simple canvas with a sine plot."""
    def update_figure(self, V, temps):
        self.axes.cla()
        tempsNp = np.array(temps)
        x = tempsNp**2
        y = np.log(V)
        x = np.delete(x, len(x) - 1)
        y = np.delete(y, len(y) - 1)
        if float('-inf') in y:
            index = np.where(y == float('-inf'))[0][0]
            x = np.delete(x, index)
            y = np.delete(y, index)
        self.axes.plot(x, y, linestyle='none', marker='o')
        resOfLingress = linregress(x, y)
        linearizedX = np.linspace(min(x), max(x), len(x))
        linearizedY = resOfLingress.intercept + resOfLingress.slope *linearizedX
        self.axes.plot(linearizedX, linearizedY, color = 'red')
        print(np.sqrt(-1/resOfLingress.slope))
        self.draw()
        
class windowForLinear(QWidget):
     def __init__(self):
         super(windowForLinear, self).__init__()
         self.resize(600, 600)



class ApplicationWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setStyleSheet('font-size: 35px;')
        self.file_menu = QMenu('&File', self)
        self.file_menu.addAction('&Open data from...', self.openData)
        self.file_menu.addAction('&Quit', self.close, Qt.CTRL + Qt.Key_Q)

        self.menuBar().addMenu(self.file_menu)
        self.files = []
        self.path = ''
        self.main_widget = QWidget()
        layout = QVBoxLayout(self.main_widget)

        self.headLayout = QHBoxLayout(self.main_widget)
        self.filesManipulationCB = QComboBox(self.main_widget)
        self.filesManipulationCB.addItems(['Вычесть одну из кривых','Вычесть константу из одной из кривых', 'Найти максимумы в диапазоне', 'Подавление кривой'])
        self.curveMinusCB = QComboBox(self.main_widget)
        self.curveMinusCB.addItems(self.files)
        self.curveMinusBtn = QPushButton(self.main_widget)

        self.curveMinusCB.setParent(None)
        self.curveMinusBtn.setParent(None)

        self.constMinusCB = QComboBox(self.main_widget)
        self.constMinusCB.addItems(self.files)
        self.constMinusLine = QLineEdit(self.main_widget)
        self.constMinusBtn = QPushButton(self.main_widget)

        self.constMinusCB.setParent(None)
        self.constMinusLine.setParent(None)
        self.constMinusBtn.setParent(None)

        self.maxSearchStart = QLineEdit(self.main_widget)
        self.maxSearchEnd = QLineEdit(self.main_widget)
        self.maxSearchBtn = QPushButton(self.main_widget)

        self.maxSearchStart.setParent(None)
        self.maxSearchEnd.setParent(None)
        self.maxSearchBtn.setParent(None)

        self.suppressionModelCB = QComboBox(self.main_widget)
        self.suppressionModelCB.addItems(self.files)
        self.suppressionModelLine = QLineEdit(self.main_widget)
        self.suppressionModelBtn = QPushButton(self.main_widget)

        self.suppressionModelCB.setParent(None)
        self.suppressionModelBtn.setParent(None)
        self.suppressionModelLine.setParent(None)

        self.headLayout.addWidget(self.filesManipulationCB)

        sc1 = MyStaticMplCanvas(self.main_widget)

        layout.addLayout(self.headLayout)
        self.filesManipulationCB.activated.connect(self.updateHeadPanel)
        self.curveMinusBtn.clicked.connect(self.curveMinus)
        self.constMinusBtn.clicked.connect(self.constMinus)
        self.maxSearchBtn.clicked.connect(self.maxSearch)
        self.suppressionModelBtn.clicked.connect(lambda: sc1.suppressCurve(self.files, self.path, str(self.suppressionModelCB.currentText()), self.temps, float(self.suppressionModelLine.text())))

        self.temps = []

        buttonsLayout = QHBoxLayout(self.main_widget)

        buttonTemps = QPushButton(self.main_widget)
        buttonTemps.setText("Change temperatures")
        buttonTemps.clicked.connect(lambda: self.table.show())

        buttonPlot = QPushButton(self.main_widget)
        buttonPlot.setText("Plot")
        buttonPlot.clicked.connect(lambda: sc1.update_figure(self.files, self.path))

        layout.addWidget(sc1)

        self.navi_toolbar = NavigationToolbar(sc1, self)
        
        layout.addWidget(self.navi_toolbar)
        buttonsLayout.addWidget(buttonTemps)
        buttonsLayout.addWidget(buttonPlot)
        layout.addLayout(buttonsLayout)        

        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

    def updateHeadPanel(self):
        print(self.headLayout.count())
        while self.headLayout.count()!=1:
            self.headLayout.itemAt(1).widget().setParent(None)
        if str(self.filesManipulationCB.currentText()) == 'Вычесть одну из кривых':
            self.curveMinusCB.addItems(self.files)
            self.headLayout.addWidget(self.curveMinusCB)
            self.headLayout.addWidget(self.curveMinusBtn)
        elif str(self.filesManipulationCB.currentText()) == 'Вычесть константу из одной из кривых':
            self.constMinusCB.addItems(self.files)
            self.headLayout.addWidget(self.constMinusCB)
            self.headLayout.addWidget(self.constMinusLine)
            self.headLayout.addWidget(self.constMinusBtn)
        elif str(self.filesManipulationCB.currentText()) == 'Найти максимумы в диапазоне':
            self.headLayout.addWidget(self.maxSearchStart)
            self.headLayout.addWidget(self.maxSearchEnd)
            self.headLayout.addWidget(self.maxSearchBtn)
        elif str(self.filesManipulationCB.currentText()) == 'Подавление кривой':
            self.suppressionModelCB.addItems(self.files)
            self.headLayout.addWidget(self.suppressionModelCB)
            self.headLayout.addWidget(self.suppressionModelLine)
            self.headLayout.addWidget(self.suppressionModelBtn)

    def getSpline(self, data):
        dataSorted = data[data[:,0].argsort()] #для функции CubicSpline необходим сортированный X (в исходных данных это не всегда так)
        B = dataSorted[:, 0]
        V = dataSorted[:, 1]
        V = V[np.unique(B, axis=0, return_index=True)[1]]
        B = np.unique(B, axis=0)
        return CubicSpline(B, V)
    
    def curveMinus(self):
        curveFile = open(self.path+'/'+str(self.curveMinusCB.currentText()), 'r')
        data = np.loadtxt(curveFile, delimiter = '\t', usecols=(0,1))
        spl = self.getSpline(data)
        for name in self.files:
            openedFile = open(self.path+'/'+name, 'r')
            data = np.loadtxt(openedFile, delimiter = '\t', usecols=(0,1))
            data[:, 1] = data[:, 1] - spl(data[:, 0])
            np.savetxt(self.path+'/'+name, data, delimiter='\t')

    def constMinus(self):
        curveFile = open(self.path+'/'+str(self.constMinusCB.currentText()), 'r')
        data = np.loadtxt(curveFile, delimiter = '\t', usecols=(0,1))
        data[:, 1] = data[:, 1] - float(self.constMinusLine.text())
        np.savetxt(self.path+'/'+str(self.constMinusCB.currentText()), data, delimiter='\t')

    def maxSearch(self):
        maxes = []
        for name in self.files:
            f = open(self.path+'/'+name, 'r')
            data = np.loadtxt(f, delimiter = '\t', usecols=(0,1))
            B = data[:, 0]
            V = data[:, 1]
            B_filtered = B[B > 0]
            V_filtered = V[B > 0]
            dc = (1e6)*2*np.sqrt(2*np.pi*n)*hPlanck/(e*B_filtered)
            start = float(self.maxSearchStart.text())
            end = float(self.maxSearchEnd.text())
            maxes.append(max(V_filtered[[i for i in range(len(dc)) if dc[i] >=start and dc[i]<=end]]))
            print(max(V_filtered[[i for i in range(len(dc)) if dc[i] >=start and dc[i]<=end]]))
        
        self.sub_window = windowForLinear()
        linGrSc = staticLinearGraphCanvas(self.sub_window)
        layoutForSubWindow = QVBoxLayout(self.sub_window)
        layoutForSubWindow.addWidget(linGrSc)
        linGrSc.update_figure(maxes,self.temps)
        self.sub_window.show()
        print('hi')

    def openData(self):
        path = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.files = [f for f in listdir(path) if isfile(join(path, f))] 
        response = QMessageBox.question(self,'', "Разделителем является точка?", QMessageBox.Yes | QMessageBox.No)
        self.path = dirname(__file__) + '\\savedData'
        filesToDelete = glob.glob(self.path + '\\*')
        for f in filesToDelete: # очищаем папку
            remove(f)
        for name in self.files:
            openedFile = open(path+'/'+name, 'r')
            filedata = openedFile.read()
            if response == QMessageBox.No:
                filedata = filedata.replace(',', '.')
            with open(self.path+'\\'+name, 'w+') as file:
                file.write(filedata)
        for name in self.files:
            self.temps.append(tempChecker(name))
        
        print(self.temps)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = ApplicationWindow()
    win.setWindowTitle("PyQt5 Matplotlib App Demo")
    win.show()
    sys.exit(app.exec_())