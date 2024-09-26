import sys
from PyQt6 import QtCore, QtGui, QtWidgets, QtTest
from PyQt6.QtCore import QRunnable, QThreadPool
import time
import glob
import os
import subprocess
from chemcrow.agents import ChemCrow
import random

log = open("./logs/log-file.txt","w")
sys.stdout = log
sys.stderr = log

m=glob.glob("./llm/*.gguf")
models_list=["gpt-3.5-turbo","gpt-4-0613"]
for items in m: #load model from llm folder
    mm=items.replace("./llm\\",'')
    models_list.append(mm)

class Worker(QRunnable):
    def __init__(self, gui):  # Accept the instance of Ui_ChemQ
        super().__init__()
        self.gui = gui

    def run(self): #model function

        model=self.gui.model.currentText()
        
        if not model.startswith("gpt-"):
            model="./llm/"+model
            model=model.strip()
            chem_model = ChemCrow(
                model=model,
                tools_model=model,
                temp=self.gui.temp.value(), verbose=False, max_tokens=100, n_ctx=2048
            )

        else:
            api_key = self.gui.api.text()

            if api_key == "0": #api codes #skip api key
                chem_model = ChemCrow(model=model, temp=self.gui.temp.value())

            elif api_key.startswith("sk-"): #api set and apply
                f = open("./batch.bat","r") 
                lines = f.readlines()
                f.close()
                f = open("./batch.bat","w")
                lines[8] = "setx OPENAI_API_KEY "+api_key+" /m\n"
                f.writelines(lines)
                f.close()
                p=subprocess.Popen("batch.bat",cwd=r"./")
                stdout, stderr = p.communicate()
                time.sleep(5)
                chem_model = ChemCrow(model=model, temp=self.gui.temp.value())

            else: #api error
                self.gui.fn.setChecked(False)
                self.gui.api.setStyleSheet("color: rgb(219, 24, 73);")
                self.gui.api.setText("Invalid API")
                self.gui.api.setDisabled(True)
                globals()['state'] = 1
                QtTest.QTest.qWait(2500)
                self.gui.api.clear()
                self.gui.api.setStyleSheet("color: rgb(192, 191, 188);")
                self.gui.api.setDisabled(False)
                return

        y=self.gui.prompt.text()
        x=str(chem_model.run(y)) #response
        globals()['state'] = 1
        time.sleep(1)
        self.gui.prompt.clear()

        out="    >>>  "+y+"\n\n"+"    ^^^  "+x+"\n\n"

        html_content = """
        <span style="color: rgb(3, 182, 252);">&nbsp;>>>&nbsp;</span>
        <span style="color: rgb(222, 221, 218);">{y}</span>
        <span style="color: rgb(3, 252, 140);"><br><br>&nbsp;^^^&nbsp;</span>
        <span style="color: rgb(222, 221, 218);">{x}<br><br><br></span>
        """.format(y=y, x=x)
        self.gui.response.append(html_content)
        self.gui.fn.setChecked(False)
        handle=open("./chats/chat.txt","a")
        handle.write(out)
        handle.close()

