# ------------------------------------------------------
# ---------------------- main.py -----------------------
# ------------------------------------------------------
from PyQt5.QtWidgets import (QApplication, QInputDialog, QMainWindow, QMessageBox, QFileDialog, QTableWidgetItem,
                             QCheckBox, QDialog, QAction, QWidget, QLabel, QFrame, QPushButton)
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt, QAbstractTableModel

from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
import matplotlib.backends.qt_editor.figureoptions as figureoptions
# from matplotlib import cm # colormap
import matplotlib.dates as mdates
import matplotlib.patches as patches
from matplotlib.lines import Line2D
import matplotlib.transforms as transforms
from matplotlib import colors

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
CFG_Legend_Max = 20
CFG_Legend_MaxMax = 600
CFG_Plot_DrawType = "steps-post"
CFG_Plot_Alpha_Selected = 1.0
CFG_Plot_Alpha_Unselected = 0.8
CFG_Plot_markersize = 6
CFG_Plot_linewidth = 0.8
CFG_Scatter_Alpha_Selected = 0.8
CFG_Scatter_Alpha_Unselected = 0.6
CFG_Scatter_MarkerSize_Selected = 20
CFG_Scatter_MarkerSize_Unselected = 1
CFG_Scatter_ColumnIndex_xdata_order = "sequence"
CFG_Bar_ColorGroup = "PSA_Wave"
CFG_Bar_Alpha_Selected = 0.8
CFG_Bar_Alpha_Unselected = 0.2
CFG_Bar_DataLength = 10
CFG_Common_preset_auto_save = 1
COMMON_PICKMODE_LEGEND = 1
COMMON_PICKMODE_POINTRULER = 2
CFG_Common_PickMode = COMMON_PICKMODE_LEGEND # legend:1, point ruler:2
CFG_Common_drop_duplicates = True
CFG_Common_show_legends = True


# Global variables
SPL_dfData = pd.DataFrame()
#                          신호명         체크되는열(신호당 1개의 체크박스만 클릭가능함)
#                                        0:none, 1:첫번째(X), 2:두번째(Y1), ...
SPL_lstChkData = [] # ["  signal name  ", 0]
SPL_strFileName = ""

SPL_boForceDraw = False # 화면을 강제 업댓




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

CFG_lstGrouping_index_AUDI_BEV = [
    # text        Cell index ( not Cell No)
    ["slave_01", [ 0,  1,  2,  3,  4,  5,  6,  7,  8]],
    ["slave_02", [ 9, 10, 11, 12, 13, 14, 15, 16, 17]],
    ["slave_03", [18, 19, 20, 21, 22, 23, 24, 25, 26]],
    ["slave_04", [27, 28, 29, 30, 31, 32, 33, 34, 35]],
    ["slave_05", [36, 37, 38, 39, 40, 41, 42, 43, 44]],
    ["slave_06", [45, 46, 47, 48, 49, 50, 51, 52, 53]],
    ["slave_07", [54, 55, 56, 57, 58, 59, 60, 61, 62]],
    ["slave_08", [63, 64, 65, 66, 67, 68, 69, 70, 71]],
    ["slave_09", [72, 73, 74, 75, 76, 77, 78, 79, 80]],
    ["slave_10", [81, 82, 83, 84, 85, 86, 87, 88, 89]],
    ["slave_11", [90, 91, 92, 93, 94, 95, 96, 97, 98]],
    ["slave_12", [99,100,101,102,103,104,105,106,107]],
]




CFG_lstGrouping_index  = CFG_lstGrouping_index_PSA7Module



# matplotlib *.png size conversion
iDelta_width_screen_png = -353 # screen to png
iDelta_height_screen_png = -104 # screen to png
iDelta_width_command_screen = 2 # command to screen
iDelta_height_command_screen = 32 # command to screen


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
    if ( (isinstance(lstStrTime[0], str) == True) or (isinstance(lstStrTime[0], np.string_) == True) ): # str 형이면

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

        elif( len(lstStrTime[0]) > 7 ): # 과거 특정입력데이터의 이상 현상 반창고
            '''
            "2022-04-26"
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
             '''
            if (   ( (lstStrTime[0][4] == '-') and (lstStrTime[0][7] == '-') )
                or ( (lstStrTime[0][4] == '-') and (lstStrTime[0][6] == '-') ) ):

                for strTime in lstStrTime:
                    try:
                        # 라이브러리를 이용한 변환
                        dateTimeOne = GetDatetime(strTime)

                        lstDateTime.append(dateTimeOne)
                        timestampOne = datetime.datetime.timestamp(dateTimeOne)
                        lstTimeStamp.append(timestampOne)
                    except:  # 변환에 에러 발생시
                        # print( strTime )
                        pass



    return lstDateTime, lstTimeStamp



#
# Diaglog 창의 이름을  "Y1 axis customize", "Y2 axis customize" 으로 바꾸기 위해
#


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

edit_parameters = NavigationToolbar.edit_parameters # 이전값 저장
NavigationToolbar.edit_parameters = my_edit_parameters # 새로운 함수로 대체


# 두문자의 공통부분을 찾기 위한 함수
def get_str_array(s):
    return {s[i:j] for i in range(len(s)) for j in range(i, len(s) + 1)}


def saveList(myList, filename):
    # (출처) https://stackoverflow.com/questions/27745500/how-to-save-a-list-to-a-file-and-read-it-as-a-list-type
    # the filename should mention the extension 'npy'
    np.save(filename, myList)
    # print("Saved successfully!")

def loadList(filename):
    # the filename should mention the extension 'npy'
    tempNumpyArray = np.load(filename)
    return tempNumpyArray.tolist()



