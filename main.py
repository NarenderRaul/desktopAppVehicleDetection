import cv2
from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtCore import *
import sys
from detect import run
import time
import os
import glob
import pandas as pd

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('main.ui', self)

        self.initUI()
        self.mode = 0
        self.setWindowTitle("CoAct")

    def initUI(self):
        self.btnOpenImg = self.findChild(QtWidgets.QPushButton, 'btnOpenImage')
        self.btnOpenImg.clicked.connect(self.OnBtnOpenImg)

        self.btnOpenFolder = self.findChild(QtWidgets.QPushButton, 'btnOpenFolder')
        self.btnOpenFolder.clicked.connect(self.OnBtnOpenFolder)

        self.btnStart = self.findChild(QtWidgets.QPushButton, 'btnStart')
        self.btnStart.clicked.connect(self.OnBtnStart)

        self.editFileName = self.findChild(QtWidgets.QLineEdit, 'editFileName')
        self.label_Progress = self.findChild(QtWidgets.QLabel, 'label_Progress')
        self.imageBox = self.findChild(QtWidgets.QLabel, 'imageBox')

    def OnBtnStart(self):
        if self.mode == 0:
            return
        if self.mode == 1:
            self.ImageStart()
        if self.mode == 2:
            self.FolderStart()

    def FolderStart(self):
        all_detections = {}
        output_file_path = r".\output_excel"
        for filename in glob.glob(os.path.join(self.folderPath, '*.*')):
            retuned_statement = run(filename)
            if retuned_statement[0] == "TRUE":
                values = retuned_statement[1]
                all_detections[filename.split('\\')[-1]] = [i.replace('RHS ', '').replace('LHS ', '') for i in
                                                        values.keys()]
        data = pd.DataFrame.from_dict(all_detections, orient='index').fillna('')
        data.to_csv(os.sep.join([output_file_path, str(self.folderName) + '.csv']))

        self.label_Progress.setText("Complete")

    def ImageStart(self):
        retuned_statement = run(self.filePath)
        if retuned_statement[0] == "TRUE":
            output_path = "./output/" + self.fileName
            output_path_2 = "./output_2/" + self.fileName
            self.image = cv2.imread(output_path)
            if self.image==None:
                self.image = cv2.imread(output_path_2)
            w_scale = self.imageBox.width() / self.image.shape[1]
            h_scale = self.imageBox.height() / self.image.shape[0]

            if w_scale > h_scale:
                imageToDisplay = cv2.resize(self.image,
                                            (int(self.image.shape[1] * h_scale), int(self.image.shape[0] * h_scale)))
            else:
                imageToDisplay = cv2.resize(self.image,
                                            (int(self.image.shape[1] * w_scale), int(self.image.shape[0] * w_scale)))

            imageToDisplay = QtGui.QImage(imageToDisplay.data, imageToDisplay.shape[1], imageToDisplay.shape[0],
                                          imageToDisplay.shape[1] * 3, QtGui.QImage.Format_RGB888).rgbSwapped()
            self.imageBox.setPixmap(QtGui.QPixmap.fromImage(imageToDisplay))

        self.label_Progress.setText("Complete")

    def OnBtnOpenImg(self):
        self.label_Progress.setText("")
        self.filePath, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open image', './', "Image files (*.jpg *.png *.gif)")
        self.fileName = QFileInfo(self.filePath).fileName()

        if self.filePath =="":
            return

        self.mode = 1
        self.editFileName.setText(self.fileName)
        self.image = cv2.imread(self.filePath)

        w_scale = self.imageBox.width() / self.image.shape[1]
        h_scale = self.imageBox.height() / self.image.shape[0]

        if w_scale > h_scale:
            imageToDisplay = cv2.resize(self.image, (int(self.image.shape[1] * h_scale), int(self.image.shape[0] * h_scale)))
        else:
            imageToDisplay = cv2.resize(self.image, (int(self.image.shape[1] * w_scale), int(self.image.shape[0] * w_scale)))

        imageToDisplay = QtGui.QImage(imageToDisplay.data, imageToDisplay.shape[1], imageToDisplay.shape[0],
                                 imageToDisplay.shape[1] * 3, QtGui.QImage.Format_RGB888).rgbSwapped()

        self.imageBox.setPixmap(QtGui.QPixmap.fromImage(imageToDisplay))

    def OnBtnOpenFolder(self):
        self.label_Progress.setText("")
        self.folderPath= QtWidgets.QFileDialog.getExistingDirectory(None, 'Select project folder:', './', QtWidgets.QFileDialog.ShowDirsOnly)

        if self.folderPath == "":
            return

        self.mode = 2
        self.imageBox.clear()

        self.folderName = QFileInfo(self.folderPath).fileName()
        self.editFileName.setText(self.folderName)

    def exit(self):
        QtCore.QCoreApplication.instance().quit()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    app.exec_()