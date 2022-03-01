# ------------------------------------------------------
# ---------------------- main.py -----------------------
# ------------------------------------------------------
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt

from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)

import numpy as np
import random
import pandas as pd
import os

SPL_dfData = pd.DataFrame()
SPL_lstChkData = [  ] # ["  signal name  ", 0]
SPL_strFileName = ""




class MatplotlibWidget(QMainWindow):



    def __init__(self):
        
        QMainWindow.__init__(self)

        loadUi("qt_designer.ui",self)

        self.setWindowTitle("Simple Matplotlib GUI")
        
        # 툴바
        self.addToolBar(NavigationToolbar(self.MplWidget.canvas, self))
        # 버튼 signal
        self.pushButton_OpenFile.clicked.connect(self.OnBtnClick_OpenFile)
        self.pushButton_Up.clicked.connect(self.OnBtnClick_Up)
        self.pushButton_Down.clicked.connect(self.OnBtnClick_Down)
        self.pushButton_Plt.clicked.connect(self.OnBtnClick_Plt)
		# 아이콘 표시하기
        self.pushButton_OpenFile.setIcon(QIcon('iconFile.png'))
        self.pushButton_Up.setIcon(QIcon('iconUp.png'))
        self.pushButton_Down.setIcon(QIcon('iconDown.png'))
        self.pushButton_Plt.setIcon(QIcon('iconPlot.png'))


        # List Widget
        #  CSV 파일의 column 이름을 표시
        
        # TableWidget 
        global SPL_lstChkData

        # TableWidget
        self.table.setRowCount( len(SPL_lstChkData) )
        self.table.setColumnCount(4)

        self.table.setHorizontalHeaderLabels(["Name", "X", "Y1", "Y2"])

        for iRow, (dname, iChkPos) in enumerate(SPL_lstChkData):
            # "name"
            self.table.setItem(iRow, 0, QTableWidgetItem(dname))

            for i in range(3):  # X, Y1, Y2
                iCol = i + 1
                ChkBox = QCheckBox()
                self.table.setCellWidget(iRow, iCol, ChkBox)
                ChkBox.stateChanged.connect(self.__checkbox_change)  # sender() 확인용 예..

        self.table.horizontalHeaderItem(0).setToolTip("Column Name in CSV")  # header tooltip

        self.table.setColumnWidth(1, 10)
        self.table.setColumnWidth(2, 10)
        self.table.setColumnWidth(3, 10)
		


    # .csv 파일을 open 했을때 수행하는 일
    def OnBtnClick_OpenFile(self):

        global SPL_strFileName

        lstFileName = QFileDialog.getOpenFileName( self, "Open file", "./", "CSV (*.csv)")

        if lstFileName[0]:
            SPL_strFileName = os.path.basename( lstFileName[0] )
            try:
                global SPL_dfData
                SPL_dfData = pd.read_csv( lstFileName[0], encoding="cp949" )
                lstColumns = SPL_dfData.columns
                self.listWidget_Columns.clear()
                for i, strColumn in enumerate(lstColumns) :
                    self.listWidget_Columns.addItem( strColumn )

            except Exception as e:
                print( f"error at opening \"{lstFileName[0]}\"")
                print( e )



    def OnBtnClick_Down(self):
        global SPL_lstChkData
        lstColData = [ x0 for x0, x1 in SPL_lstChkData ]
        lstItems = self.listWidget_Columns.selectedItems()

        print( SPL_lstChkData )
        for ItemElement in lstItems:
            ItemEntity = ItemElement.text()
            if ItemEntity not in lstColData:
                SPL_lstChkData.append( [ItemEntity, 2] )
        print( SPL_lstChkData )

        # TableWidget
        self._UpdateCheckBoxAll()



    def OnBtnClick_Up(self):
        global SPL_lstChkData
        lstColData = [ x0 for x0, x1 in SPL_lstChkData ]

        lstItems = []
        lstSelectedItem = self.table.selectedItems()

        for ItemEntity in lstSelectedItem:
            lstItems.append( ItemEntity.text() )

        print("lstItems", lstItems)


        print( "SPL_lstChkData", SPL_lstChkData )
        lstTemp = lstColData
        for ItemEntity in lstItems:
            if ItemEntity in lstColData:
                lstTemp.remove( ItemEntity )
        lstColData = lstTemp

        lstTemp = SPL_lstChkData
        for x0, x1 in SPL_lstChkData:
            if x0 not in lstColData:
                lstTemp.remove( [x0, x1] )
        SPL_lstChkData = lstTemp

        print(SPL_lstChkData)

        self._UpdateCheckBoxAll()






    def __checkbox_change(self, checkvalue):
        global SPL_lstChkData
        lstIdx = self.table.selectedIndexes()

        if( len(lstIdx) > 0):
            ckbox = self.table.cellWidget( lstIdx[0].row(), lstIdx[0].column())
            # print(ckbox)
            if isinstance(ckbox, QCheckBox):
                if ckbox.isChecked():
                    print( lstIdx[0].row(), lstIdx[0].column(), " checked")
                    # global 변수 업데이트
                    SPL_lstChkData[lstIdx[0].row()][1] = lstIdx[0].column()
                else:
                    print( lstIdx[0].row(), lstIdx[0].column(), " no checked")

            else:
                pass
            #    _ = QMessageBox.information(self, 'checkbox', "checkbox 아닙니다.")

            # Global 변수 대로 상태 업데이트
            for iRow, (dname, iChkPos) in enumerate(SPL_lstChkData):
                for iCol in range( 1, 4 ): # X, Y1, Y2
                    ckbox = self.table.cellWidget( iRow, iCol )
                    if( SPL_lstChkData[iRow][1] == iCol ):
                        ckbox.setChecked( True )
                    else:
                        ckbox.setChecked( False )



    def _UpdateCheckBoxAll(self):
        global SPL_lstChkData

        # TableWidget
        self.table.clearContents()  # 헤더는 제거 안함.
        self.table.setRowCount( len(SPL_lstChkData) )
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Name", "X", "Y1", "Y2"])

        for iRow, (dname, iChkPos) in enumerate(SPL_lstChkData):
            # "name"
            self.table.setItem(iRow, 0, QTableWidgetItem(dname))

            for i in range(3): # X, Y1, Y2
                iCol = i + 1
                ChkBox = QCheckBox()
                self.table.setCellWidget(iRow, iCol, ChkBox )
                ChkBox.setStyleSheet("text-align: center; margin-left:10%; margin-right:10%;");
                ChkBox.setContentsMargins(0, 0, 0, 0);
                ChkBox.stateChanged.connect(self.__checkbox_change)  # sender() 확인용 예..

        self.table.horizontalHeaderItem(0).setToolTip("Column Name in CSV") # header tooltip

        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()


        self.table.cellClicked.connect(self._cellclicked)

        # Global 변수 대로 상태 업데이트
        for iRow, (dname, iChkPos) in enumerate(SPL_lstChkData):
            for iCol in range( 1, 4 ): # X, Y1, Y2
                ckbox = self.table.cellWidget( iRow, iCol )
                if isinstance(ckbox, QCheckBox):
                    if( SPL_lstChkData[iRow][1] == iCol ):
                        ckbox.setChecked( True )
                    else:
                        ckbox.setChecked( False )



    def _UpdateCheckBoxState(self):

        global SPL_lstChkData

        # Global 변수 대로 상태 업데이트
        for iRow, (dname, iChkPos) in enumerate(SPL_lstChkData):
            for iCol in range( 1, 4 ): # X, Y1, Y2
                ckbox = self.table.cellWidget( iRow, iCol )
                if isinstance(ckbox, QCheckBox):
                    if( SPL_lstChkData[iRow][1] == iCol ):
                        ckbox.setChecked( True )
                    else:
                        ckbox.setChecked( False )



    def _cellclicked(self, row, col):
        print("_cellclicked... ", row, col)




    # DataFrame()의 column 이름이 중복일때 수정하기 위해
    def vFixColumnName(self):
        pass

    def OnBtnClick_Plt(self):

        global SPL_lstChkData

        XAttr = []
        lstY1Attr = []
        lstY2Attr = []

        for x0, x1 in SPL_lstChkData:

            if( x1 == 1 ): # X axis
                XAttr = x0
            elif( x1 == 2 ): # y1 axis
                lstY1Attr.append( x0 )
            elif( x1 == 3 ): # y2 axis
                lstY2Attr.append( x0 )
            else:
                pass

        if( len(SPL_dfData) > 0):

            self.MplWidget.canvas.axes.clear()

            if( len(lstY1Attr) > 0):
                x_data = np.arange( len( SPL_dfData[lstY1Attr[0]] ) )

                if( len(XAttr) > 0 ):
                    x_data = SPL_dfData[XAttr].to_numpy( )

                for Y1Attr in lstY1Attr :
                    y_data = SPL_dfData[Y1Attr].to_numpy( )
                    self.MplWidget.canvas.axes.plot( x_data, y_data )

                self.MplWidget.canvas.axes.grid(True)
                self.MplWidget.canvas.axes.legend( lstY1Attr, loc='upper right')
                self.MplWidget.canvas.axes.set_title( SPL_strFileName )

                try:
                    self.MplWidget.canvas.draw()
                except Exception as e:
                    print(e)


'''
        fs = 500
        f = random.randint(1, 100)
        ts = 1 / fs
        length_of_signal = 100
        x = np.linspace(0, 1, length_of_signal)

        cosinus_signal = np.cos(2 * np.pi * f * x)
        sinus_signal = np.sin(2 * np.pi * f * x)

        self.MplWidget.canvas.axes.clear()
        self.MplWidget.canvas.axes.plot(x, cosinus_signal)
        self.MplWidget.canvas.axes.plot(x, sinus_signal)
        self.MplWidget.canvas.axes.legend(('cosinus', 'sinus'), loc='upper right')
        self.MplWidget.canvas.axes.set_title('Cosinus - Sinus Signal')
        self.MplWidget.canvas.draw()
'''

app = QApplication([])
window = MatplotlibWidget()
window.show()
app.exec_()
