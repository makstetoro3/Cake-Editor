import sqlite3
from viev.connectQt import load

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt
from PIL import Image, ImageDraw
from PyQt5.QtGui import QPixmap


class Setting(QMainWindow):
    def __init__(self, title, pror, new=True):
        super().__init__()
        load(self, 'viev/input.ui')
        self.con = sqlite3.connect('db/dbshka.sqlite')
        self.cur = self.con.cursor()
        self.sts = new
        self.setWindowTitle(f'Настройки {title} яруса')
        self.setWindowModality(Qt.ApplicationModal)
        self.pror = pror
        self.pushButton.clicked.connect(self.save)
        self.pushButton_2.clicked.connect(self.close)
        self.horizontalSlider.setMinimum(20)
        self.horizontalSlider.setMaximum(50)
        self.horizontalSlider.setTickInterval(5)
        self.horizontalSlider.valueChanged.connect(self.siz)
        self.lineEdit.setReadOnly(True)
        self.lineEdit_2.setReadOnly(True)
        self.comboBox.currentIndexChanged.connect(self.change)
        self.comboBox_2.currentIndexChanged.connect(self.change)
        self.mass = 0
        self.price = 0
        if not new:
            self.comboBox.setCurrentText((old := self.pror.yars[title]).comboBox.currentText())
            self.comboBox_2.setCurrentText(old.comboBox_2.currentText())
            self.horizontalSlider.setValue(old.horizontalSlider.value())
            self.title = title
        self.change()

    def siz(self):
        self.label_4.setText(f'Размер: {self.horizontalSlider.value()}')
        self.change()

    def s(self):
        if (ind := self.comboBox_2.currentIndex()) == 0:
            return 25.12 * (self.horizontalSlider.value() / 2) ** 2
        elif ind == 2:
            return 8 * self.horizontalSlider.value() ** 2
        else:
            return 8 * (a := self.horizontalSlider.value()) * (a / 2)

    def change(self):
        plot, pric = self.cur.execute(f"""SELECT plot, price FROM menu
                                  WHERE name = '{self.comboBox.currentText()}'""").fetchall()[0]
        self.mass = float(f'{plot * self.s() / 1000:.2f}')
        self.price = float(f'{self.mass * 10 * pric:.2f}')
        self.lineEdit.setText(f'Цена: {self.price:.2f}')
        self.lineEdit_2.setText(f'Вес: {self.mass} кг')
        im = Image.new("RGB", (300, 240), (255, 255, 255))
        img = ImageDraw.Draw(im)
        if (ind := self.comboBox_2.currentIndex()) == 0:
            img.ellipse(((150 - (val := int(self.horizontalSlider.value() * 1.5)), 120 - val),
                         (150 + val, 120 + val)), '#20155e')
        elif ind == 2:
            img.rectangle(((150 - (val := int(self.horizontalSlider.value() * 1.5)), 120 - val),
                           (150 + val, 120 + val)), '#20155e')
        else:
            img.rectangle(((150 - (val := int(self.horizontalSlider.value() * 1.5)), 120 - int(val / 2)),
                           (150 + val, 120 + int(val / 4 * 3))), '#20155e')
        pix = im.load()
        kis = Image.open(f'type/{self.comboBox.currentText()}t.png')
        kis_pix = kis.load()
        x, y = kis.size
        for i in range(300):
            for j in range(240):
                if pix[i, j] == (32, 21, 94):
                    pix[i, j] = kis_pix[i % x, j % y]
        im.save('temporary/mod.png')
        self.label.setPixmap(QPixmap('temporary/mod.png'))

    def save(self):
        self.pror.save_res(self, self.sts)
        self.close()

    def canle(self):
        self.close()
