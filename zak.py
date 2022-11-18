import sqlite3
from viev.connectQt import load

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt


class Zaking(QMainWindow):
    def __init__(self, name, mass, prise, us):
        super().__init__()
        self.con = sqlite3.connect('db/dbshka.sqlite')
        self.cur = self.con.cursor()
        load(self, 'viev/mufer.ui')
        self.setWindowModality(Qt.ApplicationModal)
        self.name = name
        self.price = prise
        self.mass = mass
        self.label_3.setText(name)
        self.lineEdit.setText('Вес: ' + str(mass) + ' кг')
        self.lineEdit_2.setText('Стоимость: ' + str(prise))
        self.lineEdit.setReadOnly(True)
        self.lineEdit_2.setReadOnly(True)
        self.pushButton.clicked.connect(self.bay)
        self.user = us

    def bay(self):
        self.cur.execute(f'''INSERT INTO zak(name, id_user, price, data, move)
                                         VALUES('{self.name} {str(self.mass) + ' кг'}', {self.user}, '{self.price}',
                                          '{','.join(self.dateEdit.text().split(' .')[0:1])}', 
                                          '{self.comboBox.currentText()}')''')
        self.con.commit()
        self.close()
