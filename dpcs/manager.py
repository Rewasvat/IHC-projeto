from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QTableView

from .datamodel import Symbol, Category, Database


class SymbolTableModel(QAbstractTableModel):
    fields = Symbol._fields

    def __init__(self, category, parent=None):
        super().__init__(parent)

        self.category = category

    def indexByName(self, name):
        return self.category.symbolNameIndex(name)

    def nameByIndex(self, index):
        return self.category.symbolByIndex(index).name

    def rowCount(self, parent):
        return len(self.category)

    def columnCount(self, parent):
        return len(self.fields)

    def data(self, index, role):
        if not index.isValid():
            return None
        elif role != Qt.DisplayRole:
            return None

        name = self.nameByIndex(index.row())
        field = self.fields[index.column()]
        return self.category.symbol(name)[field]

    def flags(self, index):
        return super().flags(index) | Qt.ItemIsEditable

    def setData(self, index, value, role):
        if not index.isValid():
            return False
        elif role != Qt.EditRole:
            return False

        name = self.nameByIndex(index.row())
        symbol = self.category.symbol(name)

        field = self.fields[index.column()]
        if field == 'name' and (value != symbol.name):
            if self.category.symbol(value):
                return False

        symbol[field] = value
        return True

    def removeSymbol(self, name):
        index = self.indexByName(name)

        self.beginRemoveRows(QModelIndex(), index, index)
        self.category.removeSymbol(name)
        self._populateIndexes()
        self.endRemoveRows()

    def addSymbol(self, name):
        if self.category.symbol(name):
            raise ValueError

        index = self.rowCount(None)
        self.beginInsertRows(None, index, index + 1)
        self.category.addSymbol(Symbol(name=name))
        self._populateIndexes()
        self.endInsertRows()

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            try:
                return self.fields[section].capitalize()
            except IndexError:
                return None

class SymbolManager(QWidget):
    smallButtonSize = 30

    @classmethod
    def _buttonMakeSmall(cls, button):
        button.setFixedWidth(cls.smallButtonSize)

    def _createButtonRow(self, labels, process=None):
        hbox = QHBoxLayout()
        hbox.addStretch()

        result = [hbox]
        for label in labels:
            button = QPushButton(label)
            if process:
                process(button)

            hbox.addWidget(button)
            result.append(button)

        return result

    def _selectCategoryEvent(self, selection):
        if selection.isEmpty():
            self.selectCategory(None)
        else:
            index = selection.indexes()[0]
            item = self._categoryList.itemFromIndex(index)
            self.selectCategory(item.text())

    def selectCategory(self, categoryName):
        if not categoryName:
            self._populateSymbolTable(None)
        else:
            newCategory = self.database.category(categoryName)
            self._populateSymbolTable(newCategory)

    def addCategory(self):
        print('BLARGH')

    def removeCategory(self):
        print('ARGH')

    def _initCategoryList(self):
        list_ = QListWidget()
        list_.selectionModel().selectionChanged.connect(self._selectCategoryEvent)

        buttonRow, removeButton, addButton = self._createButtonRow(
            ['-', '+'], self._buttonMakeSmall)

        addButton.pressed.connect(self.addCategory)
        removeButton.pressed.connect(self.removeCategory)

        vbox = QVBoxLayout()
        vbox.addWidget(list_)
        vbox.addLayout(buttonRow)

        return vbox, list_

    def _populateCategoryList(self):
        self._categoryList.clear()

        categories = list(self.database.categories())

        for category in categories:
            self._categoryList.addItem(QListWidgetItem(category.name))

        self.selectCategory(None)

    def addSymbol(self):
        pass

    def removeSymbol(self):
        print('ARGH')

    def _initSymbolTable(self):
        table = QTableView()

        buttonRow, removeButton, addButton = self._createButtonRow(
            ['-', '+'], self._buttonMakeSmall)

        addButton.pressed.connect(self.addSymbol)
        removeButton.pressed.connect(self.removeSymbol)

        vbox = QVBoxLayout()
        vbox.addWidget(table)
        vbox.addLayout(buttonRow)

        return vbox, table

    def _initWidgetSymbolTable(self):
        table = QTableWidget()
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["Nome", "Texto", "Imagem"])
        table.resizeColumnsToContents()

        buttonRow, removeButton, addButton = self._createButtonRow(
            ['-', '+'], self._buttonMakeSmall)

        addButton.pressed.connect(self.addSymbol)
        removeButton.pressed.connect(self.removeSymbol)

        vbox = QVBoxLayout()
        vbox.addWidget(table)
        vbox.addLayout(buttonRow)

        return vbox, table

    def _populateSymbolTable(self, category=None):
        if category is None:
            self._symbolTable.setModel(None)
        else:
            self._symbolTable.setModel(SymbolTableModel(category))

    def _populateWidgetSymbolTable(self, category=None):
        self._currentCategory = category

        self._symbolTable.clearContents()

        if category:
            symbols = list(category.symbols())
        else:
            symbols = []

        self._symbolTable.setRowCount(len(symbols))

        for i, symbol in enumerate(symbols):
            self._symbolTable.setItem(i, 0, QTableWidgetItem(symbol.name))
            self._symbolTable.setItem(i, 1, QTableWidgetItem(symbol.text))
            self._symbolTable.setItem(i, 2, QTableWidgetItem(symbol.image))

    def __init__(self):
        super().__init__()

        self.database = Database.load() or Database.testData()

        displayRow = QHBoxLayout()
        categoryBox, self._categoryList = self._initCategoryList()
        self._currentCategory = None

        symbolBox, self._symbolTable = self._initSymbolTable()

        displayRow.addLayout(categoryBox)
        displayRow.addLayout(symbolBox)

        buttonRow, reloadButton, saveButton = self._createButtonRow(
            ["&Recarregar", "&Salvar"])

        layout = QVBoxLayout()
        layout.addItem(displayRow)
        layout.addItem(buttonRow)

        self.setLayout(layout)

        self._populateCategoryList()

    def save(self):
        self.database.save()