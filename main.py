# ------------------------------------------------------
# ---------------------- main.py -----------------------
# ------------------------------------------------------
from PyQt5.QtWidgets import (QApplication, QInputDialog, QMainWindow, QMessageBox, QFileDialog, QTableWidgetItem, QCheckBox)
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon
# from PyQt5.QtCore import Qt

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
CFG_Legend_Max = 30
CFG_Legend_MaxMax = 600
CFG_Makersize_Selected = 20
CFG_Alpha_Selected = 1.0
CFG_Makersize_Unselected = 1
CFG_Alpha_Unselected = 0.7



# Global variables
SPL_dfData = pd.DataFrame()
#                          신호명         체크되는열(신호당 1개의 체크박스만 클릭가능함)
#                                        0:none, 1:첫번째(X), 2:두번째(Y1), ...
SPL_lstChkData = [] # ["  signal name  ", 0]
SPL_strFileName = ""




def Timestamp2DateTime( lstTimestamp ):

    lstDateTime = []  # str -> datetime
    for Timestamp in lstTimestamp:
        dateTimeOne = datetime.datetime.utcfromtimestamp(Timestamp)
        lstDateTime.append( dateTimeOne )

    return lstDateTime



def GetDatetime(strClock): # 다양한 형태의 clock 패턴을 처리
    # 2021-06-30T07:36:10.000Z
    strptime_patterns = ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M:%S.%f', "%d-%m-%Y", "%Y-%m-%d", '%Y-%m-%dT%H:%M:%S.%fZ']

    boNoon = False
    if " 오전" in strClock:
        strClock = strClock.replace(" 오전", "")
    elif " 오후" in strClock:
        strClock = strClock.replace(" 오후", "")
        boNoon = True

    for pattern in strptime_patterns:
        try:
            datetimeClock = datetime.datetime.strptime(strClock, pattern)
            if boNoon == True:
                datetimeClock = datetimeClock + datetime.timedelta(hours=12)
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


