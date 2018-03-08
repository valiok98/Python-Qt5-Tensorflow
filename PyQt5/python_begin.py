from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import *
import sys
import os
class Image(QLabel):
    def __init__(self, title, parent):
        super().__init__(title, parent)

    def mouseMoveEvent(self, e):

        if e.buttons() != Qt.LeftButton:
            return

        mimeData = QMimeData()
        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(e.pos() - self.rect().topLeft())

        dropAction = drag.exec_(Qt.MoveAction)
    def mousePressEvent(self, e):
        super().mousePressEvent(e)
        if e.button() == Qt.LeftButton:
            print('press')

class Example(QWidget):


    image_cnt = 0

    def __init__(self):
        super().__init__()


        resolution = QDesktopWidget().screenGeometry()
        self.setGeometry(0, 0, 550, 550)
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



        vbox = QVBoxLayout()
        vbox.addWidget(self.upload, Qt.AlignBottom)
        vbox.addWidget(self.message)
        vbox.addWidget(self.train)

        self.setLayout(vbox)
        self.setWindowTitle('Click or Move')

        self.show()

 
    def openFileNamesDialog(self):    
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()", "","All Files (*);;Python Files (*.py)", options=options)
        for i,file in enumerate(files):
            file = file[::-1]
            file = file.split("/", 1)[0]
            file = file[::-1]
            
            past = os.getcwd()
            os.chdir(os.getcwd() + "/saved_images")
            print(os.getcwd())
            os.rename(past + "/" + file, os.getcwd() + "/" + file)
            os.rename(file,"images{}.png".format(Example.image_cnt))
            Example.image_cnt += 1
            os.chdir(past)

    def dragEnterEvent(self, e):
        e.accept()
    def dropEvent(self, e):


       if e.mimeData().hasUrls:
         e.setDropAction(Qt.CopyAction)
         e.accept()
        # Workaround for OSx dragging and dropping
         for url in e.mimeData().urls():

             fname = str(url.toLocalFile())

             fname = fname[::-1]
             fname = fname.split("/", 1)[0]
             fname = fname[::-1]

             self.fname = fname
             self.load_image()

             past = os.getcwd()
             os.chdir(past + "\saved_images")
             print(os.getcwd())
             if os.path.exists(past + "\\" + self.fname):
                 print("NEWWWWWW")
                 os.rename(past + "\\" + self.fname, os.getcwd() + "\\" + self.fname)
                 os.rename(self.fname, "images{}.png".format(Example.image_cnt))
                 Example.image_cnt+=1
             os.chdir(past)
         else:
            e.ignore()

    def load_image(self):
        """
        Set the image to the pixmap
        :return:
        """
        self.qp = QPainter()

        self.pixmap = QPixmap(self.fname)
        #self.pixmap = self.pixmap.scaled(520,520)
        #pixmap = pixmap.scaledToHeight(300)
        print(os.getcwd())
        self.big_label.setPixmap(self.pixmap)
        self.big_label.show()
        print(self.fname)
        print(self.pixmap.width()," ",self.pixmap.height())
        #self.resize(pixmap.width(), pixmap.height())



    def trigger_up(self):

        self.fileDialog = QFileDialog(self)
        self.fileDialog.show()
        #big_label.setText('Uploaded an image right now')
        

        
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    app.exec_()
