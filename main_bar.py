# ------------------------------------------------------
# ---------------------- main.py -----------------------
# ------------------------------------------------------
from PyQt5.QtWidgets import (QApplication, QInputDialog, QMainWindow, QMessageBox, QFileDialog, QTableWidgetItem, QCheckBox, QDialog, QAction)
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
import matplotlib.backends.qt_editor.figureoptions as figureoptions
# from matplotlib import cm # colormap
import matplotlib.dates as mdates
from matplotlib.artist import Artist

import numpy as np
import pandas as pd
import os
import copy
import datetime
import re
import random



# Configuration for SimplePlt
ChartType_Plot = 1
ChartType_Scatter = 2
ChartType_Bar = 3
CFG_ChartType = ChartType_Bar
CFG_Legend_Max = 30
CFG_Legend_MaxMax = 600
CFG_Plot_DrawType = "steps-post"
CFG_Plot_Alpha_Selected = 1.0
CFG_Plot_Alpha_Unselected = 0.8
CFG_Scatter_Alpha_Selected = 0.8
CFG_Scatter_Alpha_Unselected = 0.6
CFG_Scatter_MarkerSize_Selected = 20
CFG_Scatter_MarkerSize_Unselected = 1
CFG_Bar_ColorGroup = "PSA_Wave"
CFG_Bar_Alpha_Unselected = 0.1
CFG_Bar_DataLength = 10

# Global variables
SPL_dfData = pd.DataFrame()
#                          신호명         체크되는열(신호당 1개의 체크박스만 클릭가능함)
#                                        0:none, 1:첫번째(X), 2:두번째(Y1), ...
SPL_lstChkData = [] # ["  signal name  ", 0]
SPL_strFileName = ""






CFG_lstGrouping_index_PSA6Module = [
    # text        Cell index ( not Cell No)
    ["module_01", [ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13]],
    ["module_02", [14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]],
    ["module_03", [28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41]],
    ["module_04", [42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55]],
    ["module_05", [56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69]],
    ["module_06", [70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83]],
]


CFG_lstGrouping_index_PSA7Module = [
    # text        Cell index ( not Cell No)
    ["module_01", [ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13]],
    ["module_02", [14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]],
    ["module_03", [28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41]],
    ["module_04", [42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55]],
    ["module_05", [56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69]],
    ["module_06", [70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83]],
    ["module_07", [84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95]],
]

CFG_lstGrouping_index_FcaRu = [
    # text        Cell index ( not Cell No)
    ["module_01", [ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15]],
    ["module_02", [16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]],
    ["module_03", [32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47]],
    ["module_04", [48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63]],
    ["module_05", [64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79]],
    ["module_06", [80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95]],

]

CFG_lstGrouping_index_GmBolt = [
    # text        Cell index ( not Cell No)
    ["module_01", [ 0,  1,  2,  3,  4,  5,  6,  7 ]],
    ["module_02", [ 8,  9, 10, 11, 12, 13, 14, 15 ]],
    ["module_03", [16, 17, 18, 19, 20, 21, 22, 23 ]],
    ["module_04", [24, 25, 26, 27, 28, 29, 30, 31, 32 ]],
    ["module_05", [33, 34, 35, 36, 37, 38, 39, 40 ]],
    ["module_06", [41, 42, 43, 44, 45, 46, 47 ]],
    ["module_07", [48, 49, 50, 51, 52, 53, 54, 55 ]],
    ["module_08", [56, 57, 58, 59, 60, 61, 62, 63 ]],
    ["module_09", [64, 65, 66, 67, 68, 69, 70, 71 ]],
    ["module_10", [72, 73, 74, 75, 76, 77, 78, 79 ]],
    ["module_11", [80, 81, 82, 83, 84, 85, 86, 87 ]],
    ["module_12", [88, 89, 90, 91, 92, 93, 94, 95 ]],

]

CFG_lstGrouping_index_RsaE57 = [
    # text        Cell No
    ["module_01", [ 0,  1,  2,  3,  4,  5,  6,  7]],
    ["module_02", [ 8,  9, 10, 11, 12, 13, 14, 15]],
    ["module_03", [16, 17, 18, 19, 20, 21, 22, 23]],
    ["module_04", [24, 25, 26, 27, 28, 29, 30, 31]],
    ["module_05", [32, 33, 34, 35, 36, 37, 38, 39]],
    ["module_06", [40, 41, 42, 43, 44, 45, 46, 47]],
    ["module_07", [48, 49, 50, 51, 52, 53, 54, 55]],
    ["module_08", [56, 57, 58, 59, 60, 61, 62, 63]],
    ["module_09", [64, 65, 66, 67, 68, 69, 70, 71]],
    ["module_10", [72, 73, 74, 75, 76, 77, 78, 79]],
    ["module_11", [80, 81, 82, 83, 84, 85, 86, 87]],
    ["module_12", [88, 89, 90, 91, 92, 93, 94, 95]],
]

CFG_lstGrouping_index  = CFG_lstGrouping_index_PSA7Module




def Timestamp2DateTime( lstTimestamp ):

    lstDateTime = []  # str -> datetime
    for Timestamp in lstTimestamp:
        dateTimeOne = datetime.datetime.utcfromtimestamp(Timestamp)
        lstDateTime.append( dateTimeOne )

    return lstDateTime