class Ui_ChemQ(object):

    def setupUi(self, ChemQ):
        super().__init__()

        ChemQ.setObjectName("ChemQ")
        ChemQ.resize(964, 641)
        ChemQ.setFixedSize(964, 641)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ChemQ.sizePolicy().hasHeightForWidth())
        ChemQ.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("assets/main-logo.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        icon.addPixmap(QtGui.QPixmap("assets/main-logo.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.On)
        ChemQ.setWindowIcon(icon)
        ChemQ.setStyleSheet("background-color: rgb(33, 33, 33);\n"
"color: rgb(192, 191, 188);\n"
"font: 10pt \"Nimbus Mono PS\";")
        ChemQ.setTabShape(QtWidgets.QTabWidget.TabShape.Rounded)
        self.centralwidget = QtWidgets.QWidget(parent=ChemQ)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(parent=self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(260, 0, 701, 585))
        self.tabWidget.setStatusTip("")
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.TabPosition.East)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.TabShape.Rounded)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setStatusTip("")
        self.tab.setObjectName("tab")
        self.response = QtWidgets.QTextBrowser(parent=self.tab)
        self.response.setGeometry(QtCore.QRect(0, 0, 665, 521))
        self.response.setObjectName("response")
        self.prompt = QtWidgets.QLineEdit(parent=self.tab)
        self.prompt.setGeometry(QtCore.QRect(10, 526, 591, 51))
        self.prompt.setStyleSheet("background-color: rgb(222, 221, 218);\n"
"color: rgb(33, 33, 33);\n"
"font: 14pt \"Nimbus Mono PS\";")
        self.prompt.setObjectName("prompt")
        self.fn = QtWidgets.QPushButton(parent=self.tab)
        self.fn.setGeometry(QtCore.QRect(610, 526, 51, 51))
        self.fn.setWhatsThis("")
        self.fn.setStyleSheet("background-color: rgb(222, 221, 218);")
        self.fn.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("assets/srart.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        icon1.addPixmap(QtGui.QPixmap("assets/stop.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.On)
        self.fn.setIcon(icon1)
        self.fn.setIconSize(QtCore.QSize(28, 28))
        self.fn.setShortcut("")
        self.fn.setCheckable(True)
        self.fn.setChecked(False)
        self.fn.setObjectName("fn")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.response_2 = QtWidgets.QTextBrowser(parent=self.tab_2)
        self.response_2.setGeometry(QtCore.QRect(0, 0, 665, 581))
        self.response_2.setObjectName("response_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.label_model = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_model.setGeometry(QtCore.QRect(10, 40, 51, 19))
        self.label_model.setObjectName("label_model")
        self.label_api = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_api.setGeometry(QtCore.QRect(10, 140, 101, 19))
        self.label_api.setObjectName("label_api")
        self.label_temp = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_temp.setGeometry(QtCore.QRect(10, 240, 111, 19))
        self.label_temp.setObjectName("label_temp")
        self.model = QtWidgets.QComboBox(parent=self.centralwidget)
        self.model.setGeometry(QtCore.QRect(50, 70, 200, 27))
        self.model.setObjectName("model")
        self.api = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.api.setGeometry(QtCore.QRect(50, 170, 200, 27))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.api.sizePolicy().hasHeightForWidth())
        self.api.setSizePolicy(sizePolicy)
        self.api.setStyleSheet("background-color: rgb(50, 50, 50);")
        self.api.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.api.setObjectName("api")
        self.temp = QtWidgets.QDoubleSpinBox(parent=self.centralwidget)
        self.temp.setGeometry(QtCore.QRect(170, 270, 80, 27))
        self.temp.setMaximum(2.0)
        self.temp.setSingleStep(0.1)
        self.temp.setProperty("value", 0.3)
        self.temp.setObjectName("temp")
        self.logo = QtWidgets.QLabel(parent=self.centralwidget)
        self.logo.setGeometry(QtCore.QRect(10, 490, 249, 91))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.logo.sizePolicy().hasHeightForWidth())
        self.logo.setSizePolicy(sizePolicy)
        self.logo.setToolTip("")
        self.logo.setToolTipDuration(-1)
        self.logo.setAutoFillBackground(False)
        self.logo.setText("")
        self.logo.setPixmap(QtGui.QPixmap("assets/logo-cc.png"))
        self.logo.setScaledContents(True)
        self.logo.setWordWrap(False)
        self.logo.setObjectName("logo")
        ChemQ.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=ChemQ)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 964, 26))
        self.menubar.setObjectName("menubar")
        self.menuHelp = QtWidgets.QMenu(parent=self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        ChemQ.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=ChemQ)
        self.statusbar.setObjectName("statusbar")
        ChemQ.setStatusBar(self.statusbar)
        self.actionHelp = QtGui.QAction(parent=ChemQ)
        self.actionHelp.setObjectName("actionHelp")
        self.menuHelp.addAction(self.actionHelp)
        self.menubar.addAction(self.menuHelp.menuAction())
        self.retranslateUi(ChemQ)
        self.tabWidget.setCurrentIndex(0)
        self.fn.clicked.connect(self.stop)
        self.fn.clicked.connect(self.start)
        self.fn.clicked.connect(self.running_show)
        self.model.currentIndexChanged.connect(self.index_check) # type: ignore
        self.menuHelp.triggered['QAction*'].connect(self.help) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(ChemQ)

        for items in models_list: #load model in combobox

            self.model.addItem(items)

    def index_check(self): #api disable function

        if self.model.currentIndex() != 0 and self.model.currentIndex() != 1:
            self.api.setDisabled(True)
            self.api.clear()

        else:
            self.api.setDisabled(False)

    def stop(self):
        if not self.fn.isChecked():
            print("you terminated the process.")
            log.close()
            exit()

    def start(self):
        self.worker = Worker(self)  # Pass the instance of Ui_ChemQ
        QThreadPool.globalInstance().start(self.worker)

    def running_show(self):
        
        globals()['state'] = 0
        if self.fn.isChecked():
            c=1

            while globals()['state'] == 0:
                app.processEvents()
                l=["/","-","\\","|"]
                index=c%4
                c+=1
                I=l[index]
                R=random.randint(0,255)
                G=random.randint(0,255)
                B=random.randint(0,255)
                html_content = """
                <span style="color: rgb(200,200,200);"><br><br><br><br>&nbsp;<b>Running...<b></span><span style="color: rgb({R}, {G}, {B});">&nbsp;&nbsp;&nbsp;&nbsp;{I}{I}{I}&nbsp;</span>
                """.format(R=R,G=G,B=B,I=I)
                time.sleep(0.15)
                self.response.setText(html_content)

                if state == 1:
                    self.response.clear()

    def help(self):
        path = "README.md"
        os.startfile(path)

    def retranslateUi(self, ChemQ):
        _translate = QtCore.QCoreApplication.translate
        ChemQ.setWindowTitle(_translate("ChemQ", "Chem.Q"))
        self.response.setStatusTip(_translate("ChemQ", "answers will be here"))
        self.prompt.setStatusTip(_translate("ChemQ", "enter your prompt here"))
        self.fn.setStatusTip(_translate("ChemQ", "run"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("ChemQ", "Ai"))
        self.response_2.setStatusTip(_translate("ChemQ", "logs"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("ChemQ", "Log"))
        self.label_model.setText(_translate("ChemQ", "Model"))
        self.label_api.setText(_translate("ChemQ", "OpenAI API"))
        self.label_temp.setText(_translate("ChemQ", "Temperature"))
        self.model.setStatusTip(_translate("ChemQ", "select your model | you shall copy your local model to llm folder"))
        self.api.setStatusTip(_translate("ChemQ", "starts with sk-*** | if you want use gpt you need this"))
        self.temp.setStatusTip(_translate("ChemQ", "raise to make different answers | lower for more accurate"))
        self.logo.setStatusTip(_translate("ChemQ", "https://github.com/ur-whitelab/chemcrow-public"))
        self.menuHelp.setStatusTip(_translate("ChemQ", "menu"))
        self.fn.setShortcut(_translate("Form", "Return"))
        self.menuHelp.setTitle(_translate("ChemQ", "Menu"))
        self.actionHelp.setText(_translate("ChemQ", "Help"))

gui = Ui_ChemQ

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ChemQ = QtWidgets.QMainWindow()
    ui = Ui_ChemQ()
    ui.setupUi(ChemQ)
    ChemQ.show()
    sys.exit(app.exec())
log.close()