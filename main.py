# ------------------------------------------------------
# ---------------------- main.py -----------------------
# ------------------------------------------------------
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt

from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
from matplotlib import cm # colormap

import numpy as np
import random
import pandas as pd
import os
import copy
import datetime
import re

SPL_dfData = pd.DataFrame()
SPL_lstChkData = [] # ["  signal name  ", 0]
SPL_strFileName = ""


# "2022-04-26 11:54:23" -> 1463460958000 (초단위)
def strptime2Timestamp(lstStrTime):
    lstDateTime = []  # str -> datetime
    lstTimeStamp = []  # str -> timestamp

    '''
    "2022-04-26 11:54:23"
        0 : 2
        1 : 0
        2 : 2
        3 : 2
        4 : -
        5 : 0
        6 : 4
        7 : -
        8 : 2
        9 : 6
        10 :  
        11 : 1
        12 : 1
        13 : :
        14 : 5
        15 : 4
        16 : :
        17 : 2
        18 : 3
    '''

    # 특정 포멧을 맞추고 있다면
    if( str(type(lstStrTime[0]) ) == "<class \'str\'>" ): # str 형이면

        if( len(lstStrTime[0]) > 18 ):

            if (lstStrTime[0][4] == '-') \
                and (lstStrTime[0][7] == '-') \
                and (lstStrTime[0][10] == ' ') \
                and (lstStrTime[0][13] == ':') \
                and (lstStrTime[0][16] == ':'):

                for strTime in lstStrTime:

                    try:
                        # 라이브러리를 이용한 변환
                        dateTimeOne = datetime.datetime.strptime(strTime, '%Y-%m-%d %H:%M:%S')
                        lstDateTime.append(dateTimeOne)
                        timestampOne = datetime.datetime.timestamp(dateTimeOne)
                        lstTimeStamp.append(timestampOne)
                    except:  # 변환에 에러 발생시, 수동으로 변환. 범위 오류도 수정
                        # print( strTime )
                        numbers = re.findall('\d+', strTime)
                        year = int(numbers[0])  # year
                        month = int(numbers[1])  # month
                        day = int(numbers[2])  # day
                        hour = int(numbers[3])  # hour
                        mininute = int(numbers[4])  # min
                        second = int(numbers[5])  # sec
                        if second > 59:
                            second = 59
                        dateTimeOne = datetime.datetime(year, month, day, hour, mininute, second)
                        lstDateTime.append(dateTimeOne)
                        timestampOne = datetime.datetime.timestamp(dateTimeOne)
                        lstTimeStamp.append(timestampOne)


    return lstDateTime, lstTimeStamp



#
# Diaglog 창의 이름을  "Y1 axis customize", "Y2 axis customize" 으로 바꾸기 위해
#


'''
import matplotlib.backends.qt_editor.figureoptions as figureoptions

edit_parameters = NavigationToolbar.edit_parameters # 이전값 저장

def my_edit_parameters(self):
    # PreHook Here!
    # print( "PreHook" )
    #
    #
    #

    axes = self.canvas.figure.get_axes()
    if not axes:
        QMessageBox.warning(
            self.parent, "Error", "There are no axes to edit.")
        return
    elif len(axes) == 1:
        ax, = axes
    else:
        titles = [ "Y1 axis customize", "Y2 axis customize" ]
        item, ok = QInputDialog.getItem( self.parent, 'Customize', 'Select axes:', titles, 0, False )
        if not ok:
            return
        ax = axes[titles.index(item)]
    figureoptions.figure_edit(ax, self)


    # PostHook Here!
    # print( "PostHook" )
    #
    #
    #

NavigationToolbar.edit_parameters = my_edit_parameters # 새로운 함수로 대체

'''




