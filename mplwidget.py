# ------------------------------------------------------
# -------------------- mplwidget.py --------------------
# ------------------------------------------------------
from PyQt5.QtWidgets import *

from matplotlib.backends.backend_qt5agg import FigureCanvas

from matplotlib.figure import Figure
import matplotlib

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
        
        self.canvas = FigureCanvas(Figure())
        
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)
        
        self.canvas.axes = self.canvas.figure.add_subplot(111)
        self.canvas.axes_2 = self.canvas.axes.twinx()
        self.setLayout(vertical_layout)

        # 한글 구현
        try:
            matplotlib.rc( 'font', **font_ko )
        except:
            matplotlib.rc( 'font', **font_en )