class MatplotlibWidget(QMainWindow):

    def __init__(self):
        
        QMainWindow.__init__(self)


        loadUi("qt_designer.ui",self)
        self.setWindowIcon(QIcon('iconPlot.png')) # 맨왼쪽위 아이콘
        self.setWindowTitle("Simple Matplotlib w/ GUI")

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
                    strRet = ('Left: {1:<40}    Right: {0:<}'.format(*['({}, {:.3f})'.format(str_x, y) for x, y in coords]))
                else:
                    strRet = ('Left: {1:<40}    Right: {0:<}'.format(*['({:.3f}, {:.3f})'.format(x, y) for x, y in coords]))

                return strRet

            return format_coord

        self.MplWidget.canvas.axes_1.format_coord = make_format(self.MplWidget.canvas.axes_1,
                                                                self.MplWidget.canvas.axes_2) # y2이 z-oreder가 높을때


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

        # Canvas event handlers
        self.MplWidget.canvas.mpl_connect('button_release_event', self.onMplMouseUp)
        self.MplWidget.canvas.mpl_connect('button_press_event', self.onMplMouseDown)
        self.MplWidget.canvas.mpl_connect('motion_notify_event', self.onMplMouseMotion)
        self.MplWidget.canvas.mpl_connect('pick_event', self.onMplPick)
        self.MplWidget.canvas.mpl_connect('scroll_event', self.onMplWheel)


        # 현재 위치
        self.base_path = os.getcwd()

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

                df["column_index"] = 0 # default 값, Y 그릴때 생성되는 값
                df["filename"] = strFileName  # 파일이름 생성
                df["file_sequence"] = df.index  # Sequnce를 생성
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


    # DataFrame()의 column 이름이 중복일때 수정하기 위해
    def vFixColumnName(self):
        pass

    def OnBtnClick_Plt(self):

        global SPL_lstChkData
        global SPL_dfData

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




                #                                  먼저그림          legend           나머지그림
                # -----------------------------------------------------------------------------------------------------------
                # 'L' 체크 되었을때
                #   legend 표시가 30개 이상 일때
                #     선택된게 있을 때             : 1st 선택된 Ys    many "signal"    나머지 그림
                #     선택된게 없을 때             : 1st Y로         many "signal"    나머지 그림
                #   legend 표시가 30개 이내 일때
                #     선택된게 있을 때             : 1st Y로          legend           나머지 그림
                #     선택된게 없을 때             : 1st Y로          legend           나머지 그림
                # 'L' 체크 안 되었을때
                #   Y축 표시가 30개 이상 일때
                #     선택된게 있을 때             : 선택된 Ys        legend           나머지 그림
                #     선택된게 없을 때             : max5, min5      legend           나머지 그림
                #   Y축 표시가 30개 이내 일때
                #     선택된게 있을 때             : 모든 Ys          legend
                #     선택된게 없을 때             : 모든 Ys          legend
                
                
                # 색의 출처 : https://matplotlib.org/stable/users/prev_whats_new/dflt_style_changes.html
                colorsY1 = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'
                          , '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
                colorsY2 = ["red", "orange", "yellow", "green", "blue", "indigo", "violet"]

                # Y1과 Y2 반복
                for lstYAttr_Index, lstYAttr in enumerate( [lstY1Attr, lstY2Attr] ):

                    # Y1, Y2 에 따라 변경
                    colorsY = colorsY1
                    matplotlib_axes = self.MplWidget.canvas.axes_1
                    # Global 변수들 for 'pick_event'
                    lstGlobalYLine = self.lstY1Line
                    dicGlobalYLineToLegend = self.dicY1LineToLegend

                    # Y1 or Y2 에 따라 변경
                    if( lstYAttr_Index == 1 ): # 현재가 Y1(0)인지 Y2(1)인지에 따라 변경
                        colorsY = colorsY2
                        matplotlib_axes = self.MplWidget.canvas.axes_2
                        lstGlobalYLine = self.lstY2Line
                        dicGlobalYLineToLegend = self.dicY2LineToLegend



                    if (len(lstYAttr) > 0):  # Y1 에 그릴 데이터가 있다면

                        # ---------------------------------------------------------------
                        # legend 표시용 그래프 그리기, 먼저 그리는 데이터 사전준비 
                        # ---------------------------------------------------------------
                        lstLegend = []  # Y1 legend 표시 데이터 이름들
                        lstLegendDrawDataPos = []  # Y1 legend 표시 데이터들의 위치 정보
                        lstLegendYValue_unique = []  # Y1 legend 중복 없이.
                        lstLegendY_Selected = []  # legend 표시를 위해 먼저 그릴 Y 들


                        if (len(lstLegAttr) > 0):  # 'L' 에 체크가 되었다면

                            # 'L' 체크 되었을때
                            #   legend 표시가 30개 이상 일때
                            #     선택된게 있을 때             : (1st 선택된 Ys)    many "signal"    나머지 그림
                            #     선택된게 없을 때             : (1st Y로)         many "signal"    나머지 그림
                            #   legend 표시가 30개 이내 일때
                            #     선택된게 있을 때             : (1st Y로)          legend           나머지 그림
                            #     선택된게 없을 때             : (1st Y로)          legend           나머지 그림
                            lstLegendYValue = SPL_dfData[lstLegAttr].values.tolist()  # legend들의 데이터
                            lstLegendYValue = [x[0] for x in lstLegendYValue]  # legend들의 데이터
                            lstLegendYValue_unique = list(np.unique(lstLegendYValue, return_counts=False))  # Y1 1개의 legend

                            # 먼저 그릴 Y 찾기
                            if (len(lstLegendYValue_unique) > CFG_Legend_Max):
                                for SelectedItemText in lstSelectedItemText:
                                    if SelectedItemText in lstYAttr:
                                        lstLegendY_Selected.append(SelectedItemText)
                                if (len(lstLegendY_Selected) == 0):  # 선택된 중인 Y1 이 없으면, 1st Y
                                    lstLegendY_Selected.append(lstYAttr[0])
                            else:
                                lstLegendY_Selected.append(lstYAttr[0])


                        else:
                            # 'L' 체크 안 되었을때
                            #   Y축 표시가 30개 이상 일때
                            #     선택된게 있을 때             : (선택된 Ys)        legend           나머지 그림
                            #     선택된게 없을 때             : (max5, min5)      legend           나머지 그림
                            #   Y축 표시가 30개 이내 일때
                            #     선택된게 있을 때             : (모든 Ys)          legend
                            #     선택된게 없을 때             : (모든 Ys)          legend

                            if (len(lstYAttr) > CFG_Legend_Max):

                                for SelectedItemText in lstSelectedItemText:
                                    if SelectedItemText in lstYAttr:
                                        lstLegendY_Selected.append(SelectedItemText)

                                if (len(lstLegendY_Selected) == 0):
                                    '''
                                    # Y에 표시할 값 max 와 min 값 기준으로 정렬
                                    series_Y_max = pd.Series(SPL_dfData[lstYAttr].max())
                                    # series_Y_avg = pd.Series(SPL_dfData[lstYAttr].mean())
                                    series_Y_min = pd.Series(SPL_dfData[lstYAttr].min())
                                    # sorted_desscending = series_Y_avg.sort_values(ascending=False).index
                                    # sorted_ascending = series_Y_avg.sort_values(ascending=True).index
                                    sorted_desscending = series_Y_max.sort_values(ascending=False).index
                                    sorted_ascending = series_Y_min.sort_values(ascending=True).index
            
                                    # Y (max6, min5)
                                    for Y_sorted in sorted_desscending[0:min(6, int(len(sorted_desscending)/2))]: # 큰거 6개
                                        lstLegendY_Selected.append( Y_sorted )
                                    for Y_sorted in reversed(sorted_ascending): # 작은거 5개
                                        if(Y_sorted not in lstLegendY_Selected) and (len(lstLegendY_Selected)<(min(11, len(sorted_desscending)))): # 최대 11개
                                            lstLegendY_Selected.append( Y_sorted )
                                    '''
                                    lstLegendY_Selected = lstYAttr[:6] + lstYAttr[-5:]

                            else:
                                lstLegendY_Selected = lstYAttr



                        # ------------------------------------------------------
                        # Y축 데이터 그래프 그리기
                        # ------------------------------------------------------

                        for i, YAttr in enumerate(lstYAttr):
                            y_data = SPL_dfData[YAttr].to_numpy()

                            # -------------------------------------------------------------------------------------
                            # 시간으로 변환 (변환에 시간이 오래 걸려, 선택되었을때만 1번 수행
                            lstDateTime, lstTimeStamp = strptime2Timestamp(SPL_dfData[YAttr].values.tolist())
                            if (len(lstDateTime) == len(SPL_dfData[YAttr])):  # 같은 사이즈 만큼 변환하였다면
                                y_data = lstDateTime
                                SPL_dfData[YAttr] = lstDateTime  # 한번 변환한 것은 다시 변환 안하기 위해

                            # Timestamp 이면.
                            # UTC Timestamp 는 1970-01-01 00h00m00s 를 기준으로 초단위로 환산한 숫자
                            if (("float" in str(type(y_data[0])))  # float 형이면 \
                                    and (y_data[0] > 1300000000) \
                                    and (y_data[-1] < 1900000000) \
                                    and ("ime" in YAttr)):
                                lstDateTime = Timestamp2DateTime(SPL_dfData[YAttr].values.tolist())
                                y_data = lstDateTime
                                SPL_dfData[YAttr] = lstDateTime  # 한번 변환한 것은 다시 변환 안하기 위해

                            # -------------------------------------------------------------------------------------

                            # 셀별로 값 확인하기 위해
                            if( XAttr == "column_index" ):
                                lstColumn = SPL_dfData.columns.to_list()
                                x_data = [ (lstColumn.index(YAttr)+random.random()*0.8-0.4) for x in range( len(x_data) ) ]




                            # lstLegAttr에는 신호이름이 저장됨
                            # lstLegend 에는 'L'체크시 신호이름의 값이 저장되고, 그외는 신호이름이 저장됨
                            if (len(lstLegAttr) > 0):  # 'L' 에 체크가 되었다면

                                # 'L' 체크 되었을때
                                #   legend 표시가 30개 이상 일때
                                #     선택된게 있을 때             : (1st 선택된 Ys)    many "signal"    나머지 그림
                                #     선택된게 없을 때             : (1st Y로)         many "signal"    나머지 그림
                                #   legend 표시가 30개 이내 일때
                                #     선택된게 있을 때             : (1st Y로)          legend           나머지 그림
                                #     선택된게 없을 때             : (1st Y로)          legend           나머지 그림

                                if (YAttr in lstLegendY_Selected):

                                    if (len(lstLegendYValue_unique) > CFG_Legend_MaxMax):

                                        # legend 용 value 값들이 너무 많아 위치 데이터 생성이 어려움
                                        if YAttr in lstSelectedItemText:  # 현재 선택되어 있다면
                                            line, = matplotlib_axes.plot(
                                                x_data,
                                                y_data,
                                                '-o',
                                                linewidth=0.8,
                                                drawstyle='steps-post',
                                                alpha=CFG_Alpha_Selected,
                                                picker=True, pickradius=5)  # 5 points tolerance
                                            line.set_label(YAttr)  # 'Figure Options' 창에서 Curve이름 표시하기 위해
                                            dicGlobalYLineToLegend[line] = YAttr
                                            lstGlobalYLine.append( line )

                                        else:
                                            line, = matplotlib_axes.plot(
                                                x_data,
                                                y_data,
                                                linewidth=0.8,
                                                drawstyle='steps-post',
                                                alpha=CFG_Alpha_Unselected,
                                                picker=True, pickradius=5)  # 5 points tolerance
                                            line.set_label(YAttr)  # 'Figure Options' 창에서 Curve이름 표시하기 위해
                                            dicGlobalYLineToLegend[line] = YAttr
                                            lstGlobalYLine.append( line )
                                    else:

                                        # 첫번째 Legend의 데이터 위치와 그외 데이터로 위치를 분리함
                                        for LegendYValue in lstLegendYValue_unique:  # legend 별 1개 씩 처리함
                                            if (LegendYValue not in lstLegend):  # 이전에 표시하지 않은 legend의 데이터라면.
                                                npLegendDrawDataPos = np.where(np.array(lstLegendYValue) == LegendYValue)[0]
                                                lstLegendDrawDataPos.append(npLegendDrawDataPos)  # legend 그린 후 나머지 그릴때 안 그리려고 저장
                                                lstLegend.append(LegendYValue)  # 표시한 legend에 등록

                                                if YAttr in lstSelectedItemText:  # 현재 선택되어 있다면
                                                    line, = matplotlib_axes.plot(
                                                        x_data[npLegendDrawDataPos],
                                                        y_data[npLegendDrawDataPos],
                                                        '-o',
                                                        linewidth=0.8,
                                                        drawstyle='steps-post',
                                                        alpha=CFG_Alpha_Selected,
                                                        color=colorsY[lstLegendYValue_unique.index(LegendYValue) % len(colorsY)],
                                                        picker=True, pickradius=5)  # 5 points tolerance
                                                    line.set_label(LegendYValue)  # 'Figure Options' 창에서 Curve이름 표시하기 위해
                                                    dicGlobalYLineToLegend[line] = LegendYValue
                                                    lstGlobalYLine.append(line)
                                                else:
                                                    line, = matplotlib_axes.plot(
                                                        x_data[npLegendDrawDataPos],
                                                        y_data[npLegendDrawDataPos],
                                                        linewidth=0.8,
                                                        drawstyle='steps-post',
                                                        alpha=CFG_Alpha_Unselected,
                                                        color=colorsY[lstLegendYValue_unique.index(LegendYValue) % len(colorsY)],
                                                        picker=True, pickradius=5)  # 5 points tolerance
                                                    line.set_label(LegendYValue)  # 'Figure Options' 창에서 Curve이름 표시하기 위해
                                                    dicGlobalYLineToLegend[line] = LegendYValue
                                                    lstGlobalYLine.append(line)


                            else:

                                # 'L' 체크 안 되었을때
                                #   Y축 표시가 30개 이상 일때
                                #     선택된게 있을 때             : (선택된 Ys)        legend           나머지 그림
                                #     선택된게 없을 때             : (max5, min5)      legend           나머지 그림
                                #   Y축 표시가 30개 이내 일때
                                #     선택된게 있을 때             : (모든 Ys)          legend
                                #     선택된게 없을 때             : (모든 Ys)          legend

                                if (YAttr in lstLegendY_Selected):

                                    if (len(lstYAttr) > CFG_Legend_Max):
                                        if YAttr in lstSelectedItemText:  # 선택된게 있을 때
                                            lstLegend.append(YAttr)
                                        else:  # 선택된게 없을 때, (max5, ... ,min5)
                                            if (YAttr == lstLegendY_Selected[5]):
                                                lstLegend.append(". . .")
                                            else:
                                                lstLegend.append(YAttr)
                                    else:  #
                                        lstLegend.append(YAttr)

                                    if YAttr in lstSelectedItemText:  # 현재 선택되어 있다면
                                        line, = matplotlib_axes.plot(
                                            x_data,
                                            y_data,
                                            '-o',
                                            linewidth=0.8,
                                            drawstyle='steps-post',
                                            alpha=CFG_Alpha_Selected,
                                            color=colorsY[i%len(colorsY)],
                                            picker=True, pickradius=5)  # 5 points tolerance
                                        line.set_label(YAttr)  # 'Figure Options' 창에서 Curve이름 표시하기 위해
                                        dicGlobalYLineToLegend[line] = YAttr
                                        lstGlobalYLine.append(line)

                                    else:
                                        line, = matplotlib_axes.plot(
                                            x_data,
                                            y_data,
                                            linewidth=0.8,
                                            drawstyle='steps-post',
                                            alpha=CFG_Alpha_Unselected,
                                            color=colorsY[i%len(colorsY)],
                                            picker=True, pickradius=5)  # 5 points tolerance
                                        line.set_label(YAttr)  # 'Figure Options' 창에서 Curve이름 표시하기 위해
                                        dicGlobalYLineToLegend[line] = YAttr
                                        lstGlobalYLine.append(line)


                        # ------------------------------------------------------
                        # Legend 표시
                        # ------------------------------------------------------
                        if (len(lstLegAttr) > 0):  # 'L' 에 체크가 되었다면
                            # 'L' 체크 되었을때
                            #   legend 표시가 30개 이상 일때
                            #     선택된게 있을 때             : 1st 선택된 Ys    (many "signal")    나머지 그림
                            #     선택된게 없을 때             : 1st Y로         (many "signal")    나머지 그림
                            #   legend 표시가 30개 이내 일때
                            #     선택된게 있을 때             : 1st Y로          (legend)           나머지 그림
                            #     선택된게 없을 때             : 1st Y로          (legend)           나머지 그림
                            if (len(lstLegendYValue_unique) > CFG_Legend_MaxMax):
                                Legend = "too many legends"  # 먼저 그릴 Y 찾기

                                if( lstYAttr_Index == 0 ): # Y1 그릴때
                                    if (len(lstY2Attr) > 0):  # Y2 그릴게 있다면
                                        matplotlib_axes.legend([Legend], loc='upper left')
                                    else:
                                        matplotlib_axes.legend([Legend])
                                elif( lstYAttr_Index == 1 ): # Y2 그릴때
                                    if (len(lstY2Attr) > 0):  # Y2 그릴게 있다면
                                        matplotlib_axes.legend([Legend], loc='upper right')

                            elif (len(lstLegendYValue_unique) > CFG_Legend_Max):

                                lstLineOfLegend = lstGlobalYLine[:6] + lstGlobalYLine[-5:]
                                lstLegend = [ dicGlobalYLineToLegend[line] for line in lstLineOfLegend ]
                                lstLegend[5] = "..."

                                if( lstYAttr_Index == 0 ): # Y1 그릴때
                                    if (len(lstY2Attr) > 0):  # Y2 그릴게 있다면
                                        matplotlib_axes.legend(lstLineOfLegend, lstLegend, loc='upper left')
                                    else:
                                        matplotlib_axes.legend(lstLineOfLegend, lstLegend, )
                                elif( lstYAttr_Index == 1 ): # Y2 그릴때
                                    if (len(lstY2Attr) > 0):  # Y2 그릴게 있다면
                                        matplotlib_axes.legend(lstLineOfLegend, lstLegend, loc='upper right')

                            else:
                                if (lstYAttr_Index == 0):  # Y1 그릴때
                                    if (len(lstY2Attr) > 0):  # Y1, Y2 그릴때
                                        matplotlib_axes.legend(lstLegend, loc='upper left')
                                    else:
                                        matplotlib_axes.legend(lstLegend)
                                elif( lstYAttr_Index == 1 ): # Y2 그릴때
                                    if (len(lstY2Attr) > 0):  # Y2 그릴게 있다면
                                        matplotlib_axes.legend(lstLegend, loc='upper right')

                        else:

                            # 'L' 체크 안 되었을때
                            #   Y축 표시가 30개 이상 일때
                            #     선택된게 있을 때             : 선택된 Ys        (legend)           나머지 그림
                            #     선택된게 없을 때             : max5, min5      (legend)           나머지 그림
                            #   Y축 표시가 30개 이내 일때
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







                        # ------------------------------------------------------
                        # Legend 표시외 그래프 그리기
                        # 나머지 데이터 그리기
                        # ------------------------------------------------------
                        if (len(lstLegAttr) > 0):  # 'L' 에 체크가 되었다면



                            for i, YAttr in enumerate(lstYAttr):
                                if YAttr not in lstLegendY_Selected:

                                    # 셀별로 값 확인하기 위해서
                                    if (XAttr == "column_index"):
                                        lstColumn = SPL_dfData.columns.to_list()
                                        x_data = [(lstColumn.index(YAttr)+random.random()*0.8-0.4) for x in range(len(x_data))]

                                    y_data = SPL_dfData[YAttr].to_numpy()

                                    if (len(lstLegendYValue_unique) > CFG_Legend_MaxMax):

                                        # legend 용 value 값들이 너무 많아 위치 데이터 생성이 어려움
                                        if YAttr in lstSelectedItemText:  # 현재 선택되어 있다면
                                            line, = matplotlib_axes.plot(
                                                x_data,
                                                y_data,
                                                '-o',
                                                linewidth=0.8,
                                                drawstyle='steps-post',
                                                alpha=CFG_Alpha_Selected,
                                                picker=True, pickradius=5)  # 5 points tolerance
                                            line.set_label(YAttr)  # 'Figure Options' 창에서 Curve이름 표시하기 위해
                                            dicGlobalYLineToLegend[line] = YAttr
                                            lstGlobalYLine.append(line)

                                        else:
                                            line, = matplotlib_axes.plot(
                                                x_data,
                                                y_data,
                                                linewidth=0.8,
                                                drawstyle='steps-post',
                                                alpha=CFG_Alpha_Unselected,
                                                picker=True, pickradius=5)  # 5 points tolerance
                                            line.set_label(YAttr)  # 'Figure Options' 창에서 Curve이름 표시하기 위해위해
                                            dicGlobalYLineToLegend[line] = YAttr
                                            lstGlobalYLine.append(line)


                                    else:

                                        for j, Legend in enumerate(lstLegendYValue_unique):
                                            lstDataPos = lstLegendDrawDataPos[j]

                                            if YAttr in lstSelectedItemText:  # 현재 선택되어 있다면
                                                line, = matplotlib_axes.plot(
                                                    x_data[lstDataPos],
                                                    y_data[lstDataPos],
                                                    '-o',
                                                    linewidth=0.8,
                                                    drawstyle='steps-post',
                                                    alpha=CFG_Alpha_Selected,
                                                    color=colorsY1[j % len(colorsY1)],
                                                    picker=True, pickradius=5)  # 5 points tolerance
                                                line.set_label(YAttr)  # 'Figure Options' 창에서 Curve이름 표시하기 위해위해
                                                dicGlobalYLineToLegend[line] = Legend
                                                lstGlobalYLine.append(line)

                                            else:
                                                line, = matplotlib_axes.plot(
                                                    x_data[lstDataPos],
                                                    y_data[lstDataPos],
                                                    linewidth=0.8,
                                                    drawstyle='steps-post',
                                                    alpha=CFG_Alpha_Unselected,
                                                    color=colorsY1[j % len(colorsY1)],
                                                    picker=True, pickradius=5)  # 5 points tolerance
                                                line.set_label(YAttr)  # 'Figure Options' 창에서 Curve이름 표시하기 위해위해
                                                dicGlobalYLineToLegend[line] = Legend
                                                lstGlobalYLine.append(line)


                        else:
                            for i, YAttr in enumerate(lstYAttr):
                                if YAttr not in lstLegendY_Selected:

                                    # 셀별로 값 확인하기 위해
                                    if (XAttr == "column_index"):
                                        lstColumn = SPL_dfData.columns.to_list()
                                        x_data = [ (lstColumn.index(YAttr)+random.random()*0.8-0.4) for x in range(len(x_data))]

                                    y_data = SPL_dfData[YAttr].to_numpy()

                                    if YAttr in lstSelectedItemText:  # 현재 선택되어 있다면
                                        line, = matplotlib_axes.plot(
                                            x_data,
                                            y_data,
                                            '-o',
                                            linewidth=0.8,
                                            drawstyle='steps-post',
                                            alpha=CFG_Alpha_Selected,
                                            picker=True, pickradius=5)  # 5 points tolerance
                                        line.set_label(YAttr)  # 'Figure Options' 창에서 Curve이름 표시하기 위해
                                        dicGlobalYLineToLegend[line] = YAttr
                                        lstGlobalYLine.append(line)

                                    else:
                                        line, = matplotlib_axes.plot(
                                            x_data,
                                            y_data,
                                            linewidth=0.8,
                                            drawstyle='steps-post',
                                            alpha=CFG_Alpha_Unselected,
                                            picker=True, pickradius=5)  # 5 points tolerance
                                        line.set_label(YAttr)  # 'Figure Options' 창에서 Curve이름 표시하기 위해위해
                                        dicGlobalYLineToLegend[line] = YAttr
                                        lstGlobalYLine.append(line)














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

                    # 셀별로 값 확인하기 위해서
                    if (XAttr == "column_index"):
                        lstColumn = SPL_dfData.columns.to_list()
                        lstColIndex = []
                        for YAttr in lstY1Attr:
                            lstColIndex.append( lstColumn.index(YAttr) )
                        for YAttr in lstY2Attr:
                            lstColIndex.append( lstColumn.index(YAttr) )
                        lstColIndex.append( min(lstColIndex)-0.5 )
                        lstColIndex.append( max(lstColIndex)+0.5 )
                        x_data = lstColIndex


                    # matpltlib 의 date는 "1970-01-01 00:00:00"는 0.0
                    #                    "2000-01-01 00:00:00"는 10957.000
                    #                    "2100-01-01 00:00:00"는 47482.000 로 표시됨
                    if (    (self.xdata_type == type(datetime.datetime.now()))
                         or (self.xdata_type == type(np.datetime64('2023-03-09')))):
                        x_data = mdates.date2num(x_data)


                    x_max = max(x_data)
                    x_min = min(x_data)
                    x_left, x_right = self.MplWidget.canvas.axes_1.get_xlim()
                    if( (x_right-x_left) > (x_max-x_min)*3 ):
                        # print("x-axis", x_left, x_right, " xdata:", x_min, x_max)
                        width = max(x_data) - min(x_data) # X축 범위 조정 위해
                        self.MplWidget.canvas.axes_1.set_xlim(min(x_data) - width/20, max(x_data) + width/20)

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

        if(self.last_artist == None):

            # 원래 투명도로
            for line in self.dicY1LineToLegend.keys():
                line.set_alpha( CFG_Alpha_Unselected )
            # annotation 삭제
            for annotation in self.lstAnnotation:
                annotation.remove()
            self.lstAnnotation = []

            # 화면 업데이트
            self.MplWidget.canvas.draw()

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

        # pick_event는 1축만 가능
        # (참조) https://stackoverflow.com/questions/55565393/matplotlib-picker-event-on-secondary-y-axis
        # For those who are 'picking' artists while using twinx, pick events are only called for the artists in the top-most axes.


        # On the pick event, find the original line corresponding to the legend
        thisline = event.artist  # artist는 line 임

        if( self.last_artist == None ): #새로 클릭을 했다면

            #새로 클릭을 해서, 이전 annotion 지움
            for annotation in self.lstAnnotation:
                annotation.remove()
            self.lstAnnotation = []

            # 선택되지 않은 것은 투명하게
            for line in self.dicY1LineToLegend.keys():
                line.set_alpha(0.2)

        # annotion 표시
        Annotation_one = self.MplWidget.canvas.axes_1.annotate(self.dicY1LineToLegend[thisline],
                               xy=(event.mouseevent.x, event.mouseevent.y - 20*len( self.lstAnnotation)),
                               xycoords='figure pixels')
        self.lstAnnotation.append(Annotation_one)

        # 선택된것든 진하게
        thisline.set_alpha(1.0)

        # 마우스 버튼 UP 전까지 기억
        self.last_artist = thisline

        # 화면 업데이트
        self.MplWidget.canvas.draw()

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

















