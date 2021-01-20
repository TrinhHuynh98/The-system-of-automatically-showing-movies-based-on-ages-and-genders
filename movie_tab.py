import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget,QVBoxLayout,QTableWidget,QTableWidgetItem,QTableView,QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from database import DB
from movie_create_dialog import Dialog
from movie_update_dialog import Dialog as UpdateDialog
import csv
import os
import shutil
import time
class Table(QTableWidget):
    def __init__(self):
         super(Table, self).__init__()
         self.table = self
         self.update_data()

    def update_data(self):
        db = DB()
        db.connect()
        movies = db.get_all_movie() or []
        db.close()
        numcols = 6
        numrows = len(movies)
        print(movies)
        self.table.setColumnCount(numcols)
        self.table.setRowCount(numrows)
        self.table.setHorizontalHeaderLabels(['ID', 'Name', 'Gender', 'Age from','Age to'])
        self.table.setSelectionBehavior(QTableView.SelectRows)
        for row in range(numrows):
            for column in range(numcols):
                self.table.setItem(row, column, QTableWidgetItem(str(movies[row][column])))
        self.table.doubleClicked.connect(self.on_click)
        self.current_dialog = None
    def on_click(self):
        # #selected cell value.
        index=(self.table.selectionModel().currentIndex())
        #get id column
        movie_id =index.sibling(index.row(),0).data()
        if movie_id!=None:
             self.current_dialog = UpdateDialog(movie_id).exec_()
             print(self.current_dialog)


class Tab(QWidget):
    def __init__(self):
        super(Tab,self).__init__()
        self.layout = QVBoxLayout(self)
        self.table = Table()
        self.layout.addWidget(self.table)

        button_group  = QVBoxLayout()

        self.add_button = QPushButton("ADD")
        self.import_button = QPushButton("IMPROT FROM CSV")
        self.update_button = QPushButton("REFRESH")

        button_group.addWidget(self.add_button)
        button_group.addWidget(self.import_button)
        button_group.addWidget(self.update_button)
        self.layout.addLayout(button_group)
        
        #button click action
        self.add_button.clicked.connect(self.open_add_dialog)
        self.import_button.clicked.connect(self.create_from_csv)
        self.update_button.clicked.connect(self.update_list_movie)

    def open_add_dialog(self):
        Dialog().exec_()

    def update_list_movie(self):
        self.table.update_data()

    def create_from_csv(self):
        filePath =QFileDialog.getOpenFileName(self, 'Open File', '')[0]
        fileFolder = os.path.split(filePath)[0]
        print(fileFolder)
        conn = DB()
        conn.connect()
        if not os.path.exists('movie_images'):
            os.mkdir("movie_images")
            
        with open(filePath) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                print(row[0])
                file = os.path.join(fileFolder,row[0])
                if not os.path.exists(os.path.join(fileFolder,row[0])):
                    print("file {} not found".format(row[0]))
                    continue
                image_name = str(int(time.time()))+row[0]
                shutil.copyfile(file,os.path.join("movie_images",image_name))
                if not os.path.exists(os.path.join("movie_images",image_name)):
                    print("file {} not found".format(image_name))
                    continue
                conn.add_movie(image_name,str(row[1]),str(row[2]),int(row[3]),int(row[4]))
        conn.close()
