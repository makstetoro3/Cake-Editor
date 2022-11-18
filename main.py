import sqlite3
from PyQt5.QtWidgets import QMainWindow, QLineEdit
from viev.connectQt import load


class Singing(QMainWindow):
    def __init__(self):
        super().__init__()
        self.con = sqlite3.connect('db/dbshka.sqlite')
        self.cur = self.con.cursor()
        load(self, 'viev/entrance.ui')
        self.pushButton.clicked.connect(self.run)
        self.pushButton_2.clicked.connect(self.run_)
        self.mai = None
        self.lineEdit.setEchoMode(QLineEdit.Password)

    def op(self, elem):
        self.mai = elem

    def run(self):
        if self.lineEdit_2.text() == '':
            self.lineEdit_2.setText('введите логин')
            return
        if self.lineEdit.text() == '':
            self.lineEdit.setText('введите пароль')
            return
        if len(self.cur.execute(f"""SELECT * FROM user
        WHERE name = '{self.lineEdit_2.text()}'""").fetchall()) == 0:
            self.lineEdit_2.setText('логин не найден')
            return
        if str(self.cur.execute(f"""SELECT password FROM user
                                  WHERE name = '{self.lineEdit_2.text()}'""").fetchall()[0][0]) != self.lineEdit.text():
            self.lineEdit.setText('неверный пароль')
            return
        self.mai.use(self.cur.execute(f"""SELECT * FROM user
                            WHERE name = '{self.lineEdit_2.text()}'""").fetchall()[0])
        self.mai.show()
        self.close()

    def run_(self):
        if self.lineEdit_2.text() == '':
            self.lineEdit_2.setText('введите логин')
            return
        if self.lineEdit.text() == '':
            self.lineEdit.setText('введите пароль')
            return
        if len(self.cur.execute(f"""SELECT * FROM user
        WHERE name = '{self.lineEdit_2.text()}'""").fetchall()) > 0:
            self.lineEdit_2.setText('логин занят')
            return
        self.cur.execute(f'''INSERT INTO user(name, password)
                             VALUES('{self.lineEdit_2.text()}', '{self.lineEdit.text()}')''')
        self.con.commit()
        self.mai.use(self.cur.execute(f"""SELECT * FROM user
                            WHERE name = '{self.lineEdit_2.text()}'""").fetchall()[0])
        self.mai.show()
        self.close()