#                                                                2021-06-30T07:36:10.000Z  2021-06-30T07:36:10Z 
strptime_patterns = ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M:%S.%f', '%Y-%m-%dT%H:%M:%S.%fZ', '%Y-%m-%dT%H:%M:%SZ', "%d-%m-%Y", "%Y-%m-%d"]
def GetDatetime(strClock): # 다양한 형태의 clock 패턴을 처리
    global strptime_patterns

    boNoon = False
    if " 오전" in strClock:
        strClock = strClock.replace(" 오전", "")
    elif " 오후" in strClock:
        strClock = strClock.replace(" 오후", "")
        boNoon = True


    try:
        datetimeClock = datetime.datetime.fromisoformat(strClock)
        if boNoon == True:
            datetimeClock = datetimeClock + datetime.timedelta(hours=12)
        return datetimeClock
    except:
        pass


    for (i, pattern) in enumerate(strptime_patterns):
        try:
            datetimeClock = datetime.datetime.strptime(strClock, pattern)
            if boNoon == True:
                datetimeClock = datetimeClock + datetime.timedelta(hours=12)
            if (i!=0): # 다음을 위해 맨 앞에 위치
                strptime_patterns[i] = strptime_patterns[0]
                strptime_patterns[0] = pattern
            return datetimeClock
        except:
            pass

    print ("Date is not in expected format: %s" % (strClock))
    return strClock



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
                and ((lstStrTime[0][10] == ' ') or (lstStrTime[0][10] == 'T')) \
                and (lstStrTime[0][13] == ':') \
                and (lstStrTime[0][16] == ':'):

                for strTime in lstStrTime:

                    try:
                        # 라이브러리를 이용한 변환
                        dateTimeOne = GetDatetime(strTime)

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
            self, "Error", "There are no axes to edit.")
        return
    elif len(axes) == 1:
        ax, = axes
    else:
        ''' org code below
        
        titles = [
            ax.get_label() or
            ax.get_title() or
            " - ".join(filter(None, [ax.get_xlabel(), ax.get_ylabel()])) or
            f"<anonymous {type(ax).__name__}>"
            for ax in axes]
        duplicate_titles = [
            title for title in titles if titles.count(title) > 1]
        for i, ax in enumerate(axes):
            if titles[i] in duplicate_titles:
                titles[i] += f" (id: {id(ax):#x})"  # Deduplicate titles.
        '''
        titles = [ "Y1 axis customize", "Y2 axis customize" ]
        item, ok = QInputDialog.getItem(
            self, 'Customize', 'Select axes:', titles, 0, False)
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

# 두문자의 공통부분을 찾기 위한 함수
def get_str_array(s):
    return {s[i:j] for i in range(len(s)) for j in range(i, len(s) + 1)}






