import sqlite3
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QWidget, QLabel
from PyQt5 import uic


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.con = sqlite3.connect("coffee.db")
        self.cur = self.con.cursor()
        self.pushButton.clicked.connect(self.load_result)
        self.pushButton_2.clicked.connect(self.change_res)
        self.modified = {}
        self.titles = None

    def make_table(self, data):
        self.tableWidget.setRowCount(len(data))
        self.tableWidget.setColumnCount(len(data[0]))
        self.titles = [description[0] for description in self.cur.description]
        for i, elem in enumerate(data):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))

    def update_result(self):
        result = self.cur.execute("Select * from coffee WHERE id=?",
                             (self.spinBox.text(),)).fetchall()
        self.make_table(result)
        self.modified = {}

    def load_result(self):
        result = self.cur.execute("Select * from coffee").fetchall()
        self.make_table(result)

    def change_res(self):
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.pushButton_3.clicked.connect(self.add_coffee)
        self.pushButton_4.clicked.connect(self.update_result)
        self.tableWidget.itemChanged.connect(self.item_changed)
        self.pushButton_5.clicked.connect(self.save_results)

    def item_changed(self, item):
        self.modified[self.titles[item.column()]] = item.text()

    def save_results(self):
        if self.modified:
            cur = self.con.cursor()
            que = "UPDATE coffee SET\n"
            for key in self.modified.keys():
                que += "'{}' = '{}'\n".format(key, self.modified.get(key))
            que += "WHERE id = ?"
            cur.execute(que, (self.spinBox.text(),))
            self.con.commit()

    def add_coffee(self):
        self.result = self.cur.execute("INSERT INTO coffee('Название сорта', 'степень обжарки', 'молотый/в зернах', "
                                       "'описание вкуса', 'цена', 'объем упаковки') VALUES(?, ?, ?, ?, ?, ?)",
                                       (self.lineEdit_title.text(), self.lineEdit_obzh.text(),
                                        self.lineEdit_molot.text(), self.lineEdit_discr.text(),
                                        self.lineEdit_weight.text(), self.lineEdit_price.text()))
        self.con.commit()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
