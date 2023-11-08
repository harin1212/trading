import sys
import time

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QAxContainer import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
import pandas as pd
import GiExpertControl as giLogin
import GiExpertControl as giJongmokTRShow
import GiExpertControl as giJongmokRealTime
from pythonUI import Ui_MainWindow
from telegram import Telegram

main_ui = Ui_MainWindow()
telegram_bot = Telegram()


class indiWindow(QMainWindow):
    gaejwa_text = ""
    PW_text = ""
    siga_range = ""
    transaction = ""
    tr_data = []
    tr_new_data = []

    # UI 선언
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IndiExample")
        giJongmokTRShow.SetQtMode(True)
        giJongmokTRShow.RunIndiPython()
        giLogin.RunIndiPython()
        giJongmokRealTime.RunIndiPython()
        self.rqidD = {}
        main_ui.setupUi(self)    

        # self.siga()
        # self.tradingUpDown()

        main_ui.pushButton_1.clicked.connect(self.pushButton_1_clicked)
        main_ui.pushButton_2.clicked.connect(self.pushButton_2_clicked)
        main_ui.pushButton_3.clicked.connect(self.pushButton_3_clicked)
        main_ui.pushButton_4.clicked.connect(self.pushButton_4_clicked)
        giJongmokTRShow.SetCallBack('ReceiveData', self.giJongmokTRShow_ReceiveData)
        
        print(giLogin.GetCommState())
        if giLogin.GetCommState() == 0: # 정상
            print("")        
        elif  giLogin.GetCommState() == 1: # 비정상
        #본인의 ID 및 PW 넣으셔야 합니다.
            login_return = giLogin.StartIndi('234114','test0365*','', 'C:\\SHINHAN-i\\indi\\giexpertstarter.exe')
            if login_return == True:
                print("INDI 로그인 정보","INDI 정상 호출")
            else:
                print("INDI 로그인 정보","INDI 호출 실패")                    


    ## 계좌별 잔고 및 주문 체결 조회
    def pushButton_1_clicked(self):
        # 필수 입력
        indiWindow.gaejwa_text = main_ui.textEdit.toPlainText()
        indiWindow.PW_text = main_ui.textEdit_2.toPlainText()

        TR_Name = "SABA200QB"          
        ret = giJongmokTRShow.SetQueryName(TR_Name)         
        ret = giJongmokTRShow.SetSingleData(0,indiWindow.gaejwa_text) #계좌번호
        ret = giJongmokTRShow.SetSingleData(1,"01")  #상품구분
        ret = giJongmokTRShow.SetSingleData(2,indiWindow.PW_text) #비밀번호
        rqid = giJongmokTRShow.RequestData()
        print(type(rqid))
        print('Request Data rqid: ' + str(rqid))
        self.rqidD[rqid] = TR_Name    


    ## 매수신호 조회 - 시가대비 상승율 조회 && 거래량 급등락 종목 조회
    def pushButton_2_clicked(self):
        indiWindow.tr_data = []
        indiWindow.tr_new_data = []
        TR_Name = "TR_1862"
        indiWindow.siga_range = float(main_ui.textEdit_7.toPlainText())
        ret = giJongmokTRShow.SetQueryName(TR_Name)        
        rqid = giJongmokTRShow.RequestData()
        print((rqid))
        print('Request Data rqid: ' + str(rqid))
        self.rqidD[rqid] = TR_Name  

        TR_Name = "TR_1864"    
        transaction = main_ui.textEdit_9.toPlainText()
        ret = giJongmokTRShow.SetQueryName(TR_Name)          
        ret = giJongmokTRShow.SetSingleData(0,"2") #장구분자
        ret = giJongmokTRShow.SetSingleData(1,"3")  #대비급등락 구분
        ret = giJongmokTRShow.SetSingleData(2,"1") #대비율
        ret = giJongmokTRShow.SetSingleData(3, transaction) #거래량 조건
        ret = giJongmokTRShow.SetSingleData(4,"1") #종목조건
        ret = giJongmokTRShow.SetSingleData(5,"0") #시가총액조건
        rqid = giJongmokTRShow.RequestData()
        print(type(rqid))
        print('Request Data rqid: ' + str(rqid))
        self.rqidD[rqid] = TR_Name


    ## 뉴스제목 목록조회
    def pushButton_4_clicked(self):
        news_code = main_ui.textEdit_8.toPlainText()
        news_date = main_ui.calendarWidget.selectedDate().toString("yyyyMMdd")
        print(news_date)
        TR_Name = "TR_3100_D"    
        ret = giJongmokTRShow.SetQueryName(TR_Name)          
        ret = giJongmokTRShow.SetSingleData(0,news_code) #뉴스_종목코드
        ret = giJongmokTRShow.SetSingleData(1,"1")  #구분
        ret = giJongmokTRShow.SetSingleData(2,news_date) #조회일자
        print(giJongmokTRShow.GetErrorMessage())
        rqid = giJongmokTRShow.RequestData()
        print(type(rqid))
        print('Request Data rqid: ' + str(rqid))
        self.rqidD[rqid] = TR_Name


    ## 현물 일반 주문(매수/매도)
    def pushButton_3_clicked(self):
        TR_Name = "SABA101U1"
        jongmok_code = str(main_ui.textEdit_10.toPlainText())
        count = str(main_ui.spinBox.value())
        
        selected_comboBox_2 = main_ui.comboBox_2.currentIndex()
        if selected_comboBox_2 == 0:
            buySell = "2" #매수
        elif selected_comboBox_2 == 1:
            buySell = "1" #매도

        selected_comboBox = main_ui.comboBox.currentIndex()
        if selected_comboBox == 0:
            hoga = "1" #시장가
            price = ""
        elif selected_comboBox == 1:
            hoga = "2" #지정가
            price = str(main_ui.spinBox_2.value())

        print(indiWindow.gaejwa_text)
        print(indiWindow.PW_text)
        print("jongmok_code", jongmok_code)
        print("count",count)
        print("selected_comboBox_2",selected_comboBox_2)
        print("buySell",buySell)
        print("selected_comboBox",selected_comboBox)
        print("hoga",hoga)
        print("price",price)

        ret = giJongmokTRShow.SetQueryName(TR_Name)          
        ret = giJongmokTRShow.SetSingleData(0,indiWindow.gaejwa_text) #계좌번호
        ret = giJongmokTRShow.SetSingleData(1,"01")  #계좌상품
        ret = giJongmokTRShow.SetSingleData(2,indiWindow.PW_text) #계좌비번
        ret = giJongmokTRShow.SetSingleData(3,"") 
        ret = giJongmokTRShow.SetSingleData(4,"") 
        ret = giJongmokTRShow.SetSingleData(5,"0") #선물대용매도여부
        ret = giJongmokTRShow.SetSingleData(6,"00") #신용거래구분
        ret = giJongmokTRShow.SetSingleData(7, buySell) #매도/매수
        ret = giJongmokTRShow.SetSingleData(8, jongmok_code) #종목코드
        ret = giJongmokTRShow.SetSingleData(9, count) #주문 수량
        ret = giJongmokTRShow.SetSingleData(10, price) #주문 가격
        ret = giJongmokTRShow.SetSingleData(11, "1") #정규시간외구분코드
        ret = giJongmokTRShow.SetSingleData(12, hoga) #호가유형코드
        ret = giJongmokTRShow.SetSingleData(13,"0") #주문조건코드
        ret = giJongmokTRShow.SetSingleData(14,"0") #신용대출통합주문구분코드
        ret = giJongmokTRShow.SetSingleData(15,"") #신용대출일자
        ret = giJongmokTRShow.SetSingleData(16,"") #원주문번호
        ret = giJongmokTRShow.SetSingleData(17,"")
        ret = giJongmokTRShow.SetSingleData(18,"")
        ret = giJongmokTRShow.SetSingleData(19,"")
        ret = giJongmokTRShow.SetSingleData(20,"") #프로그램매매여부
        ret = giJongmokTRShow.SetSingleData(21,"Y") #결과메시지 처리여부
        rqid = giJongmokTRShow.RequestData()
        print("rqid",rqid)
        print('Request Data rqid: ' + str(rqid))
        print(giJongmokTRShow.GetErrorMessage())
        self.rqidD[rqid] = TR_Name



    ## 받는 데이터
    def giJongmokTRShow_ReceiveData(self,giCtrl,rqid):
        print("in receive_Data:", rqid)
        print('recv rqid: {}->{}\n'.format(rqid, self.rqidD[rqid]))
        TR_Name = self.rqidD[rqid]
        tr_data_output = []
        output = []
        print("TR_name : ",TR_Name)


        if TR_Name == "SABA200QB":
            nCnt = giCtrl.GetMultiRowCount()
            print("nCnt", nCnt)
            for i in range(0, nCnt):
                tr_data_output.append([])
                main_ui.tableWidget.setItem(i,0,QTableWidgetItem(str(giCtrl.GetMultiData(i, 0))))
                main_ui.tableWidget.setItem(i,1,QTableWidgetItem(str(giCtrl.GetMultiData(i, 1))))
                main_ui.tableWidget.setItem(i,2,QTableWidgetItem(str(giCtrl.GetMultiData(i, 2))))
                main_ui.tableWidget.setItem(i,3,QTableWidgetItem(str(giCtrl.GetMultiData(i, 5))))
                main_ui.tableWidget.setItem(i,4,QTableWidgetItem(str(giCtrl.GetMultiData(i, 6))))
                for j in range(0,5):
                    tr_data_output[i].append(giCtrl.GetMultiData(i, j))
            print(type(tr_data_output))


        if TR_Name == "TR_1862":
            nCnt = giCtrl.GetMultiRowCount()            
            print("nCnt : ",nCnt)
            print(giJongmokTRShow.GetErrorMessage())
            print("siga_range", (indiWindow.siga_range))
            for i in range(0, nCnt):
                if (float(giCtrl.GetMultiData(i, 4)) > indiWindow.siga_range) :
                    indiWindow.tr_data.append({
                        "단축코드": str(giCtrl.GetMultiData(i, 0)),
                        "한글종목명": str(giCtrl.GetMultiData(i, 1)),
                        "현재가": str(giCtrl.GetMultiData(i, 2)),
                        "시가": str(giCtrl.GetMultiData(i, 3)),
                        "시가대비상승율": str(giCtrl.GetMultiData(i, 4))
                    })
                else :
                    indiWindow.tr_data[i] = []
            print(indiWindow.tr_data)
            print(giJongmokTRShow.GetErrorMessage())
            # time.sleep(3)
          
          
        if TR_Name == "TR_1864":
            nCnt = giCtrl.GetMultiRowCount()
            print("nCnt : ", nCnt)
            for i in range(0, nCnt):
                # 두 TR(TR_1862, TR_1864) 단축코드 필터링
                for j in range(0, len(indiWindow.tr_data)):
                    if indiWindow.tr_data[j]["단축코드"] == str(giCtrl.GetMultiData(i, 1)):
                        print("str(giCtrl.GetMultiData(i, 1))", str(giCtrl.GetMultiData(i, 1)))
                        print(j)
                        print(indiWindow.tr_data[j]["단축코드"])
                        print(str(giCtrl.GetMultiData(i, 1)))
                        indiWindow.tr_new_data.append({
                            "단축코드": indiWindow.tr_data[j]["단축코드"],
                            "한글종목명": indiWindow.tr_data[j]["한글종목명"],
                            "현재가": indiWindow.tr_data[j]["현재가"],
                            "시가": indiWindow.tr_data[j]["시가"],
                            "시가대비상승율": indiWindow.tr_data[j]["시가대비상승율"],
                            "누적거래량": str(giCtrl.GetMultiData(i, 7)),
                            "급증률": str(giCtrl.GetMultiData(i, 8))
                        })
            print(giJongmokTRShow.GetErrorMessage())
            print("tr_new_data",indiWindow.tr_new_data)
            telegram_bot.sendMessage(str(indiWindow.tr_new_data[0]))
            telegram_bot.sendMessage(str(indiWindow.tr_new_data[1]))
            for k in range(0, 10):
                main_ui.tableWidget_2.setItem(k,0,QTableWidgetItem(str(indiWindow.tr_new_data[k]["단축코드"]))) #단축코드
                main_ui.tableWidget_2.setItem(k,1,QTableWidgetItem(str(indiWindow.tr_new_data[k]["한글종목명"]))) #한글종목명
                main_ui.tableWidget_2.setItem(k,2,QTableWidgetItem(str(indiWindow.tr_new_data[k]["현재가"]))) #현재가
                main_ui.tableWidget_2.setItem(k,3,QTableWidgetItem(str(indiWindow.tr_new_data[k]["시가"]))) #시가
                main_ui.tableWidget_2.setItem(k,4,QTableWidgetItem(str(indiWindow.tr_new_data[k]["시가대비상승율"]))) #시가대비상승율
                main_ui.tableWidget_2.setItem(k,5,QTableWidgetItem(str(indiWindow.tr_new_data[k]["누적거래량"]))) #누적거래량
                main_ui.tableWidget_2.setItem(k,6,QTableWidgetItem(str(indiWindow.tr_new_data[k]["급증률"]))) #급증률


        if TR_Name == "TR_3100_D" :
            nCnt = giCtrl.GetMultiRowCount()
            print("nCnt : ", nCnt)
            print(giJongmokTRShow.GetErrorMessage())
            for i in range(0, nCnt):
                main_ui.tableWidget_3.setItem(i,0,QTableWidgetItem(str(giCtrl.GetMultiData(i, 4)))) #뉴스_기사번호
                main_ui.tableWidget_3.setItem(i,1,QTableWidgetItem(str(giCtrl.GetMultiData(i, 2)))) #뉴스_제목


        if TR_Name == "SABA101U1":
            nCnt = giCtrl.GetSingleRowCount()
            print("nCnt : ",nCnt)
            main_ui.label_9.setText(str(giCtrl.GetSingleData(3)))
            telegram_bot.sendMessage(str(giCtrl.GetSingleBlockData(0)))
            

        


     
if __name__ == "__main__":
    app = QApplication(sys.argv)
    IndiWindow = indiWindow()    
    IndiWindow.show()
    font = QFont("나눔고딕", 10)
    app.setFont(font)
    app.exec_()

    # if IndiWindow.MainSymbol != "":
    #     giJongmokRealTime.UnRequestRTReg("SC", "")

