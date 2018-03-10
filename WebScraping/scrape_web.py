import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from urllib.request import urlopen as ureq
from bs4 import BeautifulSoup as soup


class Window(QWidget):


    def __init__(self):
        super(Window,self).__init__()

        self.scroll = QScrollArea()
        self.scroll_layout = QVBoxLayout()
        self.scroll_widget = QWidget()
        self.tweets = list()

        self.init_gui()

    def paintEvent(self, e):
        pass

    def init_gui(self):


        self.scroll.setHorizontalScrollBarPolicy(False)
        self.scroll.setVerticalScrollBarPolicy(True)
        self.scroll.setWidgetResizable(True)
        self.scroll.setEnabled(True)

        qs = QScrollBar(self.scroll)

        self.scroll.setMinimumWidth(250)
        self.scroll.setMinimumHeight(250)
        self.scroll.setVerticalScrollBar(qs)

        self.gather_tweets()

        self.scroll_widget.setLayout(self.scroll_layout)
        self.scroll.setWidget(self.scroll_widget)

        hbox = QHBoxLayout()
        hbox.addWidget(self.scroll)
        hbox.addWidget(qs)

        vbox = QVBoxLayout()
        qlabel = QLabel("Donald Trumps latest 20 tweets !")
        qlabel.setFont(QFont('Arial',13))
        vbox.addWidget(qlabel)
        vbox.addLayout(hbox)

        self.setLayout(vbox)
        self.setWindowTitle("Mr Trump's most recent 20 tweets")
        self.show()

    def fill_area(self,text):

        label = QLabel(text)
        my_tmp = QHBoxLayout()
        my_tmp.addWidget(label)

        up = QFrame(self)
        up.setFrameShape(QFrame.StyledPanel)
        up.setLayout(my_tmp)

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(up)
        self.scroll_layout.addWidget(splitter)

    def gather_tweets(self):

        my_url = ureq('https://twitter.com/realDonaldTrump')
        page_html = my_url.read()
        my_url.close()

        page_soup = soup(page_html,'html.parser')

        all_tr = page_soup.findAll("ol", {"id":"stream-items-id"},limit=None)
        current_table = all_tr[0]

        for _,li in enumerate(current_table.find_all('li',class_="js-stream-item")):
            if _ == 200:
                break
            try:
                curr_par =  li.find_all('div')
                curr_par[0].find_all('div')
                parr = curr_par[0].find_all('div')
                parr1 = parr[1].find('div', class_='js-tweet-text-container')
                parr2 = parr1.find('p')

                self.fill_area(parr2.text)
                print(_, "  ---------------------------")
            except:
                print("Cannot parse this tweet")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    sys.exit(app.exec())