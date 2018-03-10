import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from urllib.request import urlopen as ureq
from bs4 import BeautifulSoup as soup

class Window(QWidget):

    def __init__(self):
        super(Window,self).__init__()

        self.init_gui()

    def paintEvent(self, e):
        pass

    def init_gui(self):



        self.setWindowTitle("Mr Trump's most recent 20 tweets")
        self.show()



base_dictionary = {}

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
        string = []
        for x in parr2.text.split(","):
                string.append(x.split())
        end = []
        for i in string:
            for j in i:
                end.append(j)
        print(end)
        end.append("self")
        for i in end:
            if i not in base_dictionary.keys():
                base_dictionary[i] = 0
            else:
                base_dictionary[i] +=1
        print(parr2.text)
        print(_, "  ---------------------------")
    except:
        print("Cannot parse this tweet")


if __name__ == "__main__":
    app = QApplication(sys.args)
    win = Window()
    sys.exit(app.exec())