class dlgChartType(QDialog):


    def __init__(self):
        global CFG_ChartType
        global CFG_Plot_DrawType
        global CFG_Plot_Alpha_Selected
        global CFG_Plot_Alpha_Unselected
        global CFG_Plot_markersize
        global CFG_Plot_linewidth
        global CFG_Scatter_Alpha_Selected
        global CFG_Scatter_Alpha_Unselected
        global CFG_Scatter_MarkerSize_Selected
        global CFG_Scatter_MarkerSize_Unselected
        global CFG_Scatter_ColumnIndex_xdata_order
        global CFG_Bar_Alpha_Selected
        global CFG_Bar_Alpha_Unselected
        global CFG_Bar_ColorGroup
        global CFG_Bar_DataLength
        global CFG_Common_PickMode

        super().__init__()
        self.setupUI()
        self.setWindowIcon(QIcon('iconChartTypeOption.png')) # 맨왼쪽위 아이콘
        self.setWindowTitle("Chart type setting")

        # widget의 초기값
        if(CFG_ChartType == ChartType_Plot):
            self.radioButton_plot.setChecked(True)
            self.radioButton_scatter.setChecked(False)
            self.radioButton_bar.setChecked(False)
        elif(CFG_ChartType == ChartType_Scatter):
            self.radioButton_plot.setChecked(False)
            self.radioButton_scatter.setChecked(True)
            self.radioButton_bar.setChecked(False)
        elif(CFG_ChartType == ChartType_Bar):
            self.radioButton_plot.setChecked(False)
            self.radioButton_scatter.setChecked(False)
            self.radioButton_bar.setChecked(True)

        # set focus
        self.tabWidget.setCurrentWidget(self.tabWidget.findChild(QWidget, "tab_bar"))

        # stopping check box to get checked
        self.radioButton_plot.setCheckable(False)
        self.radioButton_scatter.setCheckable(False)
        self.radioButton_bar.setCheckable(True)


        self.comboBox_Plot_DrawStyle.addItem("default")
        self.comboBox_Plot_DrawStyle.addItem("steps-post")
        self.comboBox_Plot_DrawStyle.addItem("steps-mid")
        self.comboBox_Plot_DrawStyle.addItem("steps-pre")
        if( CFG_Plot_DrawType=="default"):
            self.comboBox_Plot_DrawStyle.setCurrentIndex(0)
        elif (CFG_Plot_DrawType == "steps-post"):
            self.comboBox_Plot_DrawStyle.setCurrentIndex(1)
        elif( CFG_Plot_DrawType=="steps-mid"):
            self.comboBox_Plot_DrawStyle.setCurrentIndex(2)
        elif( CFG_Plot_DrawType=="steps-pre"):
            self.comboBox_Plot_DrawStyle.setCurrentIndex(3)



        self.comboBox_Scatter_ColumnIndex_xdata_order.addItem("sequence")
        self.comboBox_Scatter_ColumnIndex_xdata_order.addItem("random")
        if( CFG_Scatter_ColumnIndex_xdata_order =="sequence"):
            self.comboBox_Scatter_ColumnIndex_xdata_order.setCurrentIndex(0)
        elif( CFG_Scatter_ColumnIndex_xdata_order =="random"):
            self.comboBox_Scatter_ColumnIndex_xdata_order.setCurrentIndex(1)

        self.comboBox_Bar_ColorGroup.addItem("none")
        self.comboBox_Bar_ColorGroup.addItem("PSA_Wave")
        self.comboBox_Bar_ColorGroup.addItem("FCA_RU, Volvo")
        self.comboBox_Bar_ColorGroup.addItem("GM_Bolt")
        self.comboBox_Bar_ColorGroup.addItem("AUDI_BEV") 
       
        if( CFG_Bar_ColorGroup=="none"):
            self.comboBox_Bar_ColorGroup.setCurrentIndex(0)
        elif( CFG_Bar_ColorGroup=="PSA_Wave"):
            self.comboBox_Bar_ColorGroup.setCurrentIndex(1)
        elif( CFG_Bar_ColorGroup=="FCA_RU, Volvo"):
            self.comboBox_Bar_ColorGroup.setCurrentIndex(2)
        elif( CFG_Bar_ColorGroup=="GM_Bolt"):
            self.comboBox_Bar_ColorGroup.setCurrentIndex(3)
        elif( CFG_Bar_ColorGroup=="AUDI_BEV"):
            self.comboBox_Bar_ColorGroup.setCurrentIndex(4)

        self.checkBox_preset_auto_save.setTristate( False )
        if( CFG_Common_preset_auto_save == 1 ):
            self.checkBox_preset_auto_save.setCheckState( 2 )
        else:
            self.checkBox_preset_auto_save.setCheckState( 0 )

        self.checkBox_drop_duplicates.setTristate( False )
        if( CFG_Common_drop_duplicates == 1 ):
            self.checkBox_drop_duplicates.setCheckState( 2 )
        else:
            self.checkBox_drop_duplicates.setCheckState( 0 )

        self.checkBox_show_legends.setTristate( False )
        if( CFG_Common_show_legends == 1 ):
            self.checkBox_show_legends.setCheckState( 2 )
        else:
            self.checkBox_show_legends.setCheckState( 0 )


        self.doubleSpinBox_Plot_Alpha_Select.setRange(0, 1) # 최소값 ~ 최대값
        self.doubleSpinBox_Plot_Alpha_Select.setSingleStep(0.1) # 한 스텝 변화
        self.doubleSpinBox_Plot_Alpha_Select.setDecimals(3) # 소수점 아래 표시될 자리수
        self.doubleSpinBox_Plot_Alpha_Select.setValue(CFG_Plot_Alpha_Selected)
        self.doubleSpinBox_Plot_Alpha_NoSelect.setRange(0, 1) # 최소값 ~ 최대값
        self.doubleSpinBox_Plot_Alpha_NoSelect.setSingleStep(0.1) # 한 스텝 변화
        self.doubleSpinBox_Plot_Alpha_NoSelect.setDecimals(3) # 소수점 아래 표시될 자리수
        self.doubleSpinBox_Plot_Alpha_NoSelect.setValue(CFG_Plot_Alpha_Unselected)

        self.doubleSpinBox_Plot_markersize.setRange(0, 100) # 최소값 ~ 최대값
        self.doubleSpinBox_Plot_markersize.setSingleStep(0.1) # 한 스텝 변화
        self.doubleSpinBox_Plot_markersize.setDecimals(1) # 소수점 아래 표시될 자리수
        self.doubleSpinBox_Plot_markersize.setValue(CFG_Plot_markersize)
        self.doubleSpinBox_Plot_linewidth.setRange(0, 100) # 최소값 ~ 최대값
        self.doubleSpinBox_Plot_linewidth.setSingleStep(0.1) # 한 스텝 변화
        self.doubleSpinBox_Plot_linewidth.setDecimals(1) # 소수점 아래 표시될 자리수
        self.doubleSpinBox_Plot_linewidth.setValue(CFG_Plot_linewidth)

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

        self.doubleSpinBox_Bar_Alpha_Select.setRange(0, 1) # 최소값 ~ 최대값
        self.doubleSpinBox_Bar_Alpha_Select.setSingleStep(0.1) # 한 스텝 변화
        self.doubleSpinBox_Bar_Alpha_Select.setDecimals(3) # 소수점 아래 표시될 자리수
        self.doubleSpinBox_Bar_Alpha_Select.setValue(CFG_Bar_Alpha_Selected)
        self.doubleSpinBox_Bar_Alpha_NoSelect.setRange(0, 1) # 최소값 ~ 최대값
        self.doubleSpinBox_Bar_Alpha_NoSelect.setSingleStep(0.1) # 한 스텝 변화
        self.doubleSpinBox_Bar_Alpha_NoSelect.setDecimals(3) # 소수점 아래 표시될 자리수
        self.doubleSpinBox_Bar_Alpha_NoSelect.setValue(CFG_Bar_Alpha_Unselected)

        self.doubleSpinBox_Bar_DataLength.setRange(0, 1000) # 최소값 ~ 최대값
        self.doubleSpinBox_Bar_DataLength.setSingleStep(1) # 한 스텝 변화
        self.doubleSpinBox_Bar_DataLength.setDecimals(0) # 소수점 아래 표시될 자리수
        self.doubleSpinBox_Bar_DataLength.setValue(CFG_Bar_DataLength)



        # radiao button
        if CFG_Common_PickMode == COMMON_PICKMODE_LEGEND:
            self.rbPick_Legend.setChecked(True)
            self.rbPick_LinePoint.setChecked(False)
        elif CFG_Common_PickMode == COMMON_PICKMODE_POINTRULER:
            self.rbPick_Legend.setChecked(False)
            self.rbPick_LinePoint.setChecked(True)



        self.pushButton_OK.clicked.connect(self.OnBtnClicked_OK)

        # resize disable
        self.setFixedSize(self.size())

    def setupUI(self):
        loadUi("qt_designer_ChartType.ui", self)


    # 다이얼로그 설정값 업데이트
    # main window -> Diaglog     : dlgChartType.__init__(self) 함수에서
    # Diaglog     -> main window : dlgChartType.OnBtnClicked_OK(self) 함수에서
    # (참고) dlgChartType 실행함수 : OnToolbarClick_DlgChartType(self)
    def OnBtnClicked_OK(self):
        global CFG_ChartType
        global CFG_Plot_DrawType
        global CFG_Plot_Alpha_Selected
        global CFG_Plot_Alpha_Unselected
        global CFG_Plot_markersize
        global CFG_Plot_linewidth
        global CFG_Scatter_Alpha_Selected
        global CFG_Scatter_Alpha_Unselected
        global CFG_Scatter_MarkerSize_Selected
        global CFG_Scatter_MarkerSize_Unselected
        global CFG_Scatter_ColumnIndex_xdata_order
        global CFG_Bar_Alpha_Selected
        global CFG_Bar_Alpha_Unselected
        global CFG_Bar_ColorGroup
        global CFG_Bar_DataLength
        global CFG_Common_preset_auto_save
        global CFG_Common_PickMode
        global CFG_Common_drop_duplicates
        global CFG_Common_show_legends
        global SPL_boForceDraw

        # if self.radioButton_plot.isChecked():
        #     CFG_ChartType = ChartType_Plot
        # elif self.radioButton_scatter.isChecked():
        #     CFG_ChartType = ChartType_Scatter

        if(self.comboBox_Plot_DrawStyle.currentIndex() == 0):
            CFG_Plot_DrawType = "default"
        elif(self.comboBox_Plot_DrawStyle.currentIndex() == 1):
            CFG_Plot_DrawType = "steps-post"
        elif(self.comboBox_Plot_DrawStyle.currentIndex() == 2):
            CFG_Plot_DrawType = "steps-mid"
        elif(self.comboBox_Plot_DrawStyle.currentIndex() == 3):
            CFG_Plot_DrawType = "steps-pre"

        if(self.comboBox_Scatter_ColumnIndex_xdata_order.currentIndex() == 0):
            CFG_Scatter_ColumnIndex_xdata_order  = "sequence"
        elif(self.comboBox_Scatter_ColumnIndex_xdata_order.currentIndex() == 1):
            CFG_Scatter_ColumnIndex_xdata_order  = "random"

        if(self.comboBox_Bar_ColorGroup.currentIndex() == 0):
            CFG_Bar_ColorGroup = "none"
        elif(self.comboBox_Bar_ColorGroup.currentIndex() == 1):
            CFG_Bar_ColorGroup = "PSA_Wave"
        elif(self.comboBox_Bar_ColorGroup.currentIndex() == 2):
            CFG_Bar_ColorGroup = "FCA_RU, Volvo"
        elif(self.comboBox_Bar_ColorGroup.currentIndex() == 3):
            CFG_Bar_ColorGroup = "GM_Bolt"
        elif(self.comboBox_Bar_ColorGroup.currentIndex() == 4):
            CFG_Bar_ColorGroup = "AUDI_BEV"

        if( self.checkBox_preset_auto_save.isChecked() ):
            CFG_Common_preset_auto_save = 1
        else:
            CFG_Common_preset_auto_save = 0

        if( self.checkBox_drop_duplicates.isChecked() ):
            CFG_Common_drop_duplicates = 1
        else:
            CFG_Common_drop_duplicates = 0

        if( self.checkBox_show_legends.isChecked() ):
            CFG_Common_show_legends = 1
        else:
            CFG_Common_show_legends = 0

        CFG_Plot_Alpha_Selected = self.doubleSpinBox_Plot_Alpha_Select.value()
        CFG_Plot_Alpha_Unselected = self.doubleSpinBox_Plot_Alpha_NoSelect.value()
        CFG_Plot_markersize = self.doubleSpinBox_Plot_markersize.value()
        CFG_Plot_linewidth = self.doubleSpinBox_Plot_linewidth.value()
        CFG_Scatter_Alpha_Selected = self.doubleSpinBox_Scatter_Alpha_Select.value()
        CFG_Scatter_Alpha_Unselected = self.doubleSpinBox_Scatter_Alpha_NoSelect.value()
        CFG_Scatter_MarkerSize_Selected = self.doubleSpinBox_Scatter_MarkerSize_Select.value()
        CFG_Scatter_MarkerSize_Unselected = self.doubleSpinBox_Scatter_MarkerSize_NoSelect.value()
        CFG_Bar_Alpha_Selected = self.doubleSpinBox_Bar_Alpha_Select.value()
        CFG_Bar_Alpha_Unselected = self.doubleSpinBox_Bar_Alpha_NoSelect.value()
        CFG_Bar_DataLength = self.doubleSpinBox_Bar_DataLength.value()

        if self.rbPick_Legend.isChecked():
            if( CFG_Common_PickMode != COMMON_PICKMODE_LEGEND ):
                CFG_Common_PickMode = COMMON_PICKMODE_LEGEND
                SPL_boForceDraw = True
        elif self.rbPick_LinePoint.isChecked():
            if( CFG_Common_PickMode != COMMON_PICKMODE_POINTRULER ):
                CFG_Common_PickMode = COMMON_PICKMODE_POINTRULER
                SPL_boForceDraw = True

        self.close()






# 출처 : https://stackoverflow.com/questions/31475965/fastest-way-to-populate-qtableview-from-pandas-data-frame
class PandasModel(QAbstractTableModel):
    """
    Class to populate a table view with a pandas dataframe
    """
    def __init__(self, data, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self._data = data
        self.SelectColumn = 0

    def rowCount(self, parent=None):
        return len(self._data.values)

    def columnCount(self, parent=None):
        return self._data.columns.size

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row()][index.column()])
        return None

    def headerData(self, col, orientation, role):
        self.SelectColumn = col
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None





class dlgDataFilter(QDialog):
    def __init__(self):

        super().__init__()
        self.setupUI()
        self.setWindowIcon(QIcon('iconDataFilter.png')) # 맨왼쪽위 아이콘
        self.setWindowTitle("input data filter")

        self.model = PandasModel( SPL_dfData.head() ) # dataframe의 상위 몇개만 화면에 표시
        self.tableViewDataFrame.setModel( self.model )

        self.columns = SPL_dfData.head().columns
        self.tableViewDataFrame.horizontalHeader().sectionClicked.connect(self.OnClickHeaderLabel)

        self.pushButton_OK.clicked.connect(self.OnBtnClicked_OK)
        self.pushButton_CANCEL.clicked.connect(self.OnBtnClicked_CANCEL)

        self.lineEdit_FilterEq.setText( r"dfData = dfData[ dfData['ABC']>0 ]" )

        # resize disable
        self.setFixedSize(self.size())

    def OnClickHeaderLabel(self):
        # print( "clicked:", self.columns[self.model.SelectColumn] )
        clipboard.setText( self.columns[self.model.SelectColumn] ) # 클립보드로 신호이름 복사

    def setupUI(self):
        loadUi("qt_designer_DataFilter.ui", self)

    def OnBtnClicked_OK(self):
        global SPL_dfData

        # 명령어를 text로 입력받아 실행시키기
        textFilterEq = self.lineEdit_FilterEq.text()

        boIsValidCommand = False
        if( textFilterEq == r"dfData = dfData[ dfData['ABC']>0 ]" ):
            boIsValidCommand = False
        elif( textFilterEq.startswith("dfData =") ):
            boIsValidCommand = True
            textFilterEq = textFilterEq.replace("dfData =", "")
        elif ( textFilterEq.startswith("dfData=") ):
            boIsValidCommand = True
            textFilterEq = textFilterEq.replace("dfData=", "")

        # (출처) https://chancoding.tistory.com/185
        if boIsValidCommand == True:
            dfData = SPL_dfData
            try:
                dfData = eval(textFilterEq)
                SPL_dfData = dfData
                print( "filter applied:", textFilterEq )
            except Exception as e:
                print("filter equation is wrong!")
                print( e )
        else:
            print("no input data filter!")

        self.close()

    def OnBtnClicked_CANCEL(self):
        self.close()


