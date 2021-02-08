from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import *
from main import Ui

class passUi(QDialog):
    def __init__(self, parent = None):
        super(passUi, self).__init__(parent)

        uic.loadUi('LogIn.ui', self)
        self.initUI()

    def initUI(self):
        self.btnOK = self.findChild(QtWidgets.QPushButton, 'btnOk')
        self.btnOK.clicked.connect(self.OnBtnOK)

        self.btnCancel = self.findChild(QtWidgets.QPushButton, 'btnCancel')
        self.btnCancel.clicked.connect(self.OnBtnCancel)

        self.editPass = self.findChild(QtWidgets.QLineEdit, 'editPass')
        self.editPass.setEchoMode(QLineEdit.Password)

    def OnBtnOK(self):
        if self.editPass.text() == "detect":
            self.accept()

    def OnBtnCancel(self):
        self.exit()

    def exit(self):
        QtCore.QCoreApplication.instance().quit()

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    passUi = passUi()

    if passUi.exec_() == QDialog.Accepted:
        window = Ui()
        window.show()
        sys.exit(app.exec_())