class dlgChartType(QDialog):


    def __init__(self):
        global CFG_ChartType
        global CFG_Plot_DrawType
        global CFG_Plot_Alpha_Selected
        global CFG_Plot_Alpha_Unselected
        global CFG_Scatter_Alpha_Selected
        global CFG_Scatter_Alpha_Unselected
        global CFG_Scatter_MarkerSize_Selected
        global CFG_Scatter_MarkerSize_Unselected
        global CFG_Bar_Alpha_Unselected

        super().__init__()
        self.setupUI()
        self.setWindowIcon(QIcon('iconChartTypeOption.png')) # 맨왼쪽위 아이콘
        self.setWindowTitle("Chart type setting")

        # widget의 초기값
        if(CFG_ChartType == ChartType_Plot):
            self.radioButton_plot.setChecked(True)
            self.radioButton_scatter.setChecked(False)
            self.radioButton_bar.setChecked(False)
            self.tabWidget.setCurrentIndex(0)

        elif(CFG_ChartType == ChartType_Scatter):
            self.radioButton_plot.setChecked(False)
            self.radioButton_scatter.setChecked(True)
            self.radioButton_bar.setChecked(False)
            self.tabWidget.setCurrentIndex(1)

        elif(CFG_ChartType == ChartType_Bar):
            self.radioButton_plot.setChecked(False)
            self.radioButton_scatter.setChecked(False)
            self.radioButton_bar.setChecked(True)
            self.tabWidget.setCurrentIndex(2)

        # stopping check box to get checked
        self.radioButton_plot.setCheckable(False)
        self.radioButton_scatter.setCheckable(False)
        self.radioButton_bar.setCheckable(True)


        self.comboBox_Plot_DrawStyle.addItem("default")
        self.comboBox_Plot_DrawStyle.addItem("steps-post")
        if( CFG_Plot_DrawType=="default"):
            self.comboBox_Plot_DrawStyle.setCurrentIndex(0)
        elif( CFG_Plot_DrawType=="steps-post"):
            self.comboBox_Plot_DrawStyle.setCurrentIndex(1)

        self.comboBox_Bar_ColorGroup.addItem("none")
        self.comboBox_Bar_ColorGroup.addItem("PSA_Wave")
        self.comboBox_Bar_ColorGroup.addItem("FCA_RU")
        self.comboBox_Bar_ColorGroup.addItem("GM_Bolt")
        if( CFG_Bar_ColorGroup=="none"):
            self.comboBox_Bar_ColorGroup.setCurrentIndex(0)
        elif( CFG_Bar_ColorGroup=="PSA_Wave"):
            self.comboBox_Bar_ColorGroup.setCurrentIndex(1)
        elif( CFG_Bar_ColorGroup=="FCA_RU"):
            self.comboBox_Bar_ColorGroup.setCurrentIndex(2)
        elif( CFG_Bar_ColorGroup=="GM_Bolt"):
            self.comboBox_Bar_ColorGroup.setCurrentIndex(3)


        self.doubleSpinBox_Plot_Alpha_Select.setRange(0, 1) # 최소값 ~ 최대값
        self.doubleSpinBox_Plot_Alpha_Select.setSingleStep(0.1) # 한 스텝 변화
        self.doubleSpinBox_Plot_Alpha_Select.setDecimals(3) # 소수점 아래 표시될 자리수
        self.doubleSpinBox_Plot_Alpha_Select.setValue(CFG_Plot_Alpha_Selected)
        self.doubleSpinBox_Plot_Alpha_NoSelect.setRange(0, 1) # 최소값 ~ 최대값
        self.doubleSpinBox_Plot_Alpha_NoSelect.setSingleStep(0.1) # 한 스텝 변화
        self.doubleSpinBox_Plot_Alpha_NoSelect.setDecimals(3) # 소수점 아래 표시될 자리수
        self.doubleSpinBox_Plot_Alpha_NoSelect.setValue(CFG_Plot_Alpha_Unselected)

        self.doubleSpinBox_Scatter_Alpha_Select.setRange(0, 1) # 최소값 ~ 최대값
        self.doubleSpinBox_Scatter_Alpha_Select.setSingleStep(0.1) # 한 스텝 변화
        self.doubleSpinBox_Scatter_Alpha_Select.setDecimals(3) # 소수점 아래 표시될 자리수
        self.doubleSpinBox_Scatter_Alpha_Select.setValue(CFG_Scatter_Alpha_Selected)
        self.doubleSpinBox_Scatter_Alpha_NoSelect.setRange(0, 1) # 최소값 ~ 최대값
        self.doubleSpinBox_Scatter_Alpha_NoSelect.setSingleStep(0.1) # 한 스텝 변화
        self.doubleSpinBox_Scatter_Alpha_NoSelect.setDecimals(3) # 소수점 아래 표시될 자리수
        self.doubleSpinBox_Scatter_Alpha_NoSelect.setValue(CFG_Scatter_Alpha_Unselected)

        self.doubleSpinBox_Scatter_MarkerSize_Select.setRange(0, 100) # 최소값 ~ 최대값
        self.doubleSpinBox_Scatter_MarkerSize_Select.setSingleStep(1) # 한 스텝 변화
        self.doubleSpinBox_Scatter_MarkerSize_Select.setDecimals(1) # 소수점 아래 표시될 자리수
        self.doubleSpinBox_Scatter_MarkerSize_Select.setValue(CFG_Scatter_MarkerSize_Selected)
        self.doubleSpinBox_Scatter_MarkerSize_NoSelect.setRange(0, 100) # 최소값 ~ 최대값
        self.doubleSpinBox_Scatter_MarkerSize_NoSelect.setSingleStep(1) # 한 스텝 변화
        self.doubleSpinBox_Scatter_MarkerSize_NoSelect.setDecimals(1) # 소수점 아래 표시될 자리수
        self.doubleSpinBox_Scatter_MarkerSize_NoSelect.setValue(CFG_Scatter_MarkerSize_Unselected)


        self.doubleSpinBox_Bar_Alpha_NoSelect.setRange(0, 1) # 최소값 ~ 최대값
        self.doubleSpinBox_Bar_Alpha_NoSelect.setSingleStep(0.1) # 한 스텝 변화
        self.doubleSpinBox_Bar_Alpha_NoSelect.setDecimals(3) # 소수점 아래 표시될 자리수
        self.doubleSpinBox_Bar_Alpha_NoSelect.setValue(CFG_Bar_Alpha_Unselected)

        self.doubleSpinBox_Bar_DataLength.setRange(0, 1000) # 최소값 ~ 최대값
        self.doubleSpinBox_Bar_DataLength.setSingleStep(1) # 한 스텝 변화
        self.doubleSpinBox_Bar_DataLength.setDecimals(0) # 소수점 아래 표시될 자리수
        self.doubleSpinBox_Bar_DataLength.setValue(CFG_Bar_DataLength)



        self.pushButton_OK.clicked.connect(self.OnBtnClicked_OK)

    def setupUI(self):
        loadUi("qt_designer_dialog_ChartType.ui", self)


    # 다이얼로그 설정값 업데이트
    # main window -> Diaglog     : dlgChartType.__init__(self) 함수에서
    # Diaglog     -> main window : dlgChartType.OnBtnClicked_OK(self) 함수에서
    # (참고) dlgChartType 실행함수 : OnToolbarClick_DlgChartType(self)
    def OnBtnClicked_OK(self):
        global CFG_ChartType
        global CFG_Plot_DrawType
        global CFG_Plot_Alpha_Selected
        global CFG_Plot_Alpha_Unselected
        global CFG_Scatter_Alpha_Selected
        global CFG_Scatter_Alpha_Unselected
        global CFG_Scatter_MarkerSize_Selected
        global CFG_Scatter_MarkerSize_Unselected
        global CFG_Bar_Alpha_Unselected
        global CFG_Bar_ColorGroup
        global CFG_Bar_DataLength

        # if self.radioButton_plot.isChecked():
        #     CFG_ChartType = ChartType_Plot
        # elif self.radioButton_scatter.isChecked():
        #     CFG_ChartType = ChartType_Scatter

        if(self.comboBox_Plot_DrawStyle.currentIndex() == 0):
            CFG_Plot_DrawType = "default"
        elif(self.comboBox_Plot_DrawStyle.currentIndex() == 1):
            CFG_Plot_DrawType = "steps-post"

        if(self.comboBox_Bar_ColorGroup.currentIndex() == 0):
            CFG_Bar_ColorGroup = "none"
        elif(self.comboBox_Bar_ColorGroup.currentIndex() == 1):
            CFG_Bar_ColorGroup = "PSA_Wave"
        elif(self.comboBox_Bar_ColorGroup.currentIndex() == 2):
            CFG_Bar_ColorGroup = "FCA_RU"
        elif(self.comboBox_Bar_ColorGroup.currentIndex() == 3):
            CFG_Bar_ColorGroup = "GM_Bolt"



        CFG_Plot_Alpha_Selected = self.doubleSpinBox_Plot_Alpha_Select.value()
        CFG_Plot_Alpha_Unselected = self.doubleSpinBox_Plot_Alpha_NoSelect.value()
        CFG_Scatter_Alpha_Selected = self.doubleSpinBox_Scatter_Alpha_Select.value()
        CFG_Scatter_Alpha_Unselected = self.doubleSpinBox_Scatter_Alpha_NoSelect.value()
        CFG_Scatter_MarkerSize_Selected = self.doubleSpinBox_Scatter_MarkerSize_Select.value()
        CFG_Scatter_MarkerSize_Unselected = self.doubleSpinBox_Scatter_MarkerSize_NoSelect.value()
        CFG_Bar_Alpha_Unselected = self.doubleSpinBox_Bar_Alpha_NoSelect.value()
        CFG_Bar_DataLength = self.doubleSpinBox_Bar_DataLength.value()


        self.close()











