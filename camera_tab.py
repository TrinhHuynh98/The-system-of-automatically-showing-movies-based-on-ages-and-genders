from PyQt5.QtWidgets import  QWidget, QLabel, QApplication,QVBoxLayout,QListWidget,QListWidgetItem
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot,Qt,QVariant
from PyQt5.QtGui import QImage, QPixmap
import numpy as np
import os
from imutils.video import VideoStream
import numpy as np
import argparse
import imutils
import time
import cv2
import sys
from database import DB
from config import IMG_SIZE
from models.mobile_net import MobileNetDeepEstimator
from preprocessor import preprocess_input
import tensorflow as tf
MODEL_PATH = os.path.join('model','weights.hdf5')

AGE = 4.76
class MovieWidgetItem (QWidget):
    def __init__ (self, parent = None):
        super(MovieWidgetItem, self).__init__(parent)
        # self.textQVBoxLayout = QtWidgets.QVBoxLayout()
        self.textQLabel    =QLabel()
        # self.textQVBoxLayout.addWidget(self.textQLabel)
        self.allQHBoxLayout  =QVBoxLayout()
        self.iconQLabel      =QLabel()
        self.allQHBoxLayout.addWidget(self.iconQLabel, 0)
        self.allQHBoxLayout.addWidget(self.textQLabel, 1)
        self.setLayout(self.allQHBoxLayout)
        # setStyleSheet
        self.textQLabel.setStyleSheet('''
            color: rgb(0, 0, 255);
        ''')

    def setText (self, text):
        self.textQLabel.setText(text)

    def setIcon (self, imagePath):
        self.iconQLabel.setPixmap(QPixmap(imagePath))

class Thread(QThread):
    changePixmap = pyqtSignal(QImage)
    changeDataMovie =pyqtSignal(object)
    def run(self):
        model = tf.keras.models.load_model(os.path.join('model','model.h5'))
        (H, W) = (None, None) # load our serialized model from disk print("[INFO] loading model...") net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"]) # initialize the video stream and allow the camera sensor to warmup print("[INFO] starting video stream...") vs = VideoStream(src=0).start() time.sleep(2.0)
        # load our serialized model from disk
        print("[INFO] loading model...")
        net = cv2.dnn.readNetFromCaffe(os.path.join('model','deploy.prototxt'),os.path.join('model', 'res10_300x300_ssd_iter_140000.caffemodel'))
        # initialize the video stream and allow the camera sensor to warmup
        print("[INFO] starting video stream...")
        vs = VideoStream(src=0).start()
        time.sleep(2.0)
  
        age = 0
        sex = 0
        # loop over the frames from the video stream
        while True:
            face_deteced = False
            # read the next frame from the video stream and resize it
            frame = vs.read()

            #frame = imutils.resize(frame, width=500)
            frame= cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # if the frame dimensions are None, grab them
            if W is None or H is None:
                (H, W) = frame.shape[:2]

            height, width, channel = frame.shape
            # construct a blob from the frame, pass it through the network,
            # obtain our output predictions, and initialize the list of
            # bounding box rectangles


            blob = cv2.dnn.blobFromImage(frame, 1.0, (W, H),
                (104.0, 177.0, 123.0))
            net.setInput(blob)
            detections = net.forward()
            rects = []
            for i in range(0, detections.shape[2]):
                # filter out weak detections by ensuring the predicted
                # probability is greater than a minimum threshold
                if detections[0, 0, i, 2] > 0.5:
                    face_deteced = True
                    # compute the (x, y)-coordinates of the bounding box for
                    # the object, then update the bounding box rectangles list
                    box = detections[0, 0, i, 3:7] * np.array([W, H, W, H])
                    rects.append(box.astype("int"))

                    # draw a bounding box surrounding the object so we can
                    # visualize it
                    (startX, startY, endX, endY) = box.astype("int")
                    cv2.rectangle(frame, (startX, startY), (endX, endY),
                        (0, 255, 0), 2)
                    try:
                        face = frame[startX:endX,startY:endY]
                        resized_face=cv2.resize(face,(224,224))

                        #img_data = preprocess_input(np.array([resized_face]))

                        sex,age  = model.predict(np.array([resized_face]))
                        gender = ['Male', 'Female']
                        sex = gender[round(sex[0][0])]
                        age = round(age[0][0])


                        res = '{},{}\n'.format(
                                   int(age),
                                   gender)
                        text = "{} - {}".format(sex,age)
                        cv2.putText(frame,text,(startY-10,startY-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    except Exception as e: print(e)
         

            step = channel * width
            qImg = QImage(frame.data, width, height, step, QImage.Format_RGB888)
            p =qImg.scaled(640, 480, Qt.KeepAspectRatio)

            self.changePixmap.emit(p)
            self.changeDataMovie.emit([age,sex])

class Tab(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 Video'
        self.left = 100
        self.top = 100
        self.width = 640
        self.height = 480
        self.initUI()

    @pyqtSlot(QImage)
    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))

    @pyqtSlot(object)
    def setMovieList(self,result):
        age,gender = result
        if age == None or gender ==None :
            return
        conn = DB()
        conn.connect()
        movies = conn.get_movie_by_age_and_gender(age,gender)
        conn.close()
        self.listMovieWidget.clear()
        for _,name,_,_,_,icon in movies:
                # Create QCustomQWidget
            myQCustomQWidget = MovieWidgetItem()
            myQCustomQWidget.setText(name)
            myQCustomQWidget.setIcon(os.path.join("movie_images",icon))
            # Create QListWidgetItem
            myQListWidgetItem =QListWidgetItem(self.listMovieWidget)
            # Set size hint
            myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint())
            # Add QListWidgetItem into QListWidget

            self.listMovieWidget.addItem(myQListWidgetItem)
            self.listMovieWidget.setItemWidget(myQListWidgetItem, myQCustomQWidget)

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.resize(640,480)
        # create a label
        self.layout = QVBoxLayout(self)
        self.listMovieWidget =QListWidget(self)
        self.listMovieWidget.setFlow(QListWidget.LeftToRight)
        self.label = QLabel(self)
        self.label.resize(640, 480)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.listMovieWidget)
        self.setLayout(self.layout)
        th = Thread(self)
        th.changePixmap.connect(self.setImage)
        th.changeDataMovie.connect(self.setMovieList)
        th.start()

