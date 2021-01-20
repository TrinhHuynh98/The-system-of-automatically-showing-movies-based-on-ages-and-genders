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

    def __init__(self,id):
        super(Dialog, self).__init__()
        self.movie_id = id
        if self.movie_id:
            self.imagePath = None 
            buttonBox = QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Apply | QDialogButtonBox.Cancel)
            buttonBox.button(QDialogButtonBox.Ok).setText("Save")
            buttonBox.button(QDialogButtonBox.Apply).setText("Delete")
            buttonBox.accepted.connect(self.accept)
            buttonBox.rejected.connect(self.reject)
            buttonBox.button(QDialogButtonBox.Apply).clicked.connect(self.delete_movie)

            self.image = QLabel()

            self.create_form()

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
        image_name = str(int(time.time()))
        if not os.path.exists('movie_images'):
            os.mkdir("movie_images")
        shutil.copyfile(self.imagePath,os.path.join("movie_images",image_name))
        conn.update_movie(self.movie_id,str(image_name),str(name),gender,age_from,age_to)
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


        #update information
        conn = DB()
        conn.connect()
        movie=conn.get_movie_by_id(self.movie_id)
        if movie==None:
            return
        self.name_edit.setText(movie[1])

        index = self.genderCbb.findText(movie[2],Qt.MatchFixedString)
        self.genderCbb.setCurrentIndex(index)

        self.age_from_sb.setValue(movie[3])
        self.age_to_sb.setValue(movie[4])

        self.imagePath =os.path.join("movie_images",movie[5])
        pixmap =QPixmap(self.imagePath)
        self.image.resize(500, 250)
        self.image.setPixmap(pixmap.scaled(self.image.size(),Qt.IgnoreAspectRatio))
        conn.close()

    def open_image_file(self):
        filename =QFileDialog.getOpenFileName(self, 'Open File')
        print('Path file :',filename)
        self.imagePath = filename[0]
        pixmap =QPixmap(self.imagePath)
        self.image.resize(500, 250)
        self.image.setPixmap(pixmap.scaled(self.image.size(),Qt.IgnoreAspectRatio))
    def delete_movie(self):
        conn = DB()
        conn.connect()
        conn.delete_movie(self.movie_id)
        conn.close()
        self.close()
