from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtGui
import sys
import os
from PIL import Image
from shutil import copyfile

class Added_images(QPixmap,QHoverEvent):

    def __init__(self,string):
        QHoverEvent.__init__(self   )
        QPixmap.__init__(self,string)
        self.setMouseTracking(1)
        print("Dsadadad")

    def mouseMoveEvent(self,e):
        # Do your stuff here.
        #print('sdadas')
        pass
    def enterEvent(self, QEvent):
        print(1)
        self.setOpacity(0.5)
    def leaveEvent(self,t):
        print(2)
        self.setOpacity(1.0)



class Example(QWidget):

    pictures = 0

    def __init__(self):
        super().__init__()



        self.scroll = QScrollArea()
        self.special = QWidget()
        self.special_lay = QVBoxLayout()


        self.v_right = QVBoxLayout(self)

        self.label = QLabel(self)
        self.label1 = QLabel(self)


        resolution = QDesktopWidget().screenGeometry()
        self.setGeometry(0, 0, 850, 550)
        self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                  (resolution.height() / 2) - (self.frameSize().height() / 2))



        self.big_label = QLabel(self)
        self.upload = QPushButton(self)
        self.message = QLabel(self)
        self.train = QPushButton(self)

        self.initUI()
    def initUI(self):

        self.setAcceptDrops(True)

        self.upload.setText('upload')
        self.upload.clicked.connect(lambda: self.openFileNamesDialog())
        self.upload.setFont(QFont('Arial', 23))

        self.message.setText('Or simply drag and drop !')
        self.message.setAlignment(Qt.AlignCenter)
        self.message.setFont(QFont('Arial', 23))

        self.train.setText('train')
        self.train.setFont(QFont('Arial', 23))

        left = QFrame(self)
        left.setFrameShape(QFrame.StyledPanel)

        v_left = QVBoxLayout()
        v_left.addWidget(self.upload, Qt.AlignBottom)
        v_left.addWidget(self.message)
        v_left.addWidget(self.train)

        left.setLayout(v_left)

        right = QFrame(self)
        right.setFrameShape(QFrame.StyledPanel)




        self.special.setLayout(self.special_lay)
        self.scroll.setWidgetResizable(True)
        self.scroll.setMinimumHeight(150)
        self.scroll.setWidget(self.special)

        self.labelss = QLabel("dadadssad")




        self.label1.setText("Here are your pictures : " + str(Example.pictures))
        self.label1.setAlignment(Qt.AlignTop)
        self.label1.setFont(QFont('',17))



        self.v_right.addWidget(self.scroll)
        self.v_right.addWidget(self.label1)
        self.v_right.addWidget(self.label)






        right.setLayout(self.v_right)

        right.setMaximumWidth(350)
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left)
        splitter.addWidget(right)
        #splitter.setSizes([500,200])


        vbox1 = QVBoxLayout(self)
        vbox1.addWidget(splitter)




        self.setLayout(vbox1)
        self.setWindowTitle('Click or Move')

        self.show()

 
    def openFileNamesDialog(self):    
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()", "","All Files (*);;Python Files (*.py)", options=options)
        for file in files:

            self.load_and_store(file)

    def dragEnterEvent(self, e):
        e.accept()
    def dropEvent(self, e):

       if e.mimeData().hasUrls:
         e.setDropAction(Qt.CopyAction)
         e.accept()
        # Workaround for OSx dragging and dropping
         for url in e.mimeData().urls():

             file = str(url.toLocalFile())
             self.load_and_store(file)

    def load_image(self,cnt):

        copyfile("images{}.jpg".format(cnt), "images_{}.jpg".format(cnt))
        im = Image.open("images_{}.jpg".format(cnt))
        im.save("images_{}.png".format(cnt))
        pixmaps = Added_images("images_{}.png".format(cnt))
        pixmaps = pixmaps.scaled(200, 200)

        os.remove("images_{}.png".format(cnt))


        tmp = QLabel(self)
        tmp.setPixmap(pixmaps)
        self.special_lay.addWidget(tmp)





    def load_and_store(self,file):

        Example.pictures += 1
        self.label1.setText("Here are your pictures : " + str(Example.pictures))
        new_file_name = file.split(".", 1)[0] + "(1).jpg"
        copyfile(file, new_file_name)

        fname = file[::-1]
        fname = fname.split("/", 1)[0]
        fname = fname[::-1]

        past = os.getcwd()
        new = past + "\\\\saved_images"

        if os.path.exists(new):
            os.chdir(new)
        else:
            os.makedirs(new)
            os.chdir(new)
        os.rename(new_file_name, os.getcwd() + "\\" + fname)
        cnt = 0
        while os.path.exists("images{}.jpg".format(cnt)):
            cnt += 1
        os.rename(fname, "images{}.jpg".format(cnt))

        self.load_image(cnt)


        os.chdir(past)





        
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    app.exec_()
