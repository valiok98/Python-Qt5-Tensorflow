import os
import sys
from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
class Window(QWidget):


    def __init__(self):

        super(Window,self).__init__()

        resolution = QDesktopWidget().screenGeometry()

        self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                  (resolution.height() / 2) - (self.frameSize().height() / 2))

        self.label = QLabel(self)
        self.label.setFont(QFont('Arial',20))
        self.text_editor = QTextEdit(self)

        self.open = QPushButton(self)
        self.save = QPushButton(self)
        self.clear = QPushButton(self)

        self.init_ui()

    def init_ui(self):

        self.label.setText("My text field")
        #self.text_editor.setGeometry(60,60)

        vbox = QVBoxLayout()
        vbox.addStretch()
        vbox.addWidget(self.label)
        vbox.addWidget(self.text_editor)


        self.save.setText("Save")
        self.open.setText("Open")
        self.clear.setText("Clear")

        self.save.clicked.connect(self.to_save)
        self.clear.clicked.connect(self.to_clear)
        self.open.clicked.connect(self.to_open)


        hbox = QHBoxLayout()
        hbox.addWidget(self.open)
        hbox.addWidget(self.save)
        hbox.addWidget(self.clear)

        vbox.addLayout(hbox)
        vbox.addStretch()

        self.setLayout(vbox)
        self.setWindowTitle("Notepad+++")
        self.show()

    def to_save(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename = QFileDialog.getSaveFileName(self,'Save Dialog', os.getenv('HOME'),options=options)
        if filename != ('', ''):
            with open(filename[0],'w') as f:
                mytext = self.text_editor.toPlainText()
                f.write(mytext)

    def to_open(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename = QFileDialog.getOpenFileName(self,'Open Dialog', os.getenv('HOME'),options=options)
        if filename != ('', ''):
            with open(filename[0], 'r') as f:
                mytext = f.read()
                self.text_editor.setText(mytext)

    def to_clear(self):
        self.text_editor.clear()
if __name__ == "__main__":

    app = QApplication(sys.argv)
    win = Window()
    sys.exit(app.exec_())