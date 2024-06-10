# ------------------------------------------------------
# -------------------- mplwidget.py --------------------
# ------------------------------------------------------
from PyQt5.QtWidgets import *
from PyQt5 import QtCore

import matplotlib as mpl
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt



# 한글 구현
font_ko = {
    'family': 'New Gulim'
}
font_en = {
    'family': 'Arial'
}

class MplWidget(QWidget):
    
    def __init__(self, parent = None):

        QWidget.__init__(self, parent)

        self.fig = plt.Figure()
        self.canvas = FigureCanvas( self.fig )

        #THESE TWO LINES WERE ADDED
        self.canvas.setFocusPolicy( QtCore.Qt.ClickFocus )
        self.canvas.setFocus()

        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)
        self.setLayout(vertical_layout)

        # 한글 구현
        try:
            mpl.rc( 'font', **font_ko )
        except:
            mpl.rc( 'font', **font_en )