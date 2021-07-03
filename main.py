from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QImage, QTextCursor
from PyQt5.QtWidgets import QMessageBox
import sys


from server import server
from ia import ia

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('untitled.ui', self)

        self.btn_iniciar = self.findChild(QtWidgets.QPushButton,"btn_iniciar")
        self.btn_apagar = self.findChild(QtWidgets.QPushButton, "btn_apagar")

        self.lb_img = self.findChild(QtWidgets.QLabel, "lb_img")
        self.txt_text = self.findChild(QtWidgets.QTextEdit,"txt_resultados")

        self.txt_text.moveCursor(QTextCursor.End)


        sb = self.txt_text.verticalScrollBar()
        sb.setValue(sb.maximum())

        self.btn_iniciar.clicked.connect(self.on_iniciar)
        self.btn_apagar.clicked.connect(self.on_apagar)

        self.tcp_server = server(ia(self.lb_img,self.txt_text))

        self.show()

    def on_iniciar(self):
        self.txt_text.insertPlainText("TCP conexion iniciada \n")

        try:
            self.tcp_server.create_thread()
        except TypeError:
            QMessageBox.about(self, "Error", "Ha ocurrido un error al iniciar el socket")

    def on_apagar(self):
        self.txt_text.insertPlainText("TCP conexion apagada \n")

        try:
            self.tcp_server.delete_thread()
        except TypeError:
            QMessageBox.about(self, "Error", "Ha ocurrido un error al terminar el socket ")

app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()