class dlgWSize(QDialog):
    global iDelta_width_screen_png
    global iDelta_height_screen_png
    global iDelta_width_command_screen
    global iDelta_height_command_screen

    def __init__(self):

        super().__init__()
        self.setupUI()
        self.pushButton_OK.clicked.connect(self.OnBtnClicked_OK)
        # resize disable
        self.setFixedSize(self.size())

        self.lineEdit_width.setText( "{0}".format(window.frameGeometry().width()+iDelta_width_screen_png ))
        self.lineEdit_height.setText( "{0}".format(window.frameGeometry().height()+iDelta_height_screen_png ))

        # widget의 초기값
        self.radioButton_wsize_01.setChecked(False)
        self.radioButton_wsize_02.setChecked(False)
        self.radioButton_wsize_03.setChecked(False)
        self.radioButton_wsize_04.setChecked(False)
        self.radioButton_wsize_manual.setChecked(True)


    def setupUI(self):
        loadUi("qt_designer_WSize.ui", self)

    def OnBtnClicked_OK(self):
        if self.radioButton_wsize_01.isChecked():
            iWidth = 800
            iHeight = 600
        elif self.radioButton_wsize_02.isChecked():
            iWidth = 1280
            iHeight = 720
        elif self.radioButton_wsize_03.isChecked():
            iWidth = 1280
            iHeight = 485
        elif self.radioButton_wsize_04.isChecked():
            iWidth = 1691
            iHeight = 478
        elif self.radioButton_wsize_manual.isChecked():
            iWidth = max( int(self.lineEdit_width.text()), 330)
            iHeight = max( int(self.lineEdit_height.text()), 330)

        try:
            window.resize(iWidth-iDelta_width_screen_png-iDelta_width_command_screen,\
                          iHeight-iDelta_height_screen_png-iDelta_height_command_screen)
        except Exception as e:
            print( e )




        self.close()

    def OnBtnClicked_CANCEL(self):
        self.close()



