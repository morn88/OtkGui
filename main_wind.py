import sys
from PyQt4 import QtGui, QtCore, QtSql

class OtkGui(QtGui.QWidget):
    def __init__(self):
        super(OtkGui, self).__init__()

        self.setGeometry(50, 50, 900, 600)
        self.setWindowTitle('Просмотр натяжения струнопакетов')
        # self.showMaximized()

        self.btn = QtGui.QPushButton("Запрос", self)
        self.btn.clicked.connect(self.show_date_choice)

        self.label = QtGui.QLabel('Выбранная дата: ', self)
        self.label1 = QtGui.QLabel(self)
        self.label2 = QtGui.QLabel("Cоединение с базой: ", self)
        self.label3 = QtGui.QLabel(self)

        # self.table = QtGui.QTableWidget(0, 9, self)
        # self.table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        # self.table.setHorizontalHeaderItem(0, QtGui.QTableWidgetItem("Дата"))
        # self.table.setHorizontalHeaderItem(1, QtGui.QTableWidgetItem("Время"))
        # self.table.setHorizontalHeaderItem(2, QtGui.QTableWidgetItem("Номер формы"))
        # self.table.setHorizontalHeaderItem(3, QtGui.QTableWidgetItem('Номер ячейки'))
        # self.table.setHorizontalHeaderItem(4, QtGui.QTableWidgetItem('Усилие заданное'))
        # self.table.setHorizontalHeaderItem(5, QtGui.QTableWidgetItem('Усилие 1'))
        # self.table.setHorizontalHeaderItem(6, QtGui.QTableWidgetItem('Усилие 2'))
        # self.table.setHorizontalHeaderItem(7, QtGui.QTableWidgetItem('Усилие 3'))
        # self.table.setHorizontalHeaderItem(8, QtGui.QTableWidgetItem('Усилие 4'))
        # self.table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        # self.table.horizontalHeader().setStretchLastSection(True)
        # self.table.setDisabled(True)

        self.db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        self.db.setHostName("localhost")
        self.db.setDatabaseName("pkg_strings.db")

        self.model = QtSql.QSqlTableModel(self)
        self.model.setTable('span')
        self.model.setEditStrategy(2)
        self.model.select()

        print(self.model.lastError().text())

        self.table = QtGui.QTableView(self)
        self.table.setModel(self.model)
        self.table.resizeColumnsToContents()

        self.my_grid = QtGui.QGridLayout(self)
        self.my_grid.addWidget(self.btn, 0, 0)
        self.my_grid.addWidget(self.label, 0, 1)
        self.my_grid.addWidget(self.label1, 0, 2)
        self.my_grid.addWidget(self.label2, 0, 13)
        self.my_grid.addWidget(self.label3, 0, 14)
        self.my_grid.addWidget(self.table, 1, 0, 1, 15)

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

        else:
            print("Error")
            self.label3.setStyleSheet('color: rgb(255, 0, 0)')
            self.label3.setText('Error')

        query = QtSql.QSqlQuery(self.db)
        if query.exec_("SELECT * FROM span"):
            while query.next():
                print(query.value(0), query.value(1), query.value(2), query.value(3), query.value(4), query.value(5),
                query.value(6), query.value(7), query.value(8))


app = QtGui.QApplication(sys.argv)
gui = OtkGui()

sys.exit(app.exec_())