class MatplotlibWidget(QMainWindow):

    def __init__(self):
        
        QMainWindow.__init__(self)


        loadUi("qt_designer.ui",self)
        self.setWindowIcon(QIcon('iconPlot.png')) # 맨왼쪽위 아이콘
        self.setWindowTitle("Simple Matplotlib w/ GUI")

        self.MplWidget.canvas.axes = self.MplWidget.canvas.figure.add_subplot(111)
        self.MplWidget.canvas.axes_2 = self.MplWidget.canvas.axes.twinx()

        # 좌표값
        # (출처) https://stackoverflow.com/questions/21583965/matplotlib-cursor-value-with-two-axes
        def make_format(current, other):
            # current and other are axes
            def format_coord(x, y):
                # x, y are data coordinates
                # convert to display coords
                display_coord = current.transData.transform((x, y))
                inv = other.transData.inverted()
                # convert back to data coords with respect to ax
                ax_coord = inv.transform(display_coord)
                coords = [ax_coord, (x, y)]
                return ('Left: {:<40}    Right: {:<}'.format(*['({:.3f}, {:.3f})'.format(x, y) for x, y in coords]))

            return format_coord

        self.MplWidget.canvas.axes_2.format_coord = make_format(self.MplWidget.canvas.axes_2, self.MplWidget.canvas.axes)



        # 툴바
        self.addToolBar(NavigationToolbar(self.MplWidget.canvas, self))
        # 버튼 signal
        self.pushButton_OpenFile.clicked.connect(self.OnBtnClick_OpenFile)
        self.pushButton_Up.clicked.connect(self.OnBtnClick_Up)
        self.pushButton_Down.clicked.connect(self.OnBtnClick_Down)
        self.pushButton_Plt.clicked.connect(self.OnBtnClick_Plt)
        # 버튼 아이콘 표시하기
        self.pushButton_OpenFile.setIcon(QIcon('iconFile.png'))
        self.pushButton_Up.setIcon(QIcon('iconUp.png'))
        self.pushButton_Down.setIcon(QIcon('iconDown.png'))
        self.pushButton_Plt.setIcon(QIcon('iconPlot.png'))



        # 현재 위치
        self.base_path = os.getcwd()

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
        global SPL_dfData
        global SPL_lstChkData

		#
        # list형태로 쌓은 pd.DataFrame()을 시간 순서로 합쳐서 pd.DataFrame() 형으로 return
		#
        def dfMergeEachLog(lstDataFrame):

            dfMerge = pd.DataFrame()
            for Idx, DataFrame in enumerate(lstDataFrame):
                input_df = lstDataFrame[Idx]
                dfMerge = pd.concat([dfMerge, input_df], axis=0, ignore_index=True)

            return dfMerge

        # 지정된 경로에 파일을 찾아, read_csv() 후 DataFrame 형을 list로 누적함
        def lstGetDataFrame(lstFiles):

            lstDataFrame = []

            for filename in lstFiles:

                # 파일이름 정의
                strFileName = os.path.basename(filename)  # 파일이름만

                df = pd.DataFrame()
                try:
                    print("{}".format(strFileName))
                    df = pd.read_csv(filename, encoding="cp949")  # *.csv 파일 열기
                except Exception as e:
                    try:
                        df = pd.read_csv(filename, encoding='utf-8')  # *.csv 파일 열기
                    except:
                        print("Error pd.read_csv( )")
                        print(e)

                dfData = pd.DataFrame.copy(df[:])  # hard copy
                # dfData.loc[0] = strFileName

                # pd.DataFrame() 의 list 에 저장함
                lstDataFrame.append(dfData)

            return lstDataFrame

        tupFileName = QFileDialog.getOpenFileNames( self, "Open file", self.base_path, "CSV (*.csv)")
        lstFileName = tupFileName[0]
        lstFileName.sort()

        if len( lstFileName ) > 0:
		
            self.base_path = os.path.dirname(lstFileName[0]) # 파일의 Path를 기억
            SPL_strFileName = os.path.basename( lstFileName[0] )

            try:
                lstDataFrame = lstGetDataFrame(lstFileName)
                SPL_dfData = dfMergeEachLog(lstDataFrame)
                lstColumns = SPL_dfData.columns
                self.listWidget_Columns.clear()
                for i, strColumn in enumerate(lstColumns) :
                    self.listWidget_Columns.addItem( strColumn )

                SPL_lstChkData = []  # init
                self._UpdateCheckBoxAll()

            except Exception as e:
                print( f"error at opening \"{lstFileName[0]}\"")
                print(e)
                _ = QMessageBox.information(self, e)




    def OnBtnClick_Down(self):
        global SPL_lstChkData
        lstColData = [ x0 for x0, x1 in SPL_lstChkData ]
        lstItems = self.listWidget_Columns.selectedItems()

        # print( SPL_lstChkData )
        for ItemElement in lstItems:
            ItemEntity = ItemElement.text()
            if ItemEntity not in lstColData:
                SPL_lstChkData.append( [ItemEntity, 2] )
        # print( SPL_lstChkData )

        # TableWidget
        self._UpdateCheckBoxAll()



    def OnBtnClick_Up(self):
        global SPL_lstChkData
        lstColData = [ x0 for x0, x1 in SPL_lstChkData ]

        lstItems = []
        lstSelectedItem = self.table.selectedItems()

        for ItemEntity in lstSelectedItem:
            lstItems.append( ItemEntity.text() )
        #print("lstItems", lstItems)

        lstTemp = copy.deepcopy( SPL_lstChkData ) # shadow copy시 자신을 지우는 문제 발생
        for x0, x1 in SPL_lstChkData:
            if x0 in lstItems:
                lstTemp.remove( [x0, x1] )
        SPL_lstChkData = lstTemp
        #print(SPL_lstChkData)

        self._UpdateCheckBoxAll()



    def __checkbox_change(self, checkvalue):
        global SPL_lstChkData
        lstIdx = self.table.selectedIndexes()

        if( len(lstIdx) > 0):
            ckbox = self.table.cellWidget( lstIdx[0].row(), lstIdx[0].column())
            # print(ckbox)
            if isinstance(ckbox, QCheckBox):
                if ckbox.isChecked():
                    # print( lstIdx[0].row(), lstIdx[0].column(), " checked")
                    # global 변수 업데이트
                    SPL_lstChkData[lstIdx[0].row()][1] = lstIdx[0].column()
                else:
                    # 만일 check  상태에서 클릭한다면
                    if( SPL_lstChkData[lstIdx[0].row()][1] == lstIdx[0].column() ):
                        SPL_lstChkData[lstIdx[0].row()][1] = 0
                    # print( lstIdx[0].row(), lstIdx[0].column(), " no checked")

            else:
                pass
            #    _ = QMessageBox.information(self, 'checkbox', "checkbox 아닙니다.")

            self._UpdateCheckBoxState()



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

        self._UpdateCheckBoxState()


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
        pass
        #print("_cellclicked... ", row, col)


    # DataFrame()의 column 이름이 중복일때 수정하기 위해
    def vFixColumnName(self):
        pass

    def OnBtnClick_Plt(self):

        global SPL_lstChkData

        XAttr = []
        lstY1Attr = []
        lstY2Attr = []

        # 각축별로 뭘 그려야 하는지
        for x0, x1 in SPL_lstChkData:

            if( x1 == 1 ): # X axis
                XAttr = x0
            elif( x1 == 2 ): # y1 axis
                lstY1Attr.append( x0 )
            elif( x1 == 3 ): # y2 axis
                lstY2Attr.append( x0 )
            else:
                pass

        lstSelectedItemText = []
        lstSelectedItem = self.table.selectedItems()

        for ItemEntity in lstSelectedItem:
            lstSelectedItemText.append( ItemEntity.text() )
        #print("lstItems", lstSelectedItemText)


        if( len(SPL_dfData) > 0): # DataFrame을 읽어 들였다면

            # 백업을 위한 이전 축 설정 GET, 저장
            #ax1_xmin, ax1_xmax = self.MplWidget.canvas.axes.get_xlim() 
            #ax1_ymin, ax1_ymax = self.MplWidget.canvas.axes.get_ylim()
            ax1_xlabel = self.MplWidget.canvas.axes.get_xlabel()
            ax1_ylabel = self.MplWidget.canvas.axes.get_ylabel()
            ax2_xlabel = self.MplWidget.canvas.axes_2.get_xlabel()
            ax2_ylabel = self.MplWidget.canvas.axes_2.get_ylabel()

            # 화면 지우기
            self.MplWidget.canvas.axes.clear( ) # 화면을 지움
            self.MplWidget.canvas.axes_2.clear( )  # 화면을 지움

            # 백업을 위한 이전 축 설정 SET
            if '' != ax1_xlabel:
                self.MplWidget.canvas.axes.set_xlabel(ax1_xlabel)
            if '' != ax1_ylabel:
                self.MplWidget.canvas.axes.set_ylabel(ax1_ylabel)
            if '' != ax2_xlabel:
                self.MplWidget.canvas.axes_2.set_xlabel(ax2_xlabel)
            if '' != ax2_ylabel:
                self.MplWidget.canvas.axes_2.set_ylabel(ax2_ylabel)



            if( (len(lstY1Attr) > 0) or (len(lstY2Attr) > 0) ): # Y1 에 그릴 데이터가 있다면

                # X축에 그릴 데이터
                if( len(XAttr) > 0 ): # X에 그릴 데이터가 있다면
                    x_data = SPL_dfData[XAttr].to_numpy( )
                    
                    # 시간으로 변환
                    lstDateTime, lstTimeStamp = strptime2Timestamp( SPL_dfData[XAttr].values.tolist()  )
                    if( len(lstDateTime) == len(SPL_dfData[XAttr]) ): # 같은 사이즈 만큼 변환하였다면
                        x_data = lstDateTime
                        SPL_dfData[XAttr] = lstDateTime # 한번 변환한 것은 다시 변환 안하기 위해

                else:
                    if (len(lstY1Attr) > 0):  # Y1 에 그릴 데이터가 있다면
                        x_data = np.arange( len( SPL_dfData[lstY1Attr[0]] ) ) # X 를 선택안했을 경우를 대비해서 X 축 데이터 만듦
                    elif (len(lstY2Attr) > 0):  # Y2 에 그릴 데이터가 있다면
                        x_data = np.arange( len( SPL_dfData[lstY2Attr[0]] ) ) # X 를 선택안했을 경우를 대비해서 X 축 데이터 만듦

                # Y1축에 그릴 데이터
                if (len(lstY1Attr) > 0):  # Y1 에 그릴 데이터가 있다면
                    #colorsY1 = cm.tab20( np.linspace(0, 1, len(SPL_dfData.columns)) )
                    #colorsY1 = cm.rainbow(np.linspace(0, 1, len(SPL_dfData.columns)))
                    '''
                    colorsY1 = ['#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#ff9896',
                       '#9467bd', '#c5b0d5', '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f', '#c7c7c7',
                       '#bcbd22', '#dbdb8d', '#17becf', '#9edae5']
                    '''

                    for i, Y1Attr in enumerate(lstY1Attr) :
                        y_data = SPL_dfData[Y1Attr].to_numpy( )

                        # 시간으로 변환
                        lstDateTime, lstTimeStamp = strptime2Timestamp( SPL_dfData[Y1Attr].values.tolist() )
                        if (len(lstDateTime) == len(SPL_dfData[XAttr])): # 같은 사이즈 만큼 변환하였다면
                            y_data = lstDateTime
                            SPL_dfData[Y1Attr] = lstDateTime # 한번 변환한 것은 다시 변환 안하기 위해


                        if Y1Attr in lstSelectedItemText:  # 현재 선택되어 있다면
                            line, = self.MplWidget.canvas.axes.plot( x_data, y_data, '-o', linewidth=0.8) #, drawstyle='steps-post' ) #, color=colorsY1[i%len(colorsY1)] )
                        else:
                            line, = self.MplWidget.canvas.axes.plot(x_data, y_data, linewidth=0.8 ) #, drawstyle='steps-post' )  # , color=colorsY1[i%len(colorsY1)] )
                        line.set_label( Y1Attr ) # 'Figure Options' 창에서 Curve이름 표시하기 위해

                    self.MplWidget.canvas.axes.legend( lstY1Attr, loc='upper left')



                # Y2축에 그릴 데이터
                if (len(lstY2Attr) > 0):  # Y2 에 그릴 데이터가 있다면
                    #colorsY2 = cm.Set3( np.linspace(0, 1, len(SPL_dfData.columns)) )
                    #colorsY2 = cm.gist_rainbow(np.linspace(0, 1, len(SPL_dfData.columns)))
                    colorsY2 = ["red", "orange", "yellow", "green", "blue", "indigo", "violet"]
                    for i, Y2Attr in enumerate(lstY2Attr) :
                        y2_data = SPL_dfData[Y2Attr].to_numpy( )

                        # 시간으로 변환
                        lstDateTime, lstTimeStamp = strptime2Timestamp( SPL_dfData[Y2Attr].values.tolist() )
                        if (len(lstDateTime) == len(SPL_dfData[XAttr])): # 같은 사이즈 만큼 변환하였다면
                            y2_data = lstDateTime
                            SPL_dfData[Y2Attr] = lstDateTime # 한번 변환한 것은 다시 변환 안하기 위해

                        if Y2Attr in lstSelectedItemText:  # 현재 선택되어 있다면
                            line, = self.MplWidget.canvas.axes_2.plot(x_data, y2_data, '-o', linewidth=0.8, color=colorsY2[i%len(colorsY2)] )#, drawstyle='steps-post' )
                        else:
                            line, = self.MplWidget.canvas.axes_2.plot(x_data, y2_data, linewidth=0.8, color=colorsY2[i % len(colorsY2)] ) #, drawstyle='steps-post' )
                        line.set_label(Y2Attr)  # 'Figure Options' 창에서 Curve이름 표시하기 위해
                        
                    self.MplWidget.canvas.axes_2.legend( lstY2Attr, loc='upper right')
                    self.MplWidget.canvas.axes_2.get_yaxis().set_visible(True) # 데이터가 있으면 Y2 축 보이기

                else:
                    # Y2축 데이터가 없다면, Y2축 X 데이터가 없어서 Range 오류 발생
                    width = max(x_data) - min(x_data)
                    self.MplWidget.canvas.axes.set_xlim(min(x_data)-width/20, max(x_data)+width/20)
                    self.MplWidget.canvas.axes_2.set_xlim(min(x_data)-width/20, max(x_data)+width/20)
                    # 데이터 없으면 우측 Y2 숨기기
                    self.MplWidget.canvas.axes_2.get_yaxis().set_visible(False)  # 데이터가 없으면 Y2 축 숨기기




                self.MplWidget.canvas.axes.grid(True)
                self.MplWidget.canvas.axes.set_title( SPL_strFileName )
                #self.MplWidget.canvas.axes.title.set_size(20)

                try:
                    self.MplWidget.canvas.draw()
                except Exception as e:
                    print(e)
                    _ = QMessageBox.information(self, e)



app = QApplication([])
window = MatplotlibWidget()
window.show()
app.exec_()

