class MatplotlibWidget(QMainWindow):

    global iDelta_width_screen_png
    global iDelta_height_screen_png
    global iDelta_width_command_screen
    global iDelta_height_command_screen

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
        actionOpenFile = QAction(QIcon('iconFile.png'), 'load *.csv file', self) # action: open file
        actionOpenFile.setStatusTip("load *.csv file")
        actionOpenFile.triggered.connect(self.OnToolbarClick_OpenFile)

        actionDataFilter = QAction(QIcon('iconDataFilter.png'), 'input data filter', self) # action: data filter
        actionDataFilter.setStatusTip("input data filter")
        actionDataFilter.triggered.connect(self.OnToolbarClick_DataFilter)

        actionChartType = QAction(QIcon('iconChartTypeOption.png'), 'matplotlib chart option', self) # action: graph option
        actionChartType.setStatusTip("matplotlib chart option")
        actionChartType.triggered.connect(self.OnToolbarClick_DlgChartType)




        self.UserToolbar = self.addToolBar("user toolbar")
        # self.UserToolbar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.UserToolbar.addAction(actionOpenFile)
        self.UserToolbar.addAction(actionDataFilter)
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
        self.MplWidget.canvas.mpl_connect('key_press_event', self.onMplKeyPress)
        self.MplWidget.canvas.mpl_connect('key_release_event', self.onMplKeyRelease)

        self.MplWidget.canvas.mpl_connect('button_release_event', self.onMplMouseUp)
        self.MplWidget.canvas.mpl_connect('button_press_event', self.onMplMouseDown)
        self.MplWidget.canvas.mpl_connect('motion_notify_event', self.onMplMouseMotion)
        self.MplWidget.canvas.mpl_connect('pick_event', self.onMplPick)
        self.MplWidget.canvas.mpl_connect('scroll_event', self.onMplWheel)


        # status bar
        # (출처) https://stackoverflow.com/questions/57943862/pyqt5-statusbar-separators
        self.Qbutton_window_resize = QPushButton("({0}, {1})".format(self.frameGeometry().width()+iDelta_width_screen_png,
                                                                     self.frameGeometry().height()+iDelta_height_screen_png))
        self.Qbutton_window_resize.setStyleSheet("\
                QPushButton { color:black; border:none; }   \
                QPushButton:checked{ color:red; }\
                QPushButton:hover{ color:red; } ")
        self.Qbutton_window_resize.setToolTip("(figure width, height) : click to change it !")  # tooltip
        self.statusBar().addPermanentWidget(self.Qbutton_window_resize)
        self.Qbutton_window_resize.clicked.connect(self.OnStatusbarClick_DlgWSize)


        # 현재 path
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
        self.last_mouse = "Up"
        self.lstAnnotation = []
        self.shift_is_held = False # shift key event
        self.number_annotation_one_click = 0
        # 클래스 내 사용하는 변수 : Pick
        self.lstLine_object = []
        self.lstPointLabel = []
        self.lstPoint_object = []
        self.currently_dragging = False
        self.current_artist = None
        self.offset = [0, 0]
        self.radius_y = 0.0

        # annotion box color 표시
        fc_box = colors.to_rgba('white')  # facecolor
        ec_box = colors.to_rgba('white')  # edgecolor
        self.fc_box = fc_box[:-1] + (0.7,)  # <--- Change the alpha value of facecolor to be 0.7
        self.ec_box = ec_box[:-1] + (0.7,)  # <--- Change the alpha value of edgecolor to be 0.7


    # 윈도우 사이즈
    def resizeEvent(self, event):
        self.Qbutton_window_resize.setText("({0}, {1})".format(self.frameGeometry().width()+iDelta_width_screen_png,
                                                               self.frameGeometry().height()+iDelta_height_screen_png))
        return super().resizeEvent(event)



    # 다이얼로그 설정값 업데이트
    # main window -> Diaglog     : dlgChartType.__init__(self) 함수에서
    # Diaglog     -> main window : dlgChartType.OnBtnClicked_OK(self) 함수에서
    # (참고) dlgChartType 실행함수 : OnToolbarClick_DlgChartType(self)
    def OnToolbarClick_DlgChartType(self):
        dlg = dlgChartType()
        dlg.exec_()


    def OnToolbarClick_DataFilter(self):
        dlg = dlgDataFilter()
        dlg.exec_()

    def OnStatusbarClick_DlgWSize(self):
        dlg = dlgWSize()
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
            global CFG_Bar_Alpha_Selected
            global CFG_Bar_Alpha_Unselected
            global CFG_Bar_ColorGroup
            global CFG_Bar_DataLength

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

                # Bar 그래프용 
                # 여러파일인 경우 여기서 길이 제한
                # 여러파일을 load 할때는 길이설정 -> 파일load 해야 길이 옵션이 정상 적용됨
                if( (CFG_Bar_DataLength!=0) and len(lstFiles)>1 ):
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


            # Preset 파일 쓰기, 읽기
            preset_file = "xy_preset_list.npy"
            if( os.path.isfile(preset_file) ):
                SPL_lstChkData = []
                lstChkData = loadList(preset_file) # load 시 모두 string으로 인식
                lstColumns = list(SPL_dfData.columns) + ["column_index", "filename", "file_sequence" ]
                # lstChkData 변수 str -> int 업데이트
                for iRow, (dname, iChkPos) in enumerate(lstChkData):
                    if( dname in lstColumns ): # column에 해당 변수이름이 있다면
                        lstChkData[iRow][1] = int(lstChkData[iRow][1])  # 체크되는 체크박스의 열번호, int로 변환
                        SPL_lstChkData.append( lstChkData[iRow] )

                self.table_column_clicked = -1  # reset
                # TableWidget
                self._UpdateCheckBoxAll()



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
        global CFG_Bar_Alpha_Selected
        global CFG_Bar_Alpha_Unselected
        global CFG_Bar_ColorGroup
        global CFG_Bar_DataLength
        global CFG_lstGrouping_index

        XAttr = []
        lstY1Attr = []
        lstY2Attr = []
        lstLegAttr = []

        # 색의 출처 : https://matplotlib.org/stable/users/prev_whats_new/dflt_style_changes.html
        colorsY1 = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
                    '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
        colorsY2 = ["red", "orange", "yellow", "green", "blue", "indigo", "violet"]


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

            # Preset 파일 쓰기, 읽기
            if( CFG_Common_preset_auto_save == 1 ):
                # 다음에 load 하는 파일명으로 마지막 xy 데이터 선택을 저장
                saveList(SPL_lstChkData, "xy_preset_list.npy") #


            # 화면 지우기
            self.MplWidget.canvas.axes_1.clear( ) # 화면을 지움
            self.MplWidget.canvas.axes_2.clear( )  # 화면을 지움
            
            # 클래스내 global 변수 초기화
            self.lstY1Line = []  # init
            self.lstY2Line = []  # init
            self.dicY1LineToLegend = {}  # init
            self.dicY2LineToLegend = {}  # init




            if( (len(lstY1Attr) > 0) or (len(lstY2Attr) > 0) ): # Y1 에 그릴 데이터가 있다면

                #------------------------------------------------------
                # X축에 그릴 데이터 변환 
                #------------------------------------------------------
                # if( len(XAttr) > 0 ): # X에 그릴 데이터가 있다면
                #     x_data = SPL_dfData[XAttr].to_numpy( )
                #
                #     # -------------------------------------------------------------------------------------
                #     # 시간으로 변환 (변환에 시간이 오래 걸려, 선택되었을때만 1번 수행
                #     lstDateTime, lstTimeStamp = strptime2Timestamp( SPL_dfData[XAttr].values.tolist()  )
                #
                #     if( len(lstDateTime) == len(SPL_dfData[XAttr]) ): # 같은 사이즈 만큼 변환하였다면
                #         x_data = lstDateTime
                #         SPL_dfData[XAttr] = lstDateTime # 한번 변환한 것은 다시 변환 안하기 위해
                #
                #
                #     # Timestamp 이면.
                #     # UTC Timestamp 는 1970-01-01 00h00m00s 를 기준으로 초단위로 환산한 숫자
                #     if(     ("float" in str(type(x_data[0])) ) # float 형이면 \
                #         and (x_data[0] > 1600000000) \
                #         and (x_data[-1] < 1900000000) \
                #         and ("ime" in XAttr) ):
                #
                #         lstDateTime = Timestamp2DateTime( SPL_dfData[XAttr].values.tolist() )
                #         x_data = lstDateTime
                #         SPL_dfData[XAttr] = lstDateTime  # 한번 변환한 것은 다시 변환 안하기 위해
                #     # -------------------------------------------------------------------------------------




                #------------------------------------------------------
                # 중복데이터 제거 
                #------------------------------------------------------

                if (CFG_Common_drop_duplicates == True):
                    lstCoumnm_DeleteDuplicate = []
                    if (len(lstY1Attr) > 0):  # Y1 에 그릴 데이터가 있다면
                        lstCoumnm_DeleteDuplicate = lstCoumnm_DeleteDuplicate + lstY1Attr
                    if (len(lstY2Attr) > 0):  # Y2 에 그릴 데이터가 있다면
                        lstCoumnm_DeleteDuplicate = lstCoumnm_DeleteDuplicate + lstY2Attr
                    dfData = SPL_dfData.drop_duplicates(subset=lstCoumnm_DeleteDuplicate)  # 중복줄 제거
                else:
                    dfData = SPL_dfData



                #------------------------------------------------------
                # 길이 제한
                #------------------------------------------------------
                # Bar 그래프용
                if( CFG_Bar_DataLength!=0 ):
                    iLoadDataLength = min(int(CFG_Bar_DataLength), len(dfData)) # 읽을 길이를 제한
                    dfData = dfData.tail(iLoadDataLength)  # 읽을 길이를 제한



                # ---------------------------------------------------------
                # bar 그래프용, x_data 만들기
                # ---------------------------------------------------------

                # 신호명에 number 가 없을 때
                #     x : 신호명 (raw)
                #     y : 신호값
                #     c : 신호마다 다른 색
                #     L : 미표시
                # 신호명에 number 가 있을 때
                #     x : number (num)
                #     y : 신호값
                #     c : 그룹컬러, Y1/Y2 2color, 신호마다 다른 색


                # x_data_raw, x_data_range, dicXdata
                x_data_raw = [] # Axes.set_xticks(x_data_range, labels=x_data_raw)
                x_data_range = [] # 1, 2, 3, ...
                x_data_num = [] # YAttr이 모두 num을 포함하고 있을때
                dicXdata = {} # dictionary, x_data_range[0] = dicXdata[x_data_raw[0]]

                width_Y1 = 0.8
                width_Y2 = 0.8
                dicOffset_Y = {} # y에 따른 x축 offset



                lstColor = [] # color_bar의 리스트. color_bar는 x_data 길이만큼의 list
                lstY1Y2Attr = lstY1Attr+lstY2Attr # color_bar 사용하기 위한

                # 모듈별 컬러표시용
                boColorGroup = False
                dicColor_w_YAttr = {} # YAttr별 셀 color


                # ------------------------------------------------------
                # X축에 그릴 데이터
                # ------------------------------------------------------
                if (len(XAttr) > 0) and (XAttr != "column_index"):  # X에 그릴 데이터가 있다면
                    x_data = dfData[XAttr].to_numpy() # x축 데이터

                    x_data_raw = dfData[XAttr].to_numpy()
                    x_data_raw = np.unique( x_data_raw )
                    x_data_raw = np.sort( x_data_raw ) # 정렬
                    x_data_raw = x_data_raw.tolist() # len() 함수 적용 위해
                    x_data_range = np.arange(1, len(x_data_raw)+1 )
                    x_data_range = x_data_range.tolist()
                    dicXdata = dict(zip(x_data_raw, x_data_range)) # 2ea list -> dict

                    # 이때는 y1, y2 ... 에 포함된 숫자를 구분할 필요 없음
                    # x한칸당 여러개의 bar를 표시가능
                    if ((len(lstY1Attr) > 0) or (len(lstY2Attr) > 0)):
                        width_Y1 = 0.8/len(lstY1Y2Attr)
                        width_Y2 = width_Y1

                        lstOffset_Y = []
                        for i, YAttr in enumerate(lstY1Y2Attr):
                            offset = -0.4+(0.4/len(lstY1Y2Attr))+width_Y1*i
                            lstOffset_Y.append(offset)
                        dicOffset_Y = dict(zip(lstY1Y2Attr, lstOffset_Y)) # 2ea list -> dict

                    # bar 그래프용
                    lstColor = []
                    for YAttr in lstY1Y2Attr:
                        colors_bar = [colorsY1[lstY1Y2Attr.index(YAttr) % len(colorsY1)] for x in x_data]
                        lstColor.append(colors_bar)



                else: # if (len(XAttr) > 0) and (XAttr != "column_index"):  # X에 그릴 데이터가 있다면

                    x_data = lstY1Attr+lstY2Attr  # x축 데이터


                    # y1, y2 ... 에 포함된 숫자를 구분, Y1과 Y2 각각
                    # x한칸당 Y1, Y2 최대 2개 bar 표시 가능

                    #
                    #                        CG 1 Volt, CG 2 Volt, CG 3 Volt, ...
                    # ----------------------------------------------------------------------
                    # lstLabelX_raw_from_Y1  : CG 1 Volt, CG 2 Volt, CG 3 Volt,  ...
                    # strLabelX_text_from_Y1 : CG Volt
                    # lstLabelX_num_from_Y1 :    1     ,    2     ,    3     , ...

                    lstLabelX_raw_from_Y1 = []
                    strLabelX_text_from_Y1 = ""
                    lstLabelX_num_from_Y1 = []

                    lstLabelX_raw_from_Y2 = []
                    strLabelX_text_from_Y2 = ""
                    lstLabelX_num_from_Y2 = []

                    # Y1과 Y2 반복
                    for Y_index, Y_axis in enumerate(["Y1", "Y2"]):

                        lstYAttr = lstY1Attr
                        lstLabelX_raw_from_Y = lstLabelX_raw_from_Y1
                        strLabelX_text_from_Y = strLabelX_text_from_Y1
                        lstLabelX_num_from_Y = lstLabelX_num_from_Y1
                        if( Y_axis=="Y2" ):
                            lstYAttr = lstY2Attr
                            lstLabelX_raw_from_Y = lstLabelX_raw_from_Y2
                            strLabelX_text_from_Y = strLabelX_text_from_Y2
                            lstLabelX_num_from_Y = lstLabelX_num_from_Y2

                        if (len(lstYAttr) > 0):  # Y1에 그릴 데이터가 있다면
                            strLabelX_text_from_Y = " ".join(re.findall('[a-zA-Z]+', lstYAttr[0]))
                            strLabel_text_Length = len(strLabelX_text_from_Y)
                            for YAttr in lstYAttr:
                                lstLabelX_raw_from_Y.append(YAttr)

                                # 문자열 찾음
                                lstText = re.findall('[a-zA-Z]+', YAttr)  # text 를 찾음
                                strTextJoin = " ".join(lstText)  # 찾은 text 문자열을 공백있게 합치기
                                try:
                                    # 공통인 문자열을 찾음
                                    strLabelX_text_from_Y = max(get_str_array(strTextJoin) & get_str_array(strLabelX_text_from_Y), key=len)
                                except Exception as e:
                                    # print("Error |", strFileName_In, "|", e)
                                    strLabelX_text_from_Y = ""

                                # X축으로 쓸 숫자를 찾음
                                lstNumber = re.findall('\d+', YAttr)
                                if (len(lstNumber) > 0) and (len(strLabelX_text_from_Y) > strLabel_text_Length / 2):
                                    lstLabelX_num_from_Y.append(int(lstNumber[-1]))  # 숫자는 맨 뒤의 숫자를 씀
                                else:
                                    lstLabelX_num_from_Y.append("none")  # 숫자가 없을 시 '-1'


                    # x_data_raw, x_data_range, dicXdata
                    if     (XAttr != "column_index")\
                       and ("none" not in lstLabelX_num_from_Y1) \
                       and ("none" not in lstLabelX_num_from_Y2): # y1, y2 모두 숫자로 구성

                        if      ("none" not in lstLabelX_num_from_Y1) \
                            and ("none" not in lstLabelX_num_from_Y2) \
                            and (len(lstY1Attr)>0) \
                            and (len(lstY2Attr)>0) :# y1, y2 모두 숫자로 구성

                            x_data_raw = lstLabelX_raw_from_Y1 + lstLabelX_raw_from_Y2
                            x_data_range = lstLabelX_num_from_Y1 + lstLabelX_num_from_Y2
                            x_data_num = x_data_range
                        elif ("none" not in lstLabelX_num_from_Y1) and (len(lstY2Attr)==0) :  # Y1 숫자로만 채워져 있다면
                            x_data_raw = lstLabelX_raw_from_Y1
                            x_data_range = lstLabelX_num_from_Y1
                            x_data_num = x_data_range
                        elif ("none" not in lstLabelX_num_from_Y2) and (len(lstY1Attr)==0) :  # Y2 숫자로만 채워져 있다면
                            x_data_raw = lstLabelX_raw_from_Y2
                            x_data_range = lstLabelX_num_from_Y2
                            x_data_num = x_data_range

                        dicXdata = dict(zip(x_data_raw, x_data_range))  # 2ea list -> dict
                        dicXdata = {k: v for k, v in sorted(dicXdata.items(), key=lambda item: item[1])} # x_data_range 기준으로 정렬


                    else:
                        if(len(lstY1Attr) > 0) :  # Y1 에 그릴 데이터가 있다면
                            x_data_raw += lstLabelX_raw_from_Y1

                        if (len(lstY2Attr) > 0):  # Y1 에 그릴 데이터가 있다면
                            x_data_raw += lstLabelX_raw_from_Y2

                        x_data_range = np.arange(1,len(x_data_raw)+1)
                        x_data_range = x_data_range.tolist()

                        dicXdata = dict(zip(x_data_raw, x_data_range))  # 2ea list -> dict


                    # bar 그래프 width, off
                    if ((len(lstY1Attr) > 0) and (len(lstY2Attr) > 0)):
                        width_Y1 = 0.4
                        width_Y2 = 0.4
                        lstOffset_Y = []
                        for i, YAttr in enumerate(lstY1Y2Attr):
                            if( YAttr in lstY1Attr ):
                                offset = -0.2
                            else:
                                offset = 0.2
                            lstOffset_Y.append(offset)
                        dicOffset_Y = dict(zip(lstY1Y2Attr, lstOffset_Y)) # 2ea list -> dict
                    elif(len(lstY1Attr) > 0):
                        width_Y1 = 0.8
                        width_Y2 = 0.0
                        lstOffset_Y = []
                        for i, YAttr in enumerate(lstY1Y2Attr):
                            offset = 0
                            lstOffset_Y.append(offset)
                        dicOffset_Y = dict(zip(lstY1Y2Attr, lstOffset_Y)) # 2ea list -> dict
                    elif(len(lstY2Attr) > 0):
                        width_Y1 = 0.0
                        width_Y2 = 0.8
                        lstOffset_Y = []
                        for i, YAttr in enumerate(lstY1Y2Attr):
                            offset = 0
                            lstOffset_Y.append(offset)
                        dicOffset_Y = dict(zip(lstY1Y2Attr, lstOffset_Y)) # 2ea list -> dict



                    # 모듈별 컬러표시용
                    if (CFG_Bar_ColorGroup == "PSA_Wave"):
                        if (len(x_data_range) > 84):
                            CFG_lstGrouping_index = CFG_lstGrouping_index_PSA7Module
                        else:
                            CFG_lstGrouping_index = CFG_lstGrouping_index_PSA6Module
                    elif (CFG_Bar_ColorGroup == "FCA_RU, Volvo"):
                        CFG_lstGrouping_index = CFG_lstGrouping_index_FcaRu
                    elif (CFG_Bar_ColorGroup == "GM_Bolt"):
                        CFG_lstGrouping_index = CFG_lstGrouping_index_GmBolt
                    elif (CFG_Bar_ColorGroup == "AUDI_BEV"):
                        CFG_lstGrouping_index = CFG_lstGrouping_index_AUDI_BEV
                    else:
                        CFG_lstGrouping_index = [
                            # text   Cell index ( not Cell No)
                            ["none", [999]],
                        ]

                    lstCellNoOutOfColorGroup = [cell_index+1 for item in CFG_lstGrouping_index for cell_index in item[1]]
                    lstCellColorOutOfColorGroup = [colorsY1[i%len(colorsY1)] for i, item in enumerate(CFG_lstGrouping_index) for cell_index in item[1]]
                    if( lstCellNoOutOfColorGroup == sorted(x_data_range) ):
                        boColorGroup = True
                        lstX_range_w_YAttr = [dicXdata[YAttr] for YAttr in lstY1Y2Attr]
                        dicColor_w_X_ragne = dict(zip(lstCellNoOutOfColorGroup, lstCellColorOutOfColorGroup))  # 2ea list -> dict
                        lstColor_w_YAttr = []
                        for X_range_w_YAttr in lstX_range_w_YAttr:
                            color_w_YAttr = dicColor_w_X_ragne[X_range_w_YAttr]
                            lstColor_w_YAttr.append(color_w_YAttr)
                        dicColor_w_YAttr = dict(zip(lstY1Y2Attr, lstColor_w_YAttr))  # 2ea list -> dict
















                # 먼저 그릴 lstDrawY_Legend 찾음

                #                                  먼저그림          legend           나머지그림
                # -----------------------------------------------------------------------------------------------------------
                # 'L' 체크 되었을때
                #   legend 표시가 20개 이상 일때
                #     선택된게 있을 때             : 1st 선택된 Ys    many "signal"    나머지 그림
                #     선택된게 없을 때             : 1st Y로         many "signal"    나머지 그림
                #   legend 표시가 20개 이내 일때
                #     선택된게 있을 때             : 1st Y로          legend           나머지 그림
                #     선택된게 없을 때             : 1st Y로          legend           나머지 그림
                # 'L' 체크 안 되었을때
                #   Y축 표시가 20개 이상 일때
                #     선택된게 있을 때             : 선택된 Ys        legend           나머지 그림
                #     선택된게 없을 때             : max5, min5      legend           나머지 그림
                #   Y축 표시가 20개 이내 일때
                #     선택된게 있을 때             : 모든 Ys          legend
                #     선택된게 없을 때             : 모든 Ys          legend


                # Y1과 Y2 반복
                for lstYAttr_Index, lstYAttr in enumerate( [lstY1Attr, lstY2Attr] ):

                    # Y1, Y2 에 따라 변경
                    colorsY = colorsY1
                    matplotlib_axes = self.MplWidget.canvas.axes_1
                    # Global 변수들 for 'pick_event'
                    lstGlobalYLine = self.lstY1Line
                    dicGlobalYLineToLegend = self.dicY1LineToLegend

                    # Bar 그래프용 
                    width_Y = width_Y1

                    # Y1 or Y2 에 따라 변경
                    if( lstYAttr_Index == 1 ): # 현재가 Y1(0)인지 Y2(1)인지에 따라 변경
                        colorsY = colorsY2
                        matplotlib_axes = self.MplWidget.canvas.axes_2
                        lstGlobalYLine = self.lstY2Line
                        dicGlobalYLineToLegend = self.dicY2LineToLegend

                        # Bar 그래프용 
                        width_Y = width_Y2


                    if (len(lstYAttr) > 0):  # Y1 에 그릴 데이터가 있다면

                        # ---------------------------------------------------------------
                        # legend 표시용 그래프 그리기, 먼저 그리는 데이터 사전준비 
                        # ---------------------------------------------------------------
                        lstLegend = []  # Y1 legend 표시 데이터 이름들
                        lstLegendDrawDataPos = []  # Y1 legend 표시 데이터들의 위치 정보
                        lstLegendYValue_unique = []  # Y1 legend 중복 없이.
                        lstDrawY_Legend = []  # legend 표시를 위해 먼저 그릴 Y 들


                        if (len(lstLegAttr) > 0):  # 'L' 에 체크가 되었다면

                            # 'L' 체크 되었을때
                            #   legend 표시가 20개 이상 일때
                            #     선택된게 있을 때             : (1st 선택된 Ys)    many "signal"    나머지 그림
                            #     선택된게 없을 때             : (1st Y로)         many "signal"    나머지 그림
                            #   legend 표시가 20개 이내 일때
                            #     선택된게 있을 때             : (1st Y로)          legend           나머지 그림
                            #     선택된게 없을 때             : (1st Y로)          legend           나머지 그림
                            lstLegendYValue = dfData[lstLegAttr].values.tolist()  # legend들의 데이터
                            lstLegendYValue = [x[0] for x in lstLegendYValue]  # legend들의 데이터
                            lstLegendYValue_unique = list(np.unique(lstLegendYValue, return_counts=False))  # Y1 1개의 legend

                            # lstColor
                            if (len(XAttr) > 0) and (XAttr != "column_index"):  # X에 그릴 데이터가 있다면
                                # bar 그래프용
                                lstColor = []
                                for i in lstLegendYValue:
                                    colors_bar = [colorsY[lstLegendYValue_unique.index(i) % len(colorsY1)] for x in x_data]
                                    lstColor.append(colors_bar)
                            else:
                                # bar 그래프용
                                lstColor = []
                                for i in lstLegendYValue_unique:
                                    colors_bar = colorsY1[lstLegendYValue_unique.index(i) % len(colorsY1)]
                                    lstColor.append(colors_bar)



                            # 먼저 그릴 Y 찾기
                            if (len(lstLegendYValue_unique) > CFG_Legend_Max):
                                for SelectedItemText in lstSelectedItemText:
                                    if SelectedItemText in lstYAttr:
                                        lstDrawY_Legend.append(SelectedItemText)
                                if (len(lstDrawY_Legend) == 0):  # 선택된 중인 Y1 이 없으면, 1st Y
                                    lstDrawY_Legend.append(lstYAttr[0])
                            else:
                                lstDrawY_Legend.append(lstYAttr[0])


                        else: #  if (len(lstLegAttr) > 0):  # 'L' 에 체크가 되었다면
						
                            # 'L' 체크 안 되었을때
                            #   Y축 표시가 20개 이상 일때
                            #     선택된게 있을 때             : (선택된 Ys)        legend           나머지 그림
                            #     선택된게 없을 때             : (max5, min5)      legend           나머지 그림
                            #   Y축 표시가 20개 이내 일때
                            #     선택된게 있을 때             : (모든 Ys)          legend
                            #     선택된게 없을 때             : (모든 Ys)          legend

                            if (len(lstYAttr) > CFG_Legend_Max):

                                for SelectedItemText in lstSelectedItemText:
                                    if SelectedItemText in lstYAttr:
                                        lstDrawY_Legend.append(SelectedItemText)

                                if (len(lstDrawY_Legend) == 0):
                                    '''
                                    # Y에 표시할 값 max 와 min 값 기준으로 정렬
                                    series_Y_max = pd.Series(dfData[lstYAttr].max())
                                    # series_Y_avg = pd.Series(dfData[lstYAttr].mean())
                                    series_Y_min = pd.Series(dfData[lstYAttr].min())
                                    # sorted_desscending = series_Y_avg.sort_values(ascending=False).index
                                    # sorted_ascending = series_Y_avg.sort_values(ascending=True).index
                                    sorted_desscending = series_Y_max.sort_values(ascending=False).index
                                    sorted_ascending = series_Y_min.sort_values(ascending=True).index
            
                                    # Y (max6, min5)
                                    for Y_sorted in sorted_desscending[0:min(6, int(len(sorted_desscending)/2))]: # 큰거 6개
                                        lstDrawY_Legend.append( Y_sorted )
                                    for Y_sorted in reversed(sorted_ascending): # 작은거 5개
                                        if(Y_sorted not in lstDrawY_Legend) and (len(lstDrawY_Legend)<(min(11, len(sorted_desscending)))): # 최대 11개
                                            lstDrawY_Legend.append( Y_sorted )
                                    '''
                                    lstDrawY_Legend = lstYAttr[:6] + lstYAttr[-5:]

                            else:
                                lstDrawY_Legend = lstYAttr


                            # lstColor
                            if (len(XAttr) > 0) and (XAttr != "column_index"):  # X에 그릴 데이터가 있다면
                                # bar 그래프용
                                lstColor = []
                                for i in lstY1Y2Attr:
                                    colors_bar = [colorsY[lstY1Y2Attr.index(i) % len(colorsY1)] for x in x_data]
                                    lstColor.append(colors_bar)
                            else:
                                # bar 그래프용
                                lstColor = []
                                for i in lstY1Y2Attr:
                                    colors_bar = colorsY1[lstY1Y2Attr.index(i) % len(colorsY1)]
                                    lstColor.append(colors_bar)






                        # ------------------------------------------------------
                        # Y축 데이터 그래프 그리기
                        # ------------------------------------------------------

                        for i, YAttr in enumerate(lstYAttr):
                            y_data = dfData[YAttr].to_numpy()

                            # bar 그래프용
                            iLength = min(int(CFG_Bar_DataLength), len(y_data))  # 읽을 길이를 제한 # column 데이터 길이

                            # # -------------------------------------------------------------------------------------
                            # # 시간으로 변환 (변환에 시간이 오래 걸려, 선택되었을때만 1번 수행
                            # lstDateTime, lstTimeStamp = strptime2Timestamp(dfData[YAttr].values.tolist())
                            # if (len(lstDateTime) == len(dfData[YAttr])):  # 같은 사이즈 만큼 변환하였다면
                            #     y_data = lstDateTime
                            #     dfData[YAttr] = lstDateTime  # 한번 변환한 것은 다시 변환 안하기 위해
                            #
                            # # Timestamp 이면.
                            # # UTC Timestamp 는 1970-01-01 00h00m00s 를 기준으로 초단위로 환산한 숫자
                            # if (("float" in str(type(y_data[0])))  # float 형이면 \
                            #         and (y_data[0] > 1300000000) \
                            #         and (y_data[-1] < 1900000000) \
                            #         and ("ime" in YAttr)):
                            #     lstDateTime = Timestamp2DateTime(dfData[YAttr].values.tolist())
                            #     y_data = lstDateTime
                            #     dfData[YAttr] = lstDateTime  # 한번 변환한 것은 다시 변환 안하기 위해
                            #
                            # # -------------------------------------------------------------------------------------

                            # # 셀별로 값 확인하기 위해
                            # if( XAttr == "column_index" ):
                            #     lstColumn = dfData.columns.to_list()
                            #     if( CFG_Scatter_ColumnIndex_xdata_order == "random" ):
                            #         x_data = [ (1+lstColumn.index(YAttr)-lstColumn.index(lstYAttr[0])+random.random()*0.8-0.4) for x in range(len(x_data))]
                            #     else:
                            #         x_data = [(1+lstColumn.index(YAttr)-lstColumn.index(lstYAttr[0])+x*0.8/(len(x_data)-1)-0.4) for x in range(len(x_data))]

                            # lstLegAttr에는 신호이름이 저장됨
                            # lstLegend 에는 'L'체크시 신호이름의 값이 저장되고, 그외는 신호이름이 저장됨
                            if (len(lstLegAttr) > 0):  # 'L' 에 체크가 되었다면

                                if (len(XAttr) > 0) and (XAttr != "column_index"):  # X에 그릴 데이터가 있다면
                                    x_data_disp = x_data
                                    y_data_disp = y_data

                                else:
                                    x_data_disp = [YAttr for y in y_data]
                                    y_data_disp = y_data


                                # 'L' 체크 되었을때
                                #   legend 표시가 20개 이상 일때
                                #     선택된게 있을 때             : (1st 선택된 Ys)    many "signal"    나머지 그림
                                #     선택된게 없을 때             : (1st Y로)         many "signal"    나머지 그림
                                #   legend 표시가 20개 이내 일때
                                #     선택된게 있을 때             : (1st Y로)          legend           나머지 그림
                                #     선택된게 없을 때             : (1st Y로)          legend           나머지 그림

                                if (YAttr in lstDrawY_Legend):

                                    if (len(lstLegendYValue_unique) > CFG_Legend_MaxMax):

                                        # legend 용 value 값들이 너무 많아 위치 데이터 생성이 어려움
                                        if YAttr in lstSelectedItemText:  # 현재 선택되어 있다면
                                            for row in range(len(y_data_disp) - iLength,
                                                             len(y_data_disp) - iLength + 1):  # range(시작, 끝)
                                                matplotlib_axes.bar(
                                                    dicXdata[x_data_disp[0]] + dicOffset_Y[YAttr],
                                                    y_data_disp[row],
                                                    alpha=CFG_Bar_Alpha_Selected,
                                                    width=width_Y,
                                                    color=lstColor_disp[lstY1Y2Attr.index(YAttr) % len(lstColor_disp)],
                                                    label=YAttr)
                                        else:
                                            for row in range(len(y_data_disp) - iLength,
                                                             len(y_data_disp) - iLength + 1):  #
                                                matplotlib_axes.bar(
                                                    dicXdata[x_data_disp[0]] + dicOffset_Y[YAttr],
                                                    y_data_disp[row],
                                                    alpha=CFG_Bar_Alpha_Unselected,
                                                    width=width_Y,
                                                    color=lstColor_disp[lstY1Y2Attr.index(YAttr) % len(lstColor_disp)],
                                                    label=YAttr)


                                    else:

                                        # 첫번째 Legend의 데이터 위치와 그외 데이터로 위치를 분리함
                                        for LegendYValue in lstLegendYValue_unique:  # legend 별 1개 씩 처리함
                                            if (LegendYValue not in lstLegend):  # 이전에 표시하지 않은 legend의 데이터라면.
                                                npLegendDrawDataPos = np.where(np.array(lstLegendYValue) == LegendYValue)[0]
                                                lstLegendDrawDataPos.append(npLegendDrawDataPos)  # legend 그린 후 나머지 그릴때 안 그리려고 저장
                                                lstLegend.append(LegendYValue)  # 표시한 legend에 등록

                                                if YAttr in lstSelectedItemText:  # 현재 선택되어 있다면
                                                    matplotlib_axes.bar(
                                                        dicXdata[x_data_disp[npLegendDrawDataPos[0]]]+dicOffset_Y[YAttr],
                                                        y_data_disp[npLegendDrawDataPos[0]],
                                                        alpha=CFG_Bar_Alpha_Selected,
                                                        width=width_Y,
                                                        color=colorsY[lstLegendYValue_unique.index(LegendYValue) % len(colorsY)],
                                                        label=LegendYValue)
                                                else:
                                                    matplotlib_axes.bar(
                                                        dicXdata[x_data_disp[npLegendDrawDataPos[0]]]+dicOffset_Y[YAttr],
                                                        y_data_disp[npLegendDrawDataPos[0]],
                                                        alpha=CFG_Bar_Alpha_Unselected,
                                                        width=width_Y,
                                                        color=colorsY[lstLegendYValue_unique.index(LegendYValue) % len(colorsY)],
                                                        label=LegendYValue)


                            else: # if (len(lstLegAttr) > 0):  # 'L' 에 체크가 되었다면

                                # 'L' 체크 안 되었을때
                                #   Y축 표시가 20개 이상 일때
                                #     선택된게 있을 때             : (선택된 Ys)        legend           나머지 그림
                                #     선택된게 없을 때             : (max5, min5)      legend           나머지 그림
                                #   Y축 표시가 20개 이내 일때
                                #     선택된게 있을 때             : (모든 Ys)          legend
                                #     선택된게 없을 때             : (모든 Ys)          legend

                                if (YAttr in lstDrawY_Legend):

                                    if (len(lstYAttr) > CFG_Legend_Max):
                                        if YAttr in lstSelectedItemText:  # 선택된게 있을 때
                                            lstLegend.append(YAttr)
                                        else:  # 선택된게 없을 때, (max5, ... ,min5)
                                            if (YAttr == lstDrawY_Legend[5]):
                                                lstLegend.append(". . .")
                                            else:
                                                lstLegend.append(YAttr)
                                    else:  #
                                        lstLegend.append(YAttr)



                                    if (len(XAttr) > 0) and (XAttr != "column_index"):  # X에 그릴 데이터가 있다면
                                        x_data_disp = x_data[len(x_data)-iLength]
                                        y_data_disp = y_data
                                    else:
                                        x_data_disp = x_data[x_data.index(YAttr)]
                                        y_data_disp = y_data

                                    if(boColorGroup==True):
                                        color_w_YAttr = dicColor_w_YAttr[YAttr]
                                    else:
                                        color_w_YAttr = colorsY[lstY1Y2Attr.index(YAttr) % len(colorsY)]


                                    if YAttr in lstSelectedItemText:  # 현재 선택되어 있다면
                                        for row in range(len(y_data_disp)-iLength, len(y_data_disp)-iLength+1):  # range(시작, 끝)
                                            matplotlib_axes.bar(
                                                dicXdata[x_data_disp] + dicOffset_Y[YAttr],
                                                y_data_disp[row],
                                                alpha=CFG_Bar_Alpha_Selected,
                                                width=width_Y,
                                                color=color_w_YAttr,
                                                label=YAttr)
                                    else:
                                        for row in range(len(y_data_disp)-iLength, len(y_data_disp)-iLength+1):  #
                                            matplotlib_axes.bar(
                                                dicXdata[x_data_disp] + dicOffset_Y[YAttr],
                                                y_data_disp[row],
                                                alpha=CFG_Bar_Alpha_Unselected,
                                                width=width_Y,
                                                color=color_w_YAttr,
                                                label=YAttr)























                        # ------------------------------------------------------
                        # Legend 표시
                        # ------------------------------------------------------
                        if( CFG_Common_show_legends == True ):

                            if (len(lstLegAttr) > 0):  # 'L' 에 체크가 되었다면
                                # 'L' 체크 되었을때
                                #   legend 표시가 20개 이상 일때
                                #     선택된게 있을 때             : 1st 선택된 Ys    (many "signal")    나머지 그림
                                #     선택된게 없을 때             : 1st Y로         (many "signal")    나머지 그림
                                #   legend 표시가 20개 이내 일때
                                #     선택된게 있을 때             : 1st Y로          (legend)           나머지 그림
                                #     선택된게 없을 때             : 1st Y로          (legend)           나머지 그림
                                if (len(lstLegendYValue_unique) > CFG_Legend_Max):
                                    Legend = "too many legends"  # 먼저 그릴 Y 찾기

                                    if( lstYAttr_Index == 0 ): # Y1 그릴때
                                        if (len(lstY2Attr) > 0):  # Y2 그릴게 있다면
                                            matplotlib_axes.legend([Legend], loc='upper left')
                                        else:
                                            matplotlib_axes.legend([Legend])
                                    elif( lstYAttr_Index == 1 ): # Y2 그릴때
                                        if (len(lstY2Attr) > 0):  # Y2 그릴게 있다면
                                            matplotlib_axes.legend([Legend], loc='upper right')

                                else:
                                    # 신호이름을 포함한 legend
                                    lstLegend_w_name = []
                                    for legend in lstLegend:
                                        if( (isinstance(legend, str)==True) or (isinstance(legend, np.string_)==True) ):
                                            legend_w_name = legend
                                        else:
                                            legend_w_name = lstLegAttr[0] + " " + str(legend)
                                        lstLegend_w_name.append(legend_w_name)

                                    if (lstYAttr_Index == 0):  # Y1 그릴때
                                        if (len(lstY2Attr) > 0):  # Y1, Y2 그릴때
                                            matplotlib_axes.legend(lstLegend_w_name, loc='upper left')
                                        else:
                                            matplotlib_axes.legend(lstLegend_w_name)
                                    elif( lstYAttr_Index == 1 ): # Y2 그릴때
                                        if (len(lstY2Attr) > 0):  # Y2 그릴게 있다면
                                            matplotlib_axes.legend(lstLegend_w_name, loc='upper right')

                            else:

                                # 'L' 체크 안 되었을때
                                #   Y축 표시가 20개 이상 일때
                                #     선택된게 있을 때             : 선택된 Ys        (legend)           나머지 그림
                                #     선택된게 없을 때             : max5, min5      (legend)           나머지 그림
                                #   Y축 표시가 20개 이내 일때
                                #     선택된게 있을 때             : 모든 Ys          (legend)
                                #     선택된게 없을 때             : 모든 Ys          (legend)

                                if (lstYAttr_Index == 0):  # Y1 그릴때
                                    if (len(lstY2Attr) > 0):  # Y1, Y2 그릴때
                                        matplotlib_axes.legend(lstLegend, loc='upper left')
                                    else:
                                        matplotlib_axes.legend(lstLegend)

                                elif (lstYAttr_Index == 1):  # Y2 그릴때
                                    if (len(lstY2Attr) > 0):  # Y2 그릴게 있다면
                                        matplotlib_axes.legend(lstLegend, loc='upper right')


                        else: #  if( CFG_Common_show_legends == True ):

                            pass


























                        # ------------------------------------------------------
                        # Legend 표시외 그래프 그리기
                        # 나머지 데이터 그리기
                        # ------------------------------------------------------
                        if (len(lstLegAttr) > 0):  # 'L' 에 체크가 되었다면


                            # iProgress = -1
                            for i, YAttr in enumerate(lstYAttr):
                                if (1):  # if YAttr not in lstDrawY_Legend:

                                    # # 셀별로 값 확인하기 위해서
                                    # if (XAttr == "column_index"):
                                    #     lstColumn = dfData.columns.to_list()
                                    #     if (CFG_Scatter_ColumnIndex_xdata_order == "random"):
                                    #         x_data = [(1+lstColumn.index(YAttr)-lstColumn.index(lstYAttr[0])+random.random()*0.8-0.4) for x in range(len(x_data))]
                                    #     else:
                                    #         x_data = [(1+lstColumn.index(YAttr)-lstColumn.index(lstYAttr[0])+ x*0.8/(len(x_data)-1)-0.4) for x in range(len(x_data))]

                                    y_data = dfData[YAttr].to_numpy()

                                    if (len(lstLegendYValue_unique) > CFG_Legend_MaxMax):

                                        # legend 용 value 값들이 너무 많아 위치 데이터 생성이 어려움
                                        if (len(XAttr) > 0) and (XAttr != "column_index"):  # X에 그릴 데이터가 있다면
                                            x_data_disp = x_data  #
                                            y_data_disp = y_data  #
                                            lstColor_disp = [colors_bar for colors_bar in lstColor]
                                        else:
                                            x_data_disp = [x_data[x_data.index(YAttr)] for y in y_data]
                                            y_data_disp = y_data
                                            lstColor_disp = [colors_bar[x_data.index(YAttr)] for colors_bar in lstColor]

                                        if YAttr in lstSelectedItemText:  # 현재 선택되어 있다면
                                            for row in range(len(y_data_disp)-iLength+1, len(y_data_disp)):  #
                                                matplotlib_axes.bar(
                                                    dicXdata[x_data_disp[row]] + dicOffset_Y[YAttr],
                                                    y_data_disp[row],
                                                    alpha=CFG_Bar_Alpha_Selected,
                                                    width=width_Y,
                                                    color=lstColor_disp[lstY1Y2Attr.index(YAttr) % len(lstColor)],
                                                    label=YAttr)
                                        else:
                                            for row in range(len(y_data_disp)-iLength+1, len(y_data_disp)):  #
                                                matplotlib_axes.bar(
                                                    dicXdata[x_data_disp[row]] + dicOffset_Y[YAttr],
                                                    y_data_disp[row],
                                                    alpha=CFG_Bar_Alpha_Unselected,
                                                    width=width_Y,
                                                    color=lstColor_disp[lstY1Y2Attr.index(YAttr) % len(lstColor)],
                                                    label=YAttr)

                                    else:

                                        for j, Legend in enumerate(lstLegendYValue_unique):
                                            lstDataPos = lstLegendDrawDataPos[j]
                                            if(i==0): # legend전에 그린 그래프는 제외
                                                lstDataPos = lstDataPos[1:]

                                            # if(i==0): # legend 이전에 그림
                                            #     lstDataPos = lstLegendDrawDataPos[j][1:]

                                            if (len(XAttr) > 0) and (XAttr != "column_index"):  # X에 그릴 데이터가 있다면
                                                x_data_disp = x_data  #
                                                y_data_disp = y_data  #
                                            else:
                                                x_data_disp = [x_data[x_data.index(YAttr)] for y in y_data]
                                                y_data_disp = y_data

                                            if YAttr in lstSelectedItemText:  # 현재 선택되어 있다면
                                                matplotlib_axes.bar(
                                                    [dicXdata[x_data_disp[i]]+dicOffset_Y[YAttr] for i in lstDataPos],
                                                    [y_data_disp[i] for i in lstDataPos],
                                                    alpha=CFG_Bar_Alpha_Selected,
                                                    width=width_Y,
                                                    color=[colorsY[lstLegendYValue_unique.index(Legend)%len(colorsY)] for x in lstDataPos],
                                                    label=YAttr)
                                            else:
                                                matplotlib_axes.bar(
                                                    [dicXdata[x_data_disp[i]]+dicOffset_Y[YAttr] for i in lstDataPos],
                                                    [y_data_disp[i] for i in lstDataPos],
                                                    alpha=CFG_Bar_Alpha_Unselected,
                                                    width=width_Y,
                                                    color=[colorsY[lstLegendYValue_unique.index(Legend)%len(colorsY)] for x in lstDataPos],
                                                    label=YAttr)

                                # if (iProgress != int((lstY1Y2Attr.index(YAttr)+1)/(len(lstY1Y2Attr)) * 100)):
                                #     iProgress = int((lstY1Y2Attr.index(YAttr)+1)/(len(lstY1Y2Attr)) * 100)
                                #     if (iProgress % 10 == 0):
                                #         print("{0}%({1}/{2})".format(iProgress, (lstY1Y2Attr.index(YAttr)+1), len(lstY1Y2Attr) ))  # 진행상황 표시


                        else: #if (len(lstLegAttr) > 0):  # 'L' 에 체크가 되었다면

                            for i, YAttr in enumerate(lstYAttr):

                                y_data = dfData[YAttr].to_numpy()

                                iRow_start = len(y_data_disp)-iLength
                                if YAttr in lstDrawY_Legend:
                                    iRow_start = len(y_data_disp)-iLength+1 # legend 이전에 그린거 제외

                                    if (len(XAttr) > 0) and (XAttr != "column_index"):  # X에 그릴 데이터가 있다면
                                        x_data_disp = x_data
                                        y_data_disp = y_data
                                    else:
                                        x_data_disp = [x_data[x_data.index(YAttr)] for y in y_data]
                                        y_data_disp = y_data

                                else: # if YAttr in lstDrawY_Legend:
                                    if (len(XAttr) > 0) and (XAttr != "column_index"):  # X에 그릴 데이터가 있다면
                                        x_data_disp = x_data #
                                        y_data_disp = y_data #
                                    else:
                                        x_data_disp = [x_data[x_data.index(YAttr)] for y in y_data]
                                        y_data_disp = y_data
                                
                                # Bar 색상지정
                                if(boColorGroup==True):
                                    color_w_YAttr = dicColor_w_YAttr[YAttr]
                                else:
                                    color_w_YAttr = colorsY[lstY1Y2Attr.index(YAttr) % len(colorsY)]


                                if YAttr in lstSelectedItemText:  # 현재 선택되어 있다면
                                    for row in range(iRow_start, len(y_data_disp)):  #
                                        matplotlib_axes.bar(
                                            dicXdata[x_data_disp[row]]+dicOffset_Y[YAttr],
                                            y_data_disp[row],
                                            alpha=CFG_Bar_Alpha_Selected,
                                            width=width_Y,
                                            color=color_w_YAttr,
                                            label=YAttr)
                                else:
                                    for row in range(iRow_start, len(y_data_disp)):  #
                                        matplotlib_axes.bar(
                                            dicXdata[x_data_disp[row]]+dicOffset_Y[YAttr],
                                            y_data_disp[row],
                                            alpha=CFG_Bar_Alpha_Unselected,
                                            width=width_Y,
                                            color=color_w_YAttr,
                                            label=YAttr)

                                # if (iProgress != int((lstY1Y2Attr.index(YAttr)+1)/(len(lstY1Y2Attr)) * 100)):
                                #     iProgress = int((lstY1Y2Attr.index(YAttr)+1)/(len(lstY1Y2Attr)) * 100)
                                #     if (iProgress % 10 == 0):
                                #         print("{0}%({1}/{2})".format(iProgress, (lstY1Y2Attr.index(YAttr)+1), len(lstY1Y2Attr) ))  # 진행상황 표시












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


                # xticks
                if (len(lstY2Attr)>0) or (len(lstY1Attr)>0): # 그릴 데이터가 있을때
                    if (len(XAttr) > 0) and (XAttr != "column_index"):  # X에 그릴 데이터가 있다면
                        lstOrder = []
                        for x_data_one in x_data_range:
                            lstOrder.append(x_data_range.index(x_data_one))
                        lstOrder = sorted(lstOrder)

                        npMask = np.empty((0))
                        if (len(lstOrder) > 200):
                            npMask = np.arange(0,len(lstOrder),5) # 0,5,10, ...
                        elif (len(lstOrder) > 100):
                            npMask = np.arange(0,len(lstOrder),3)
                        elif (len(lstOrder) > 30):
                            npMask = np.arange(0,len(lstOrder),2)
                        else:
                            npMask = np.arange(0,len(lstOrder),1)

                        self.MplWidget.canvas.axes_1.set_xticks( [ x_data_range[iMask] for iMask in npMask ], \
                                                                labels=[ x_data_raw[iMask] for iMask in npMask ] )
                        self.MplWidget.canvas.axes_2.set_xticks( [ x_data_range[iMask] for iMask in npMask ], \
                                                                labels=[ x_data_raw[iMask] for iMask in npMask ] )

                    elif(XAttr == "column_index"): # column_index
                        lstOrder = [] # lstOrder가 실제 순서와 다를 수 있지만, tick표시용으로 괜찮음
                        for YAttr in lstY1Attr:
                            lstOrder.append(lstY1Y2Attr.index(YAttr))
                        for YAttr in lstY2Attr:
                            lstOrder.append(lstY1Y2Attr.index(YAttr))
                        lstOrder = [ iOrder-min(lstOrder)+1 for iOrder in lstOrder ] # 1, 2, 3, ...

                        npMask = np.empty((0))
                        if (len(lstOrder) > 200):
                            npMask = np.arange(0,len(lstOrder),5) # 0,5,10, ...
                        elif (len(lstOrder) > 100):
                            npMask = np.arange(0,len(lstOrder),3)
                        elif (len(lstOrder) > 30):
                            npMask = np.arange(0,len(lstOrder),2)
                        else:
                            npMask = np.arange(0,len(lstOrder),1)

                        self.MplWidget.canvas.axes_1.set_xticks( [ x_data_range[iMask] for iMask in npMask ], \
                                                                labels=[ lstOrder[iMask] for iMask in npMask ] )
                        self.MplWidget.canvas.axes_2.set_xticks( [ x_data_range[iMask] for iMask in npMask ], \
                                                                labels=[ lstOrder[iMask] for iMask in npMask ] )

                    elif (len(x_data_raw)==len(x_data_num) ): # 숫자일때
                        x_data_range = sorted(x_data_range) # 정렬

                        npMask = np.empty((0))
                        if (len(x_data_range) > 200):
                            npMask = np.arange(0,len(x_data_range),5) # 0,5,10, ...
                        elif (len(x_data_range) > 100):
                            npMask = np.arange(0,len(x_data_range),3)
                        elif (len(x_data_range) > 30):
                            npMask = np.arange(0,len(x_data_range),2)
                        else:
                            npMask = np.arange(0,len(x_data_range),1)

                        self.MplWidget.canvas.axes_1.set_xticks( [ x_data_range[iMask] for iMask in npMask ] )
                        self.MplWidget.canvas.axes_2.set_xticks( [ x_data_range[iMask] for iMask in npMask ] )

                    else:
                        self.MplWidget.canvas.axes_1.set_xticks(x_data_range, labels=x_data_raw)



                # label
                if (len(XAttr) > 0):  # X에 그릴 데이터가 있다면
                    self.MplWidget.canvas.axes_1.set_xlabel(XAttr) # 1개만 들어올것임
                else:
                    self.MplWidget.canvas.axes_1.set_xlabel("sequnce")


                if (len(lstY1Attr) > 0):  # Y1에 그릴 데이터가 있다면
                    if (len(lstY1Attr) == 1):  # 여러개 일수 있음
                        self.MplWidget.canvas.axes_1.set_ylabel(lstY1Attr[0])
                    else:
                        strLabel = lstY1Attr[0].strip() # 선행, 후행 공백을 삭제
                        for Y1Attr in lstY1Attr:
                            # 공통인 문잘열을 찾음
                            strLabel = max(get_str_array(Y1Attr) & get_str_array(strLabel), key=len)
                            if( len(strLabel)==0 ): #같은게 하나도 없으면 반복문 빠져나옴
                                break
                        if( len(strLabel)>0 ):
                            self.MplWidget.canvas.axes_1.set_ylabel(strLabel)

                if (len(lstY2Attr) > 0):  # Y1에 그릴 데이터가 있다면
                    if (len(lstY2Attr) == 1):  # 여러개 일수 있음
                        self.MplWidget.canvas.axes_2.set_ylabel(lstY2Attr[0])
                    else:
                        strLabel = lstY2Attr[0].strip() # 선행, 후행 공백을 삭제
                        for Y2Attr in lstY2Attr:
                            # 공통인 문잘열을 찾음
                            strLabel = max(get_str_array(Y2Attr) & get_str_array(strLabel), key=len)
                            if (len(strLabel) == 0):  # 같은게 하나도 없으면 반복문 빠져나옴
                                break
                        if( len(strLabel) > 0 ):
                            self.MplWidget.canvas.axes_2.set_ylabel(strLabel)


                # X 축 신호가 바뀌면, 오류가 나는 경우 있음
                try:
                    self.MplWidget.canvas.axes_1.autoscale_view()
                    self.MplWidget.canvas.axes_2.autoscale_view()

                    # # 셀별로 값 확인하기 위해서
                    # if (XAttr == "column_index"):
                    #     lstColumn = dfData.columns.to_list()
                    #     lstColIndex = []
                    #     for YAttr in lstY1Attr:
                    #         lstColIndex.append( 1+lstColumn.index(YAttr)-lstColumn.index(lstY1Attr[0]) )
                    #     for YAttr in lstY2Attr:
                    #         lstColIndex.append( 1+lstColumn.index(YAttr)-lstColumn.index(lstY2Attr[0]) )
                    #     lstColIndex.append( min(lstColIndex)-0.5 )
                    #     lstColIndex.append( max(lstColIndex)+0.5 )
                    #     x_data = lstColIndex
                    #
                    #
                    # # matpltlib 의 date는 "1970-01-01 00:00:00"는 0.0
                    # #                    "2000-01-01 00:00:00"는 10957.000
                    # #                    "2100-01-01 00:00:00"는 47482.000 로 표시됨
                    # if (    (self.xdata_type == type(datetime.datetime.now()))
                    #      or (self.xdata_type == type(np.datetime64('2023-03-09')))):
                    #     x_data = mdates.date2num(x_data)
                    #
                    #
                    # x_max = max(x_data)
                    # x_min = min(x_data)
                    # x_left, x_right = self.MplWidget.canvas.axes_1.get_xlim()
                    # if( (x_right-x_left) > (x_max-x_min)*3 ):
                    #     # print("x-axis", x_left, x_right, " xdata:", x_min, x_max)
                    #     width = max(x_data) - min(x_data) # X축 범위 조정 위해
                    #     self.MplWidget.canvas.axes_1.set_xlim(min(x_data) - width/20, max(x_data) + width/20)
                    #     self.MplWidget.canvas.axes_2.set_xlim(min(x_data) - width/20, max(x_data) + width/20)

                except Exception as e:
                    pass # max()나 min()을 구할수 없는 데이터타입일때 오류 발생
                    # print( e )


                # ------------------------------------------------------
                # 화면에 그리기
                # ------------------------------------------------------
                try:
                    # plot
                    self.MplWidget.canvas.draw()
                except Exception as e:
                    print(e)
                    _ = QMessageBox.information(self, e)



    def onMplKeyPress(self, event):
        """
        Keyboard key callback
        """
        if event.key == 'shift':
            self.shift_is_held = True



    def onMplKeyRelease(self, event):
        """
        Keyboard key callback
        """
        if event.key == 'shift':
            self.shift_is_held = False




    def onMplMouseUp(self, event):
        """
        Mouse button up callback
        """
        # 마우스 UP시 
        self.last_mouse = "Up"
        self.current_artist = None
        self.currently_dragging = False
        pass



    def onMplMouseDown(self, event):
        """
        Mouse button down callback
        """
        global SPL_boForceDraw

        if((self.last_artist != None) and (self.last_mouse == "Up")) or (SPL_boForceDraw==True) :


            # annotation 삭제
            for annotation in self.lstAnnotation:
                annotation.remove()
            self.lstAnnotation = []

            # 화면 업데이트
            self.MplWidget.canvas.draw()
            SPL_boForceDraw = False

        self.last_mouse = "Down"
        self.number_annotation_one_click = 0

        # line 모드
        self.currently_dragging = True
        if(CFG_Common_PickMode == COMMON_PICKMODE_POINTRULER):
            if event and event.dblclick:
                if len(self.lstPointLabel) < 1: # 기능제한. bar를 rectangular로 인식하여 2개 지점을 이용한 라인을 그을 수 없음
                    x, y = event.xdata, event.ydata
                    newPointLabel = "point"+str(len(self.lstPointLabel)+1)
                    axes_1 = self.MplWidget.canvas.axes_1
                    # calculate the aspect ratio
                    xscale, yscale = axes_1.transData.transform([1, 1]) - axes_1.transData.transform([0, 0])
                    # draw the ellipse to be displayed as circle
                    xmin, xmax = axes_1.get_xlim()
                    radius_x = abs((xmax-xmin)/50)
                    radius_y = radius_x * xscale / yscale
                    self.radius_y = radius_y
                    point_object = patches.Ellipse(xy=(x, y),
                                                   width=radius_x,
                                                   height=radius_y,
                                                   angle=0,
                                                   facecolor="none",
                                                   edgecolor='red',
                                                   alpha=0.8,
                                                   label=newPointLabel)
                    point_object.set_picker(2)
                    self.MplWidget.canvas.axes_1.add_patch(point_object) # 원을 그림
                    self.lstPointLabel.append(newPointLabel)
                    self.lstPoint_object.append(point_object)
                    # annotion 표시
                    Annotation_one = axes_1.annotate(
                        f"({x:.3f}, {y:.3f})",
                        xy=(x, y-1.2*radius_y),
                        color='blue',
                        bbox=dict(boxstyle='square,pad=.0', facecolor=self.fc_box, edgecolor=self.ec_box))
                    self.lstAnnotation.append(Annotation_one)
                    if len(self.lstPointLabel) == 2: # 2개 point이면 line 그림
                        xdata = []
                        ydata = []
                        for p in axes_1.patches:
                            cx, cy = p.center
                            xdata.append(cx)
                            ydata.append(cy)
                        self.lstLine_object = axes_1.plot(xdata, ydata, alpha=0.5, c='red', lw=2, picker=True)
                        self.lstLine_object[0].set_pickradius(1)
                        Annotation_one = axes_1.annotate(
                            f"△=({xdata[1]-xdata[0]:.3f}, {ydata[1]-ydata[0]:.3f})",
                            xy=(xdata[0]+(xdata[1]-xdata[0])/2, ydata[0]+(ydata[1]-ydata[0])/2),
                            color='blue',
                            bbox=dict(boxstyle='square,pad=.0', facecolor=self.fc_box, edgecolor=self.ec_box))
                        self.lstAnnotation.append(Annotation_one)

                    # 화면 업데이트
                    xmin, xmax = self.MplWidget.canvas.axes_1.get_xlim() # x, y축 범위 고정
                    ymin, ymax = self.MplWidget.canvas.axes_1.get_ylim()
                    self.MplWidget.canvas.axes_1.set_xlim(xmin, xmax)
                    self.MplWidget.canvas.axes_1.set_ylim(ymin, ymax)
                    self.MplWidget.canvas.draw()

                else:
                    boReDraw = False
                    # annotation 삭제
                    for annotation in self.lstAnnotation:
                        annotation.remove()
                        boReDraw = True
                    self.lstAnnotation = []
                    for i, point_object in enumerate(self.lstPoint_object): # 원을 지움
                        point_object.remove()
                        boReDraw = True
                    self.lstPointLabel = []
                    self.lstPoint_object = []
                    for i, line_object in enumerate(self.lstLine_object): # 선을 지움
                        line_object.remove()
                        boReDraw = True
                    self.lstLine_object = []
                    if( boReDraw == True ):
                        # 화면 업데이트 및 화면업댓시 x,y 변경안하도록
                        xmin, xmax = self.MplWidget.canvas.axes_1.get_xlim()
                        ymin, ymax = self.MplWidget.canvas.axes_1.get_ylim()
                        self.MplWidget.canvas.axes_1.set_xlim(xmin, xmax)
                        self.MplWidget.canvas.axes_1.set_ylim(ymin, ymax)
                        self.MplWidget.canvas.draw()
        else:
            boReDraw = False
            for i, point_object in enumerate(self.lstPoint_object):  # 원을 지움
                point_object.remove()
                boReDraw = True
            self.lstPointLabel = []
            self.lstPoint_object = []
            for i, line_object in enumerate(self.lstLine_object):  # 선을 지움
                line_object.remove()
                boReDraw = True
            self.lstLine_object = []
            if (boReDraw == True):
                self.MplWidget.canvas.draw()

        pass



    def onMplMouseMotion(self, event):
        """
        Mouse motion callback
        """
        if (CFG_Common_PickMode == COMMON_PICKMODE_POINTRULER):
            if not self.currently_dragging:
                return
            if self.current_artist == None:
                return
            if event.xdata == None:
                return
            dx, dy = self.offset
            if isinstance(self.current_artist, patches.Ellipse) and (len(self.lstPointLabel) > 0):
                cx, cy = event.xdata + dx, event.ydata + dy
                self.current_artist.center = cx, cy
                xdata, ydata = [cx], [cy]
                # print("moving", current_artist.get_label())
                if(len(self.lstLine_object) > 0):
                    xdata = list(self.lstLine_object[0].get_xdata())
                    ydata = list(self.lstLine_object[0].get_ydata())
                    for i in range(0, len(xdata)):
                        if self.lstPointLabel[i] == self.current_artist.get_label():
                            xdata[i] = cx
                            ydata[i] = cy
                            break
                    self.lstLine_object[0].set_data(xdata, ydata) # 라인 좌표도 변경

            elif isinstance(self.current_artist, Line2D) and (len(self.lstLine_object) > 0):
                xdata = list(self.lstLine_object[0].get_xdata())
                ydata = list(self.lstLine_object[0].get_ydata())
                xdata0 = xdata[0]
                ydata0 = ydata[0]
                for i in range(0, len(xdata)):
                    xdata[i] = event.xdata + dx + xdata[i] - xdata0
                    ydata[i] = event.ydata + dy + ydata[i] - ydata0
                self.lstLine_object[0].set_data(xdata, ydata)
                for p in self.MplWidget.canvas.axes_1.patches: # 포인트 좌표도 변경
                    pointLabel = p.get_label()
                    i = self.lstPointLabel.index(pointLabel)
                    p.center = xdata[i], ydata[i]

            radius_y = self.radius_y
            # annotation 삭제
            for annotation in self.lstAnnotation:
                annotation.remove()
            self.lstAnnotation = []
            # annotion 표시
            if(len(self.lstPoint_object)>0):
                Annotation_one = self.MplWidget.canvas.axes_1.annotate(
                    f"({xdata[0]:.3f}, {ydata[0]:.3f})",
                    xy=(xdata[0], ydata[0]-1.2*radius_y),
                    color='blue',
                    bbox=dict(boxstyle='square,pad=.0', facecolor=self.fc_box, edgecolor=self.ec_box))
                self.lstAnnotation.append(Annotation_one)
            if(len(self.lstPoint_object)>1):
                Annotation_one = self.MplWidget.canvas.axes_1.annotate(
                    f"({xdata[1]:.3f}, {ydata[1]:.3f})",
                    xy=(xdata[1], ydata[1]-1.2*radius_y),
                    color='blue',
                    bbox=dict(boxstyle='square,pad=.0', facecolor=self.fc_box, edgecolor=self.ec_box))
                self.lstAnnotation.append(Annotation_one)
            if(len(self.lstLine_object)>0):
                Annotation_one = self.MplWidget.canvas.axes_1.annotate(
                    f"△=({xdata[1] - xdata[0]:.3f}, {ydata[1] - ydata[0]:.3f})",
                    xy=(xdata[0]+(xdata[1]-xdata[0])/2, ydata[0]+(ydata[1]-ydata[0])/2),
                    color='blue',
                    bbox=dict(boxstyle='square,pad=.0', facecolor=self.fc_box, edgecolor=self.ec_box))
                self.lstAnnotation.append(Annotation_one)

            # 화면 업데이트
            self.MplWidget.canvas.draw()

        pass



    def onMplPick(self, event):
        """
        Mouse pick callback
        """

        # pick_event는 1축만 가능
        # (참조) https://stackoverflow.com/questions/55565393/matplotlib-picker-event-on-secondary-y-axis
        # For those who are 'picking' artists while using twinx, pick events are only called for the artists in the top-most axes.

        if( CFG_Common_PickMode==COMMON_PICKMODE_LEGEND ):
            # On the pick event, find the original line corresponding to the legend
            thisline = event.artist  # artist는 line 임

            if (self.last_mouse=="Up") and (self.shift_is_held==False):  # 새로 클릭을 했다면

                #새로 클릭을 해서, 이전 annotion 지움
                for annotation in self.lstAnnotation:
                    annotation.remove()
                self.lstAnnotation = []

            # 마우스 버튼 UP 전까지 기억
            self.last_artist = thisline
            self.last_mouse = "Down"


        elif( CFG_Common_PickMode==COMMON_PICKMODE_POINTRULER ):
            if self.current_artist is None:
                if(len(self.lstPoint_object)>0):
                    if(event.artist == self.lstPoint_object[0]):
                        self.current_artist = event.artist
                if (len(self.lstPoint_object) > 1):
                    if (event.artist == self.lstPoint_object[1]):
                        self.current_artist = event.artist
                if (len(self.lstLine_object)>0):
                    if (event.artist == self.lstLine_object[0]):
                        self.current_artist = event.artist
                if self.current_artist is None:
                    return

                # print("pick ", current_artist)
                if isinstance(event.artist, patches.Ellipse):
                    if event.mouseevent.dblclick:
                        pass
                    else:
                        x0, y0 = self.current_artist.center
                        x1, y1 = event.mouseevent.xdata, event.mouseevent.ydata
                        self.offset = [(x0 - x1), (y0 - y1)]
                elif isinstance(event.artist, Line2D):
                    if event.mouseevent.dblclick:
                        pass
                    else:
                        xdata = event.artist.get_xdata()
                        ydata = event.artist.get_ydata()
                        x1, y1 = event.mouseevent.xdata, event.mouseevent.ydata
                        self.offset = xdata[0] - x1, ydata[0] - y1

                # 화면 업데이트
                self.MplWidget.canvas.draw()

        pass



    def onMplWheel(self, event):
        """
        Mouse wheel scroll callback
        """
        pass





app = QApplication([])
clipboard = app.clipboard() # 클립보드 사용 위해
window = MatplotlibWidget()
window.show()
app.exec_()
















