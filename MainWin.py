import sys
import sqlite3
from viev.connectQt import load
import csv

from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QHeaderView, QPushButton, QGroupBox
from PyQt5.QtWidgets import QInputDialog, QMessageBox, QApplication, QVBoxLayout, QLabel, QFileDialog
from PyQt5.QtGui import QPixmap
from math import ceil
from PIL import Image, ImageDraw
from xlsxwriter.workbook import Workbook

from Cry import Setting
from main import Singing
from zak import Zaking


class MyWidget(QMainWindow):
    def __init__(self):
        global sin
        self.user = -1
        sin = Singing()
        sin.op(self)
        sin.show()
        super().__init__()
        load(self, 'viev/01.ui')
        self.con = sqlite3.connect('db/dbshka.sqlite')
        self.cur = self.con.cursor()
        self.lineEdit.setReadOnly(True)
        self.lineEdit_2.setReadOnly(True)
        self.change_login.clicked.connect(self.lodi)
        self.pushButton_2.clicked.connect(self.pasw)
        self.pushButton_4.clicked.connect(self.out)
        self.tabWidget.currentChanged.connect(self.tabs)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.svoystv.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget_3.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget_3.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.lineprice.setReadOnly(True)
        self.lineEdit_3.setReadOnly(True)
        self.add_sloy.clicked.connect(self.app)
        self.delet_sloy.clicked.connect(self.delete)
        self.pushButton_3.clicked.connect(self.clear)
        self.bye.clicked.connect(self.zak)
        self.pushButton_5.clicked.connect(self.save_table)
        self.pushButton.clicked.connect(self.save_table_to_css)
        self.pushButton_6.clicked.connect(self.check)
        self.yars = []
        self.mass = 0
        self.price = 0

        catal = self.cur.execute('SELECT id, name FROM catal').fetchall()
        self.tableWidget_3.setColumnCount(3)
        self.tableWidget_3.setRowCount(ceil(len(catal) / 3))
        for i in enumerate(catal):
            lay = QVBoxLayout()
            img = QLabel()
            img.setPixmap(QPixmap(f'catalog/{i[1][0]}.png'))
            lay.addWidget(img)
            btn = QPushButton(f'{i[1][1]}\nзаказать')
            btn.clicked.connect(self.zak_cat)
            lay.addWidget(btn)
            box = QGroupBox()
            box.setLayout(lay)
            self.tableWidget_3.setCellWidget(i[0] // 3, i[0] % 3, box)

    def check(self):
        if (row := self.tableWidget.currentRow()) == -1:
            return
        name = self.tableWidget.item(row, 0).text().split()
        if (pute := QFileDialog.getSaveFileName(self, "сохранить", ' '.join(name), "(*.txt)")[0]) == '':
            return
        with open(pute, 'w') as file:
            file.write(
                f'''------------------
Название: {name[0]}
Вес: {name[1]}
Цена: {self.tableWidget.item(row, 1).text()}
Время: {self.tableWidget.item(row, 2).text()}
Место: {self.tableWidget.item(row, 3).text()}
------------------'''
            )

    def save_table(self):
        if (file := QFileDialog.getSaveFileName(self, "сохранить", 'заказы', "(*.xlsx)")[0]) == '':
            return
        workbook = Workbook(file)
        worksheet = workbook.add_worksheet()
        for i, row in enumerate(self.cur.execute(f'''SELECT name, price, data, move FROM zak
        WHERE id_user = "{self.user}"''').fetchall()):
            for j, value in enumerate(row):
                worksheet.write(i, j, row[j])
        workbook.close()

    def save_table_to_css(self):
        if (a := QFileDialog.getSaveFileName(self, "сохранить", 'заказы', "(*.csv)")[0]) == '':
            return
        with open(a, 'w') as file:
            writer = csv.writer(file)
            writer.writerow(['Название', 'Цена', 'Дата', 'Место'])
            writer.writerows(self.cur.execute(f'''SELECT name, price, data, move FROM zak
        WHERE id_user = "{self.user}"''').fetchall())

    def zak_cat(self):
        global re
        name = self.sender().text().split('\n')[0]
        mass, price = self.cur.execute(f'''SELECT mass, price FROM catal
                                             WHERE name = "{name}"''').fetchall()[0]
        re = Zaking(name, mass, price, self.user)
        re.show()

    def zak(self):
        global re
        if len(self.yars) > 0:
            re = Zaking(self.yars[0].comboBox.currentText(), self.mass, self.price, self.user)
            re.show()

    def change(self):
        self.mass = 0
        for i in self.yars:
            self.mass += i.mass
        self.price = 0
        for i in self.yars:
            self.price += i.price
        self.lineEdit_3.setText('Вес: ' + str(self.mass) + ' кг')
        self.lineprice.setText('Стоимость: ' + str(self.price))
        im = Image.new("RGB", (300, 240), (255, 255, 255))
        img = ImageDraw.Draw(im)
        for elem in self.yars:
            if (ind := elem.comboBox_2.currentIndex()) == 0:
                img.ellipse(((150 - (val := int(elem.horizontalSlider.value() * 1.5)), 120 - val),
                             (150 + val, 120 + val)), '#20155e')
            elif ind == 2:
                img.rectangle(((150 - (val := int(elem.horizontalSlider.value() * 1.5)), 120 - val),
                               (150 + val, 120 + val)), '#20155e')
            else:
                img.rectangle(((150 - (val := int(elem.horizontalSlider.value() * 1.5)), 120 - int(val / 2)),
                               (150 + val, 120 + int(val / 4 * 3))), '#20155e')
            pix = im.load()
            kis = Image.open(f'type/{elem.comboBox.currentText()}t.png')
            kis_pix = kis.load()
            x, y = kis.size
            for i in range(300):
                for j in range(240):
                    if pix[i, j] == (32, 21, 94):
                        pix[i, j] = kis_pix[i % x, j % y]
        im.save('temporary/top.png')
        self.label.setPixmap(QPixmap('temporary/top.png'))
        im = Image.new("RGB", (300, 240), (255, 255, 255))
        img = ImageDraw.Draw(im)
        for num, elem in enumerate(self.yars):
            img.rectangle(((150 - (val := int(elem.horizontalSlider.value() * 1.5)), 200 - 20 * num),
                           (150 + val, 220 - 20 * num)), '#20155e')
            pix = im.load()
            kis = Image.open(f'type/{elem.comboBox.currentText()}.png')
            kis_pix = kis.load()
            x, y = kis.size
            for i in range(300):
                for j in range(240):
                    if pix[i, j] == (32, 21, 94):
                        pix[i, j] = kis_pix[i % x, j % y]
        im.save('temporary/bok.png')
        self.visiual_tort.setPixmap(QPixmap('temporary/bok.png'))

    def clear(self):
        msgbox = QMessageBox()
        msgbox.setWindowTitle('Очистка')
        msgbox.setText('Очистить?')
        msgbox.addButton('Нет', QMessageBox.NoRole)
        msgbox.addButton('Да', QMessageBox.YesRole)
        msgbox.setIcon(QMessageBox.Question)
        ok = msgbox.exec()
        if not ok:
            return
        self.svoystv.setRowCount(0)
        self.yars = []
        self.change()

    def delete(self):
        if (cou := self.svoystv.rowCount()) > 0 and (curr := self.svoystv.currentRow()) != -1:
            if cou - curr > 1:
                for i in range(curr, cou - 1):
                    self.svoystv.cellWidget(i + 1, 1).setText(f'Настроить {i + 1} ярус')
            self.svoystv.removeRow(curr)
            self.yars.pop(curr)
            self.change()

    def use(self, us):
        self.user = us[0]
        self.lineEdit_2.setText('Логин: ' + str(us[1]))
        self.lineEdit.setText('Пароль: ' + str(us[2]))

    def app(self):
        global ed
        ed = Setting(len(self.yars) + 1, self)
        ed.show()

    def save_res(self, res, new):
        if new:
            self.yars.append(res)
            self.svoystv.setRowCount((cou := self.svoystv.rowCount()) + 1)
            self.svoystv.setItem(cou, 0, QTableWidgetItem(res.comboBox.currentText()))
            btn = QPushButton(f'Настроить {cou + 1} ярус', self)
            btn.clicked.connect(self.setting)
            self.svoystv.setCellWidget(cou, 1, btn)
        else:
            self.yars[res.title] = res
        self.change()

    def setting(self):
        global ed
        ed = Setting(int(self.sender().text().split()[1]) - 1, self, False)
        ed.show()

    def lodi(self):
        new, ok_pressed = QInputDialog.getText(self, "Введите имя", "Введите новый логин")
        if not ok_pressed:
            return
        self.lineEdit_2.setText('Логин: ' + new)
        self.cur.execute(f'''UPDATE user SET name = '{new}' WHERE id = "{self.user}"''')
        self.con.commit()

    def tabs(self):
        if 2 == self.tabWidget.currentIndex():
            self.tableWidget.setRowCount(len(item := self.cur.execute(f'''SELECT name, price, data, move FROM zak
            WHERE id_user = "{self.user}"''').fetchall()))
            for i in enumerate(item):
                for j in enumerate(i[1]):
                    self.tableWidget.setItem(i[0], j[0], QTableWidgetItem(str(j[1])))

    def pasw(self):
        new, ok_pressed = QInputDialog.getText(self, "Введите пароль", "Введите новый пароль")
        if not ok_pressed:
            return
        self.lineEdit.setText('Пароль: ' + new)
        self.cur.execute(f'''UPDATE user SET password = '{new}' WHERE id = {self.user}''')
        self.con.commit()

    def out(self):
        global ma
        msgbox = QMessageBox()
        msgbox.setWindowTitle('Выход')
        msgbox.setText('Выйти?')
        msgbox.addButton('Нет', QMessageBox.NoRole)
        msgbox.addButton('Да', QMessageBox.YesRole)
        msgbox.setIcon(QMessageBox.Question)
        ok = msgbox.exec()
        if not ok:
            return
        ma = MyWidget()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ma = MyWidget()
    sys.exit(app.exec_())
