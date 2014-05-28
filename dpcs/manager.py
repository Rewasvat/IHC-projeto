from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from .datamodel import Symbol, Category, Database


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