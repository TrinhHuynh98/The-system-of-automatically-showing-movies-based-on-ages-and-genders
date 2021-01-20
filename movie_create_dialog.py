from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog,
QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout,
QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QSpinBox, QTextEdit,
QVBoxLayout,QWidget,QFileDialog,QLabel)
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
from database import DB
import os
import shutil
import time
class Dialog(QDialog):
    NumGridRows = 3
    NumButtons = 4

    def __init__(self):
        super(Dialog, self).__init__()
        self.create_form()
        self.imagePath = None 

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        self.image = QLabel()

        uploadButton =QPushButton('UPLOAD', self)
        mainLayout = QVBoxLayout()

        mainLayout.addWidget(self.image)
        mainLayout.addWidget(uploadButton)
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(buttonBox)

        self.setLayout(mainLayout)
        self.setWindowTitle("Movie information")

        uploadButton.clicked.connect(self.open_image_file)

    def accept(self):
        conn = DB()
        conn.connect()
        name = self.name_edit.text()
        gender = self.genderCbb.currentText()
        age_from = self.age_from_sb.text()
        age_to = self.age_to_sb.text()
        #check os to split
        image_name = str(int(time.time()))
        print(image_name)
        if not os.path.exists('movie_images'):
            os.mkdir("movie_images")
        shutil.copyfile(self.imagePath,os.path.join("movie_images",image_name))
        conn.add_movie(str(image_name),str(name),gender,age_from,age_to)
        conn.close()
        self.close()

    def create_form(self):
        self.formGroupBox = QGroupBox("Movie information")
        self.name_edit = QLineEdit()
        self.genderCbb = QComboBox()
        self.genderCbb.addItems(["male","female","both"])
        self.age_from_sb = QSpinBox()
        self.age_to_sb = QSpinBox()

        layout = QFormLayout()
        layout.addRow(QLabel("Name:"),self.name_edit )
        layout.addRow(QLabel("Gender:"),self.genderCbb)
        layout.addRow(QLabel("Age from:"), self.age_from_sb)
        layout.addRow(QLabel("to:"), self.age_to_sb)
        self.formGroupBox.setLayout(layout)

    def open_image_file(self):
        filename =QFileDialog.getOpenFileName(self, 'Open File')
        self.imagePath = filename[0]
        pixmap =QPixmap(self.imagePath)
        self.image.resize(500, 250)
        self.image.setPixmap(pixmap.scaled(self.image.size(),Qt.IgnoreAspectRatio))
