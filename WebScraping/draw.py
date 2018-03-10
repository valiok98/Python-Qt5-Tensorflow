'''ps_draw_circles1.py
draw circles with PySide (public PyQT)
tested with PySide474 and Python27/Python33

take a screen shot (PRTSC key) with
LightShot from
http://app.prntscr.com/
and get an internet link to the display
http://prntscr.com/kw6b6
'''

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class DrawCircles(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        # setGeometry(x_pos, y_pos, width, height)
        self.setGeometry(300, 300, 350, 350)
        self.setWindowTitle('Draw circles')

    def paintEvent(self, event):
        paint = QPainter()
        paint.begin(self)
        # optional
        paint.setRenderHint(QPainter.Antialiasing)
        # make a white drawing background
        paint.setBrush(Qt.white)
        paint.drawRect(event.rect())
        # for circle make the ellipse radii match
        radx = 100
        rady = 100
        # draw red circles
        paint.setPen(Qt.red)
        for k in range(125, 220, 10):
            center = QPoint(k, k)
            # optionally fill each circle yellow
            paint.setBrush(Qt.yellow)
            paint.drawEllipse(center, radx, rady)
        paint.end()

app = QApplication([])
circles = DrawCircles()
circles.show()
app.exec_()