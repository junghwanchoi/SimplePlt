# ------------------------------------------------------
# ---------------------- main.py -----------------------
# ------------------------------------------------------
from PyQt5.QtWidgets import*
from PyQt5.uic import loadUi

from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)

import numpy as np
import random
import pandas as pd

SPLT_dfData = pd.DataFrame()

class MatplotlibWidget(QMainWindow):
    
    def __init__(self):
        
        QMainWindow.__init__(self)

        loadUi("qt_designer.ui",self)

        self.setWindowTitle("PyQt5 & Matplotlib Example GUI")

        self.pushButton_OpenFile.clicked.connect(self.OnBtnClick_OpenFile)
        self.pushButton_Down.clicked.connect(self.update_graph)

        self.addToolBar(NavigationToolbar(self.MplWidget.canvas, self))

    def OnBtnClick_OpenFile(self):
        lstFileName = QFileDialog.getOpenFileName( self, "Open file", "./", "CSV (*.csv)")

        if lstFileName[0]:
            try:
                global SPLT_dfData
                SPLT_dfData = pd.read_csv( lstFileName[0], encoding="utf-8" )
                lstColumns = SPLT_dfData.columns
                self.listView_Columns.clear()
                for i, strColumn in enumerate(lstColumns) :
                    self.listView_Columns.addItem( strColumn )

            except:
                print( f"error at opening \"{lstFileName[0]}\"")

    def update_graph(self):

        fs = 500
        f = random.randint(1, 100)
        ts = 1/fs
        length_of_signal = 100
        t = np.linspace(0,1,length_of_signal)
        
        cosinus_signal = np.cos(2*np.pi*f*t)
        sinus_signal = np.sin(2*np.pi*f*t)

        self.MplWidget.canvas.axes.clear()
        self.MplWidget.canvas.axes.plot(t, cosinus_signal)
        self.MplWidget.canvas.axes.plot(t, sinus_signal)
        self.MplWidget.canvas.axes.legend(('cosinus', 'sinus'),loc='upper right')
        self.MplWidget.canvas.axes.set_title('Cosinus - Sinus Signal')
        self.MplWidget.canvas.draw()
        

app = QApplication([])
window = MatplotlibWidget()
window.show()
app.exec_()