class MatplotlibWidget(QMainWindow):

    def __init__(self):
        
        QMainWindow.__init__(self)


        loadUi("qt_designer_main.ui",self)
        self.setWindowIcon(QIcon('iconPlot.png')) # 맨왼쪽위 아이콘
        self.setWindowTitle("Simple Matplotlib Bar w/ GUI")

        self.MplWidget.canvas.axes_1 = self.MplWidget.canvas.figure.add_subplot(111)
        self.MplWidget.canvas.axes_2 = self.MplWidget.canvas.axes_1.twinx()

        # z-order 변경
        # https://stackoverflow.com/questions/61886791/matplotlib-picker-not-working-with-a-plot-which-has-twiny
        self.MplWidget.canvas.axes_1.set_zorder(self.MplWidget.canvas.axes_2.get_zorder() + 1)
        self.MplWidget.canvas.axes_1.set_frame_on(False)



        # x축 지점이 날짜면 제대로 파싱하기 위해 형을 저장. 
        self.xdata_type = type(0.0) # default로 float로 저장


        # 좌표값
        # (출처) https://stackoverflow.com/questions/21583965/matplotlib-cursor-value-with-two-axes
        def make_format(current, other):
            # current and other are axes
            def format_coord(x, y):
                strRet = ''
                # x, y are data coordinates
                # convert to display coords
                display_coord = current.transData.transform((x, y))
                inv = other.transData.inverted()
                # convert back to data coords with respect to ax
                ax_coord = inv.transform(display_coord)
                coords = [ax_coord, (x, y)]


                # matpltlib 의 date는 "1970-01-01 00:00:00"는 0.0
                #                    "2000-01-01 00:00:00"는 10957.000
                #                    "2100-01-01 00:00:00"는 47482.000 로 표시됨
                if( (self.xdata_type==type(datetime.datetime.now()) ) or (self.xdata_type==type(np.datetime64('2023-03-09'))) ):
                    str_x = mdates.num2date(x).strftime('%Y-%m-%d %H:%M:%S')
                    strRet = ('Left: {1:<40}    Right: {0:<}'.format(*['({}, {:.6f})'.format(str_x, y) for x, y in coords]))
                else:
                    strRet = ('Left: {1:<40}    Right: {0:<}'.format(*['({:.6f}, {:.6f})'.format(x, y) for x, y in coords]))

                return strRet

            return format_coord

        self.MplWidget.canvas.axes_1.format_coord = make_format(self.MplWidget.canvas.axes_1,
                                                                self.MplWidget.canvas.axes_2) # y2이 z-oreder가 높을때



        # 사용자 툴바
        actionOpenFile = QAction(QIcon('iconFile.png'), 'open file', self) # action: open file
        actionOpenFile.setStatusTip("load *.csv file")
        actionOpenFile.triggered.connect(self.OnToolbarClick_OpenFile)

        actionChartType = QAction(QIcon('iconChartTypeOption.png'), 'option', self) # action: graph option
        actionChartType.setStatusTip("matplotlib chart type: plot or scatter")
        actionChartType.triggered.connect(self.OnToolbarClick_DlgChartType)

        self.UserToolbar = self.addToolBar("user toolbar")
        # self.UserToolbar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.UserToolbar.addAction(actionOpenFile)
        self.UserToolbar.addAction(actionChartType)

        # Matplotlib 기본툴바
        self.addToolBar(NavigationToolbar(self.MplWidget.canvas, "matplotlib toolbar", self))


        # 버튼 signal
        self.pushButton_Up.clicked.connect(self.OnBtnClick_Up)
        self.pushButton_Down.clicked.connect(self.OnBtnClick_Down)
        self.pushButton_Plt.clicked.connect(self.OnBtnClick_Plt)

        # 버튼 아이콘 표시하기
        self.pushButton_Up.setIcon(QIcon('iconUp.png'))
        self.pushButton_Down.setIcon(QIcon('iconDown.png'))
        self.pushButton_Plt.setIcon(QIcon('iconPlot.png'))

        # Canvas event handlers
        self.MplWidget.canvas.mpl_connect('button_release_event', self.onMplMouseUp)
        self.MplWidget.canvas.mpl_connect('button_press_event', self.onMplMouseDown)
        self.MplWidget.canvas.mpl_connect('motion_notify_event', self.onMplMouseMotion)
        self.MplWidget.canvas.mpl_connect('pick_event', self.onMplPick)
        self.MplWidget.canvas.mpl_connect('scroll_event', self.onMplWheel)


        # 현재 위치
        self.base_path = os.getcwd()
        self.table_column_clicked = -1

        # List Widget
        #  CSV 파일의 column 이름을 표시
        
        # TableWidget 
        global SPL_lstChkData

        # TableWidget
        self.table.setRowCount( len(SPL_lstChkData) )
        self.table.setColumnCount(5)

        self.table.setHorizontalHeaderLabels(["Name", "X", "Y1", "Y2", "L"])

        for iRow, (dname, iChkPos) in enumerate(SPL_lstChkData):
            # "name"
            self.table.setItem(iRow, 0, QTableWidgetItem(dname))

            for i in range(4):  # X, Y1, Y2, L
                iCol = i + 1
                ChkBox = QCheckBox()
                self.table.setCellWidget(iRow, iCol, ChkBox)
                ChkBox.stateChanged.connect(self.__checkbox_change)  # sender() 확인용 예..

        self.table.horizontalHeaderItem(0).setToolTip("Column Name in CSV")  # header tooltip

        self.table.setColumnWidth(1, 10)
        self.table.setColumnWidth(2, 10)
        self.table.setColumnWidth(3, 10)
        self.table.setColumnWidth(4, 10)

        # 클래스 내 사용하는 변수
        self.lstY1Line = []
        self.lstY2Line = []
        self.dicY1LineToLegend = {}
        self.dicY2LineToLegend = {}
        self.last_artist = None
        self.lstAnnotation = []

    # 다이얼로그 설정값 업데이트
    # main window -> Diaglog     : dlgChartType.__init__(self) 함수에서
    # Diaglog     -> main window : dlgChartType.OnBtnClicked_OK(self) 함수에서
    # (참고) dlgChartType 실행함수 : OnToolbarClick_DlgChartType(self)
    def OnToolbarClick_DlgChartType(self):
        dlg = dlgChartType()
        dlg.exec_()




    # .csv 파일을 open 했을때 수행하는 일
    def OnToolbarClick_OpenFile(self):

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

                df["column_index"] = 0 # default 값, Y 그릴때 생성되는 값
                df["filename"] = strFileName  # 파일이름 생성
                df["file_sequence"] = df.index  # Sequnce를 생성

                if(CFG_Bar_DataLength!=0):
                    iLoadDataLength = min(int(CFG_Bar_DataLength), len(df)) # 읽을 길이를 제한
                    df = df.tail(iLoadDataLength)  # 읽을 길이를 제한

                # Clock 데이터 만듬
                lstColumn = df.columns.tolist()
                if ("Clock" not in lstColumn):
                    if ("작업일" in lstColumn) and (" 작업 시간" in lstColumn):
                        df["Clock"] = df["작업일"] + ' ' + df[" 작업 시간"]

                dfData = pd.DataFrame.copy(df[:])  # hard copy


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

        iColumn = self.table_column_clicked # header column을 클릭했을때
        if (iColumn<1) or (iColumn>4):
            iColumn=2 # default 는 2(Y1)

        # print( SPL_lstChkData )
        for ItemElement in lstItems:
            ItemEntity = ItemElement.text()
            if ItemEntity not in lstColData:
                SPL_lstChkData.append( [ItemEntity, iColumn] )

                if(iColumn==1)or(iColumn==4): # 추가하는 열이 'X' 또는 'L'일 경우 1개만 클릭
                    iAppendRow = len(SPL_lstChkData)-1
                    # 체크박스 클릭시 'X', 'L' 인 경우 다른 행에서도 열위치가 'X'(1), 'L'(4) 인 경우 none(0)으로 바꿈
                    for iRow, (dname, iChkPos) in enumerate(SPL_lstChkData):
                        if (iAppendRow != iRow):
                            if ((SPL_lstChkData[iAppendRow][1] == 1) and (SPL_lstChkData[iRow][1] == 1)):
                                SPL_lstChkData[iRow][1] = 0  # none(0), X(1), Y1(2), Y2(3), L(4)
                            elif ((SPL_lstChkData[iAppendRow][1] == 4) and (SPL_lstChkData[iRow][1] == 4)):
                                SPL_lstChkData[iRow][1] = 0  # none(0), X(1), Y1(2), Y2(3), L(4)


        # print( SPL_lstChkData )

        self.table_column_clicked = -1 # reset

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


    # 체크박스 클릭하면, Global 변수에 저장
    # 체크박스 상태가 클릭에 따라 바뀌나, 특정한 규칙을 적용하기 위해 _UpdateCheckBoxState()를 다시 호출해서 규칙을 적용
    # 체크박스 X(1), Y1(2), Y2(3)의 열 위치가 저장되는 방식이라, 동시에 안 눌려짐
    def __checkbox_change(self, checkvalue):
        global SPL_lstChkData

        lstIdx = self.table.selectedIndexes()
        iClickedRow = -1

        if( len(lstIdx) > 0):
            ckbox = self.table.cellWidget( lstIdx[0].row(), lstIdx[0].column())

            # print(ckbox)
            if isinstance(ckbox, QCheckBox):
                iClickedRow = lstIdx[0].row()
                iClickedCol = lstIdx[0].column()
                if ckbox.isChecked():
                    # print( lstIdx[0].row(), lstIdx[0].column(), " checked")

                    # 1) global 변수 업데이트
                    # 2) global 변수 + 특정 규칙 적용
                    # 3) _UpdateCheckBoxState()를 다시 호출하여 보여지는 체크박스 상태를 바꿈
                    #
                    # SPL_lstChkData[iClickedRow][0] - 신호이름, SPL_lstChkData[iClickedRow][1] - 열번호
                    SPL_lstChkData[iClickedRow][1] = iClickedCol # 체크되는 체크박스의 열번호

                else:
                    # 만일 check 상태에서 클릭한다면
                    if( SPL_lstChkData[iClickedRow][1] == iClickedCol ):
                        SPL_lstChkData[iClickedRow][1] = 0
                    # print( lstIdx[0].row(), lstIdx[0].column(), " no checked")
            else:
                pass
            #    _ = QMessageBox.information(self, 'checkbox', "checkbox 아닙니다.")


        # 체크박스 클릭시 'X', 'L' 인 경우 다른 행에서도 열위치가 'X'(1), 'L'(4) 인 경우 none(0)으로 바꿈
        if( iClickedRow != -1 ):
            for iRow, (dname, iChkPos) in enumerate(SPL_lstChkData):
                if( iClickedRow != iRow ):
                    if( (SPL_lstChkData[iClickedRow][1]==1 ) and (SPL_lstChkData[iRow][1]==1 ) ):
                        SPL_lstChkData[iRow][1] = 0 # none(0), X(1), Y1(2), Y2(3), L(4)
                    elif( (SPL_lstChkData[iClickedRow][1]==4 ) and (SPL_lstChkData[iRow][1]==4 ) ):
                        SPL_lstChkData[iRow][1] = 0 # none(0), X(1), Y1(2), Y2(3), L(4)


            self._UpdateCheckBoxState() # 특정한 규칙을 적용하기 위해 _UpdateCheckBoxState()를 다시 호출

        # end of function


    def _UpdateCheckBoxAll(self):
        global SPL_lstChkData

        # TableWidget
        self.table.clearContents()  # 헤더는 제거 안함.
        self.table.setRowCount( len(SPL_lstChkData) )
        self.table.setColumnCount(5) # ["Name", "X", "Y1", "Y2", "L"]
        self.table.setHorizontalHeaderLabels(["Name", "X", "Y1", "Y2", "L"])

        for iRow, (dname, iChkPos) in enumerate(SPL_lstChkData):
            # "name"
            self.table.setItem(iRow, 0, QTableWidgetItem(dname))

            for iCol in range(1, 5): # X(1), Y1(2), Y2(3), L(4)
                ChkBox = QCheckBox()
                self.table.setCellWidget(iRow, iCol, ChkBox )
                ChkBox.setStyleSheet("text-align: center; margin-left:10%; margin-right:10%;")
                ChkBox.setContentsMargins(0, 0, 0, 0) # left, top, right, bottom
                ChkBox.stateChanged.connect(self.__checkbox_change)  # sender() 확인용 예..

        self.table.horizontalHeaderItem(0).setToolTip("Column Name in CSV") # header tooltip
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
        self.table.cellClicked.connect(self._cellclicked)
        self.table.horizontalHeader().sectionClicked.connect(self._onHeaderClicked)


        self._UpdateCheckBoxState()


    # Global 변수 대로 보여지는 체크박스상태 업데이트
    # 열 위치가 저장되는 방식이라, X, Y1, Y2가 동시에 안 눌려짐
    def _UpdateCheckBoxState(self):
        global SPL_lstChkData

        # Global 변수 대로 상태 업데이트
        for iRow, (dname, iChkPos) in enumerate(SPL_lstChkData):
            for iCol in range( 1, 5 ): # X, Y1, Y2, L
                ckbox = self.table.cellWidget( iRow, iCol )
                if isinstance(ckbox, QCheckBox):
                    if( SPL_lstChkData[iRow][1] == iCol ): # 체크되는 체크박스의 열번호
                        ckbox.setChecked( True )
                    else:
                        ckbox.setChecked( False )
        # end of function



    def _cellclicked(self, row, col):
        pass
        #print("_cellclicked... ", row, col)

    def _onHeaderClicked(self, logicalIndex):
        self.table_column_clicked = logicalIndex




    # DataFrame()의 column 이름이 중복일때 수정하기 위해
    def vFixColumnName(self):
        pass

    def OnBtnClick_Plt(self):

        global SPL_lstChkData
        global SPL_dfData
        global CFG_Bar_ColorGroup
        global CFG_lstGrouping_index

        XAttr = []
        lstY1Attr = []
        lstY2Attr = []
        lstLegAttr = []


        # 각축별로 뭘 그려야 하는지
        for x0, x1 in SPL_lstChkData:

            if( x1 == 1 ): # X axis
                XAttr = x0
            elif( x1 == 2 ): # y1 axis
                lstY1Attr.append( x0 )
            elif( x1 == 3 ): # y2 axis
                lstY2Attr.append( x0 )
            elif( x1 == 4 ): # 'L' column
                lstLegAttr.append( x0 )
            else:
                pass

        lstSelectedItemText = []
        lstSelectedItem = self.table.selectedItems()

        for ItemEntity in lstSelectedItem:
            lstSelectedItemText.append( ItemEntity.text() )
        #print("lstItems", lstSelectedItemText)


        if( len(SPL_dfData) > 0): # DataFrame을 읽어 들였다면

            # 백업을 위한 이전 축 설정 GET, 저장
            #ax1_xmin, ax1_xmax = self.MplWidget.canvas.axes_1.get_xlim()
            #ax1_ymin, ax1_ymax = self.MplWidget.canvas.axes_1.get_ylim()

            ax1_xlabel = self.MplWidget.canvas.axes_1.get_xlabel()
            ax1_ylabel = self.MplWidget.canvas.axes_1.get_ylabel()

            ax2_xlabel = self.MplWidget.canvas.axes_2.get_xlabel()
            ax2_ylabel = self.MplWidget.canvas.axes_2.get_ylabel()


            # 화면 지우기
            self.MplWidget.canvas.axes_1.clear( ) # 화면을 지움
            self.MplWidget.canvas.axes_2.clear( )  # 화면을 지움
            
            # 클래스내 global 변수 초기화
            self.lstY1Line = []  # init
            self.lstY2Line = []  # init
            self.dicY1LineToLegend = {}  # init
            self.dicY2LineToLegend = {}  # init

            # 백업을 위한 이전 축 설정 SET
            if '' != ax1_xlabel:
                self.MplWidget.canvas.axes_1.set_xlabel(ax1_xlabel)
            if '' != ax1_ylabel:
                self.MplWidget.canvas.axes_1.set_ylabel(ax1_ylabel)

            if '' != ax2_xlabel:
                self.MplWidget.canvas.axes_2.set_xlabel(ax2_xlabel)
            if '' != ax2_ylabel:
                self.MplWidget.canvas.axes_2.set_ylabel(ax2_ylabel)


            if( (len(lstY1Attr) > 0) or (len(lstY2Attr) > 0) ): # Y1 에 그릴 데이터가 있다면

                #------------------------------------------------------
                # X축에 그릴 데이터
                #------------------------------------------------------
                if( len(XAttr) > 0 ): # X에 그릴 데이터가 있다면
                    x_data = SPL_dfData[XAttr].to_numpy( )


                    # -------------------------------------------------------------------------------------
                    # 시간으로 변환 (변환에 시간이 오래 걸려, 선택되었을때만 1번 수행
                    lstDateTime, lstTimeStamp = strptime2Timestamp( SPL_dfData[XAttr].values.tolist()  )

                    if( len(lstDateTime) == len(SPL_dfData[XAttr]) ): # 같은 사이즈 만큼 변환하였다면
                        x_data = lstDateTime
                        SPL_dfData[XAttr] = lstDateTime # 한번 변환한 것은 다시 변환 안하기 위해


                    # Timestamp 이면.
                    # UTC Timestamp 는 1970-01-01 00h00m00s 를 기준으로 초단위로 환산한 숫자
                    if(     ("float" in str(type(x_data[0])) ) # float 형이면 \
                        and (x_data[0] > 1600000000) \
                        and (x_data[-1] < 1900000000) \
                        and ("ime" in XAttr) ):

                        lstDateTime = Timestamp2DateTime( SPL_dfData[XAttr].values.tolist() )
                        x_data = lstDateTime
                        SPL_dfData[XAttr] = lstDateTime  # 한번 변환한 것은 다시 변환 안하기 위해
                    # -------------------------------------------------------------------------------------


                else:
                    if (len(lstY1Attr) > 0):  # Y1 에 그릴 데이터가 있다면
                        x_data = np.arange( len( SPL_dfData[lstY1Attr[0]] ) ) # X 를 선택안했을 경우를 대비해서 X 축 데이터 만듦
                    elif (len(lstY2Attr) > 0):  # Y2 에 그릴 데이터가 있다면
                        x_data = np.arange( len( SPL_dfData[lstY2Attr[0]] ) ) # X 를 선택안했을 경우를 대비해서 X 축 데이터 만듦
                
                # 날짜면 제대로 파싱하기 위해
                self.xdata_type = type(x_data[0])






                
                # 색의 출처 : https://matplotlib.org/stable/users/prev_whats_new/dflt_style_changes.html
                colorsY1 = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'
                          , '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
                colorsY2 = ["red", "orange", "yellow", "green", "blue", "indigo", "violet"]



                #
                #                        CG 1 Volt, CG 2 Volt, CG 3 Volt, ...
                # ----------------------------------------------------------------------
                # lstLabel_raw_fromY   : CG 1 Volt, CG 2 Volt, CG 3 Volt,  ...
                # strLabel_text_fromY1 : CG Volt
                # lstLabelX_num_from_Y :    1     ,    2     ,    3     , ...

                lstLabel_raw_fromY1 = []
                strLabel_text_fromY1 = ""
                lstLabelX_num_from_Y1 = []
                if (len(lstY1Attr) > 0):  # Y1에 그릴 데이터가 있다면
                    strLabel_text_fromY1 = " ".join(re.findall('[a-zA-Z]+', lstY1Attr[0]))
                    strLabel_text_Length = len(strLabel_text_fromY1)
                    for Y1Attr in lstY1Attr:
                        lstLabel_raw_fromY1.append( Y1Attr )

                        # 문자열 찾음
                        lstText = re.findall('[a-zA-Z]+', Y1Attr) # text 를 찾음
                        strTextJoin = " ".join(lstText)  # 찾은 text 문자열을 공백있게 합치기
                        # 공통인 문잘열을 찾음
                        strLabel_text_fromY1 = max(get_str_array(strTextJoin) & get_str_array(strLabel_text_fromY1), key=len)

                        # X축으로 쓸 숫자를 찾음
                        lstNumber = re.findall('\d+', Y1Attr)
                        if (len(lstNumber)>0) and (len(strLabel_text_fromY1)>strLabel_text_Length/2):
                            lstLabelX_num_from_Y1.append(int(lstNumber[-1]))  # 숫자는 맨 뒤의 숫자를 씀
                        else:
                            lstLabelX_num_from_Y1.append(-1) # 숫자가 없을 시 '-1'

                lstLabel_raw_fromY2 = []
                strLabel_text_fromY2 = ""
                lstLabelX_num_from_Y2 = []
                if (len(lstY2Attr) > 0):  # Y2에 그릴 데이터가 있다면
                    strLabel_text_fromY2 = " ".join(re.findall('[a-zA-Z]+', lstY2Attr[0]))
                    strLabel_text_Length = len(strLabel_text_fromY2)
                    for Y2Attr in lstY2Attr:
                        lstLabel_raw_fromY2.append( Y2Attr )
                        
                        # 문자열 찾음
                        lstText = re.findall('[a-zA-Z]+', Y2Attr)
                        strTextJoin = " ".join(lstText)  # 리스트 안 문자열를 공백있게 합치기
                        # 공통인 문잘열을 찾음
                        strLabel_text_fromY2 = max(get_str_array(strTextJoin) & get_str_array(strLabel_text_fromY2), key=len)

                        # X축으로 쓸 숫자를 찾음
                        lstNumber = re.findall('\d+', Y2Attr)
                        if (len(lstNumber) > 0) and (len(strLabel_text_fromY2) > strLabel_text_Length / 2):
                            lstLabelX_num_from_Y2.append(int(lstNumber[-1]))  # 숫자는 맨 뒤의 숫자를 씀
                        else:
                            lstLabelX_num_from_Y2.append(-1) # 숫자가 없을 시 '-1'



                # 신호명에 number 가 없을 때
                #     x : 신호명 (raw)
                #     y : 신호값
                #     c : 신호마다 다른 색
                #     L : 미표시
                # 신호명에 number 가 있을 때
                #     x : number (num)
                #     y : 신호값
                #     c : 그룹컬러, Y1/Y2 2color, 신호마다 다른 색

                # lstLabelX
                lstLabelX = []
                width_Y1 = 0.5
                width_Y2 = 0.5
                offset_Y1 = 0
                offset_Y2 = 0
                x_data_all = np.arange(1)

                if( -1 in lstLabelX_num_from_Y1 ) or ( -1 in lstLabelX_num_from_Y2 ): # 신호명에 number가 없을때
                    lstLabelX = lstLabel_raw_fromY1 + lstLabel_raw_fromY2
                    lstLabelX.sort()
                    x_data_all = np.arange(len(lstLabelX))

                    if (len(lstY1Attr)>0):
                        x_data = np.searchsorted(lstLabelX, lstY1Attr)  # (source, search) -> index
                        y_data = SPL_dfData[lstY1Attr].to_numpy()
                        iLength = len(y_data) # column 데이터 길이
                        lstColor = [colorsY1[x % len(colorsY1)] for x in x_data]
                        if (len(lstY2Attr) > 0):
                            lstColor=colorsY1[0]
                        for row in range(iLength):  #
                            self.MplWidget.canvas.axes_1.bar(
                                x_data+offset_Y1,
                                y_data[row],
                                alpha=CFG_Bar_Alpha_Unselected,
                                width=width_Y1,
                                color=lstColor)

                    if (len(lstY2Attr)>0):
                        x_data = np.searchsorted(lstLabelX, lstY2Attr)  # (source, search) -> index
                        y_data = SPL_dfData[lstY2Attr].to_numpy()
                        iLength = len(y_data) # column 데이터 길이
                        lstColor = [colorsY2[x % len(colorsY2)] for x in x_data]
                        if (len(lstY1Attr) > 0):
                            lstColor=colorsY2[0]
                        for row in range(iLength):  #
                            self.MplWidget.canvas.axes_2.bar(
                                x_data+offset_Y2,
                                y_data[row],
                                alpha=CFG_Bar_Alpha_Unselected,
                                width=width_Y2,
                                color=lstColor)

                else:
                    # X축을 번호로
                    lstLabelX = copy.deepcopy(lstLabelX_num_from_Y1)
                    if (len(lstLabelX_num_from_Y1) > 0) and (len(lstLabelX_num_from_Y2) > 0):
                        for LabelX in lstLabelX_num_from_Y2:
                            if LabelX not in lstLabelX:
                                lstLabelX.append(LabelX)
                        lstLabelX.sort()
                        width_Y1 = 0.4
                        width_Y2 = 0.4
                        offset_Y1 = -0.2
                        offset_Y2 = 0.2
                    elif (len(lstLabelX_num_from_Y1) > 0):
                        lstLabelX = sorted(lstLabelX_num_from_Y1)
                    elif (len(lstLabelX_num_from_Y2) > 0):
                        lstLabelX = sorted(lstLabelX_num_from_Y2)

                    x_data = np.searchsorted(lstLabelX, lstLabelX_num_from_Y1)  # (source, search) -> index
                    y_data = SPL_dfData[lstY1Attr].to_numpy()
                    iLength = len(y_data)  # column 데이터 길이

                    # lstLabelX_num_from_Y1 순서가 정렬되지 않은 경우가 있음
                    x_data_sort, x_data_index = zip(*sorted(zip(x_data, list(range(len(x_data))))))
                    x_data_sort = list(x_data_sort) # tuple -> list
                    x_data_index = np.asarray(x_data_index) # tuple -> numpy


                    if (len(lstLabelX_num_from_Y1) > 0):

                        if (CFG_Bar_ColorGroup == "PSA_Wave"):
                            if (len(x_data) > 84):
                                CFG_lstGrouping_index = CFG_lstGrouping_index_PSA7Module
                            else:
                                CFG_lstGrouping_index = CFG_lstGrouping_index_PSA6Module
                        elif (CFG_Bar_ColorGroup == "FCA_RU"):
                            CFG_lstGrouping_index = CFG_lstGrouping_index_FcaRu
                        elif (CFG_Bar_ColorGroup == "GM_Bolt"):
                            CFG_lstGrouping_index = CFG_lstGrouping_index_GmBolt
                        else:
                            CFG_lstGrouping_index = [
                                # text   Cell index ( not Cell No)
                                ["none", [999]],
                            ]

                        lstColorGroupIndex = [item for sublist in CFG_lstGrouping_index for item in sublist[1]]
                        lstColorGroupLegend = [x[0] for x in CFG_lstGrouping_index]

                        if ( x_data_sort == lstColorGroupIndex ):  # Grouping 설정의 갯수와 같다면

                            for row in range(iLength):  #
                                for g, Grouping in enumerate(CFG_lstGrouping_index):  # 모듈별로 나누기
                                    self.MplWidget.canvas.axes_1.bar(
                                        x_data[x_data_index[Grouping[1]]] + offset_Y1,
                                        y_data[row][x_data_index[Grouping[1]]],
                                        alpha=CFG_Bar_Alpha_Unselected,
                                        width=width_Y1,
                                        color=colorsY1[g % len(colorsY1)])
                                if (row == 0):
                                    self.MplWidget.canvas.axes_1.legend(lstColorGroupLegend)
                        else:
                            lstColor = [ colorsY1[x%len(colorsY1)] for x in x_data ]
                            if (len(lstLabelX_num_from_Y2) > 0):
                                lstColor = colorsY1[0]
                            for row in range(iLength):  #
                                self.MplWidget.canvas.axes_1.bar(
                                    x_data + offset_Y1,
                                    y_data[row],
                                    alpha=CFG_Bar_Alpha_Unselected,
                                    width=width_Y1,
                                    color=lstColor)


                    if (len(lstLabelX_num_from_Y2) > 0):
                        x_data = np.searchsorted(lstLabelX, lstLabelX_num_from_Y2)  # (source, search) -> index
                        y_data = SPL_dfData[lstY2Attr].to_numpy()
                        iLength = len(y_data) # column 데이터 길이
                        lstColor = [colorsY2[x % len(colorsY2)] for x in x_data]
                        if (len(lstLabelX_num_from_Y1) > 0):
                            lstColor = colorsY2[0]
                        for row in range(iLength):  #
                            self.MplWidget.canvas.axes_2.bar(
                                x_data+offset_Y2,
                                y_data[row],
                                alpha=CFG_Bar_Alpha_Unselected,
                                width=width_Y2,
                                color=lstColor)

                    x_data_all = np.arange(len(lstLabelX))







                # ------------------------------------------------------
                # X축이름, Y축이름, Title
                # ------------------------------------------------------

                if (len(lstY2Attr) > 0):  # Y2 에 그릴 데이터가 있다면
                    if (len(lstY1Attr) > 0):  # Y1, Y2 표시하였다면
                        self.MplWidget.canvas.axes_2.get_yaxis().set_visible(True)  # 데이터가 있으면 Y2 축 보이기
                    else:
                        self.MplWidget.canvas.axes_2.get_yaxis().set_visible(True)  # 데이터가 있으면 Y2 축 보이기

                else:
                    # 데이터 없으면 우측 Y2 숨기기
                    self.MplWidget.canvas.axes_2.get_yaxis().set_visible(False)  # 데이터가 없으면 Y2 축 숨기기


                self.MplWidget.canvas.axes_1.grid(True)
                self.MplWidget.canvas.axes_1.set_title( SPL_strFileName )
                #self.MplWidget.canvas.axes_1.title.set_size(20)

                if( -1 in lstLabelX_num_from_Y1 ) or ( -1 in lstLabelX_num_from_Y2 ): # 신호명에 number가 없을때
                    if( len(x_data_all)>20 ):
                        self.MplWidget.canvas.axes_1.set_xticks(
                            [x for x in x_data_all if np.where(x_data_all==x)[0] % 2 == 0],
                            [x for x in lstLabelX if lstLabelX.index(x) % 2 == 0],  # 2 간격으로 x tick 표시
                            rotation='vertical' )
                    elif( len(x_data_all)>10 ):
                        self.MplWidget.canvas.axes_1.set_xticks( x_data_all, lstLabelX, rotation=45 ) # 회전
                    else:
                        self.MplWidget.canvas.axes_1.set_xticks( x_data_all, lstLabelX ) # 그대로

                else:
                    if( len(x_data_all)>20 ):
                        self.MplWidget.canvas.axes_1.set_xticks(
                            [x for x in x_data_all if np.where(x_data_all==x)[0] % 2 == 0],
                            [x for x in lstLabelX if lstLabelX.index(x) % 2 == 0])  # 2 간격으로 x tick 표시
                    else:
                        self.MplWidget.canvas.axes_1.set_xticks( x_data_all, lstLabelX )

                # self.MplWidget.canvas.axes_1.set_xlabel(lstLabelX) # 1개만 들어올것임



                if (len(lstY1Attr) > 0):  # Y1에 그릴 데이터가 있다면
                    self.MplWidget.canvas.axes_1.set_ylabel(strLabel_text_fromY1)

                if (len(lstY2Attr) > 0):  # Y1에 그릴 데이터가 있다면
                    self.MplWidget.canvas.axes_2.set_ylabel(strLabel_text_fromY2)
                    # self.MplWidget.canvas.axes_2.legend(strLabel_text_fromY2)







                # ------------------------------------------------------
                # 화면에 그리기
                # ------------------------------------------------------
                try:
                    # plot
                    self.MplWidget.canvas.draw()
                except Exception as e:
                    print(e)
                    _ = QMessageBox.information(self, e)



    def onMplMouseUp(self, event):
        """
        Mouse button up callback
        """
        # 마우스 UP시 마지막 클릭 정보 지움 
        self.last_artist = None
        pass



    def onMplMouseDown(self, event):
        """
        Mouse button down callback
        """
        pass



    def onMplMouseMotion(self, event):
        """
        Mouse motion callback
        """
        pass



    def onMplPick(self, event):
        """
        Mouse pick callback
        """

        pass



    def onMplWheel(self, event):
        """
        Mouse wheel scroll callback
        """
        pass





app = QApplication([])
window = MatplotlibWidget()
window.show()
app.exec_()

















