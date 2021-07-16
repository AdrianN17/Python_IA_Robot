from PyQt5 import QtWidgets, uic, QtCore
from PyQt5 import QtCore
from PyQt5.QtGui import  QTextCursor
from PyQt5.QtWidgets import QMessageBox
import sys
import subprocess
import pathlib

from server import server
from ia import ia

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('untitled.ui', self)

        style = open('style.qss').read()

        self.setStyleSheet(style)

        self.btn_iniciar = self.findChild(QtWidgets.QPushButton,"btn_iniciar")
        self.btn_apagar = self.findChild(QtWidgets.QPushButton, "btn_apagar")
        self.btn_abrir = self.findChild(QtWidgets.QPushButton, "btn_abrir")

        self.lb_img = self.findChild(QtWidgets.QLabel, "lb_img")
        self.txt_text = self.findChild(QtWidgets.QTextEdit,"txt_resultados")

        self.btn_iniciar.clicked.connect(self.on_iniciar)
        self.btn_apagar.clicked.connect(self.on_apagar)
        self.btn_abrir.clicked.connect(self.on_abrir)

        self.ia = ia(self.lb_img,self.txt_text)
        self.tcp_server = server(self.ia)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.timer_update)

        self.show()

    def on_iniciar(self):
        self.txt_text.insertPlainText("TCP conexion iniciada \n")
        self.ia.resetear_decision()
        self.timer.start(1000)

        try:
            self.tcp_server.create_thread()
        except TypeError:
            QMessageBox.about(self, "Error", "Ha ocurrido un error al iniciar el socket")

    def on_apagar(self):
        self.txt_text.insertPlainText("TCP conexion apagada \n")
        self.timer.stop()

        try:
            self.tcp_server.delete_thread()
        except TypeError:
            QMessageBox.about(self, "Error", "Ha ocurrido un error al terminar el socket ")

    def timer_update(self):
        self.ia.aplicar_tiempo()
        self.txt_text.moveCursor(QTextCursor.End)

    def on_abrir(self):

        path_file = str(pathlib.Path(__file__).parent.absolute()) + "\Simulador\Proyecto_Robot_IA.exe"
        subprocess.Popen([path_file])


app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()