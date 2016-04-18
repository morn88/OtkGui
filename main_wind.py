import sys
from PyQt4 import QtGui, QtCore, QtSql

class OtkGui(QtGui.QWidget):
    def __init__(self):
        super(OtkGui, self).__init__()

        self.setGeometry(50, 50, 980, 600)
        self.setWindowTitle('Просмотр натяжения струнопакетов')
        # self.showMaximized()

        self.btn = QtGui.QPushButton("Запрос", self)
        self.btn.clicked.connect(self.show_date_choice)

        self.label = QtGui.QLabel('Выбранная дата: ', self)
        self.label1 = QtGui.QLabel(self)
        self.label2 = QtGui.QLabel("Cоединение с базой: ", self)
        self.label3 = QtGui.QLabel(self)


        self.db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        self.db.setHostName("localhost")
        self.db.setDatabaseName("pkg_strings.db")

        self.model = QtSql.QSqlTableModel(self)
        self.model.setTable('span')

        curr_date = QtCore.QDate.currentDate()
        string = "tens_date=" + '"' + curr_date.toString('yyyy-MM-dd') + '"'
        self.model.setFilter(string)
        self.model.select()

        self.model.setHeaderData(0, QtCore.Qt.Horizontal, 'Дата')
        self.model.setHeaderData(1, QtCore.Qt.Horizontal, 'Время')
        self.model.setHeaderData(2, QtCore.Qt.Horizontal, 'Номер формы')
        self.model.setHeaderData(3, QtCore.Qt.Horizontal, 'Номер ячейки')
        self.model.setHeaderData(4, QtCore.Qt.Horizontal, 'Заданное усилие')
        self.model.setHeaderData(5, QtCore.Qt.Horizontal, 'Усилие 1')
        self.model.setHeaderData(6, QtCore.Qt.Horizontal, 'Усилие 2')
        self.model.setHeaderData(7, QtCore.Qt.Horizontal, 'Усилие 3')
        self.model.setHeaderData(8, QtCore.Qt.Horizontal, 'Усилие 4')

        self.label3.setText(self.model.lastError().text())
        print(self.model.lastError().text())

        self.table = QtGui.QTableView(self)
        self.table.setModel(self.model)
        self.table.setShowGrid(True)
        self.table.resizeColumnsToContents()
        self.table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.table.horizontalHeader().setStretchLastSection(True)

        self.stylesheet = "::section{Background-color:rgb(190,1,1);border-radius:14px;color:white;}"
        self.table.horizontalHeader().setStyleSheet(self.stylesheet)
        self.table.verticalHeader().setStyleSheet(self.stylesheet)

        self.my_grid = QtGui.QGridLayout(self)
        self.my_grid.addWidget(self.btn, 0, 0)
        self.my_grid.addWidget(self.label, 0, 1)
        self.my_grid.addWidget(self.label1, 0, 2)
        self.my_grid.addWidget(self.label2, 0, 13)
        self.my_grid.addWidget(self.label3, 0, 14)
        self.my_grid.addWidget(self.table, 1, 0, 1, 1)

        self.show()

    def show_date_choice(self):
        global modalWindow
        modalWindow = QtGui.QWidget(self, QtCore.Qt.Window)
        modalWindow.setWindowTitle("Выберите дату")
        modalWindow.setFixedSize(500, 300)
        modalWindow.setWindowModality(QtCore.Qt.WindowModal)
        modalWindow.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        modalWindow.move(self.geometry().center() - modalWindow.rect().center() - QtCore.QPoint(4, 30))

        modalWindow.cld1 = QtGui.QCalendarWidget(modalWindow)
        modalWindow.cld1.setFirstDayOfWeek(1)
        modalWindow.cld1.setGridVisible(True)
        modalWindow.cld1.resize(modalWindow.size())
        # modalWindow.cld1.setDateRange(QtCore.QDate.currentDate().addDays(-120), QtCore.QDate.currentDate())
        modalWindow.cld1.setMaximumDate(QtCore.QDate.currentDate())
        modalWindow.cld1.selectionChanged.connect(self.my_query)
        modalWindow.cld1.setHorizontalHeaderFormat(2)
        modalWindow.cld1.setVerticalHeaderFormat(0)

        modalWindow.show()

    def my_query(self):
        my_date = modalWindow.cld1.selectedDate()
        self.label1.setText(my_date.toString('dd.MM.yyyy'))
        modalWindow.close()
        ok = self.db.open()
        if ok:
            print('OK')
            self.label3.setStyleSheet('color: rgb(0, 255, 0)')
            self.label3.setText('OK')
            print(my_date.toString('yyyy-MM-dd'))
            string = "tens_date=" +'"' + my_date.toString('yyyy-MM-dd') + '"'
            self.model.setFilter(string)
            self.model.select()
            self.table.setSortingEnabled(True)
            self.table.setSelectionBehavior(1)
            self.table.resizeColumnsToContents()
            self.table.horizontalHeader().setStretchLastSection(True)
        else:
            print("Error")
            self.label3.setStyleSheet('color: rgb(255, 0, 0)')
            self.label3.setText('Error')


app = QtGui.QApplication(sys.argv)
gui = OtkGui()

sys.exit(app.exec_())
