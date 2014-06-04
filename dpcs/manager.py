from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QTableView

from .datamodel import Symbol, Category, Database


class BaseTableModel(QAbstractTableModel):
    fields = Symbol._fields

    def indexByName(self, name):
        raise NotImplementedError

    def itemByIndex(self, index):
        raise NotImplementedError

    def existing(self, name):
        raise NotImplementedError

    def itemCount(self):
        raise NotImplementedError

    def _removeItem(self, item):
        raise NotImplementedError

    def _addItem(self, item):
        raise NotImplementedError

    def __init__(self, category, parent=None):
        super().__init__(parent)

        self.category = category

    def rowCount(self, parent):
        return self.itemCount()

    def columnCount(self, parent):
        return len(self.fields)

    def data(self, index, role):
        if not index.isValid():
            return None
        elif role not in (Qt.DisplayRole, Qt.EditRole):
            return None

        item = self.itemByIndex(index.row())
        field = self.fields[index.column()]
        return getattr(item, field)

    def flags(self, index):
        return super().flags(index) | Qt.ItemIsEditable

    def setData(self, index, value, role):
        if not index.isValid():
            return False
        elif role != Qt.EditRole:
            return False

        item = self.itemByIndex(index.row())
        field = self.fields[index.column()]

        if field == 'name' and (value != item.name):
            if self.existing(value):
                return False

        setattr(item, field, value)
        return True

    def removeItem(self, item):
        index = self.indexByName(item.name)

        self.beginRemoveRows(QModelIndex(), index, index)
        self._removeItem(item)
        self.endRemoveRows()

    def addItem(self, item):
        if self.existing(item.name):
            raise ValueError

        index = self.rowCount(None)
        self.beginInsertRows(QModelIndex(), index, index)
        self._addItem(item)
        self.endInsertRows()

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                try:
                    return self.fields[section].capitalize()
                except IndexError:
                    return None
            elif orientation == Qt.Vertical:
                return str(section)


class SymbolTableModel(BaseTableModel):
    fields = Symbol._fields

    def indexByName(self, name):
        return self.category.symbolNameIndex(name)

    def itemByIndex(self, index):
        return self.category.symbolByIndex(index)

    def existing(self, name):
        return self.category.symbol(name)

    def itemCount(self):
        return self.category.symbolCount()

    def _addItem(self, item):
        self.category.addSymbol(item)

    def _addItemByName(self, name):
        self._addItem(Symbol(name=name))

    def _removeItem(self, item):
        return self.category.removeSymbol(item)

    def _removeItemByName(self, name):
        return self.category.removeSymbol(name)


class CategoryTableModel(BaseTableModel):
    fields = Category._fields

    def indexByName(self, name):
        return self.category.categoryNameIndex(name)

    def itemByIndex(self, index):
        return self.category.categoryByIndex(index)

    def existing(self, name):
        return self.category.category(name)

    def itemCount(self):
        return self.category.categoryCount()

    def _addItem(self, item):
        self.category.addCategory(item)

    def _addItemByName(self, name):
        self._addItem(Category(name=name))

    def _removeItem(self, item):
        return self.category.removeCategory(item)

    def _removeItemByName(self, name):
        return self.category.removeCategory(name)


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

    def _createTimeSlider(self, min, max):
        box = QVBoxLayout()

        slider = QSlider()

        slider.setOrientation(Qt.Horizontal)
        slider.setMinimum(min)
        slider.setMaximum(max)
        slider.setSingleStep(1)
        slider.valueChanged.connect(self.setRotationTime)

        hbox = QHBoxLayout()
        minLabel = QLabel(str(min))
        maxLabel = QLabel(str(max))
        curLabel = QLabel()

        hbox.addWidget(minLabel)
        hbox.addSpacer()
        hbox.addWidget(curLabel)
        hbox.addSpacer()
        hbox.addWidget(maxLabel)

        def updateLabel(value):
            curLabel.setText(str(value))

        box.addWidget(QLabel("Tempo de Rotação (em segundos)"))
        box.addWidget(slider)



        return box, slider

    def setRotationTime(self, value):
        self.rotationTime = value

    def _selectCategoryEvent(self, selection):
        if selection.isEmpty():
            self.selectCategory(None)
        else:
            self.selectCategory(self.selectedCategory())

    def _selectSymbolEvent(self, selection):
        self._updateSymbolButtons()

    def _updateCategoryButtons(self):
        self._categoryRemoveButton.setEnabled(self.selectedCategory() is not None)

    def _updateSymbolButtons(self):
        self._symbolRemoveButton.setEnabled(self.selectedSymbol() is not None)
        self._symbolAddButton.setEnabled(self.selectedCategory() is not None)

    def selectedCategory(self):
        try:
            index = self._categoryTable.selectedIndexes()[0]
        except IndexError:
            return None

        category = self._categoryTable.model().itemByIndex(index.row())
        return category

    def selectCategory(self, category):
        if not category:
            self._populateSymbolTable(None)
            self._updateCategoryButtons()
            self._updateSymbolButtons()
            return

        if isinstance(category, str):
            category = self.database.category(category)

        self._populateSymbolTable(category)
        self._updateCategoryButtons()
        self._updateSymbolButtons()

    def addCategory(self):
        self._categoryTable.model().addItem(Category(name='Nova Categoria'))

    def removeCategory(self):
        category = self.selectedCategory()
        if category is not None:
            self._categoryTable.model().removeItem(category)

    def selectedSymbol(self):
        try:
            index = self._symbolTable.selectedIndexes()[0]
        except IndexError:
            return None

        symbol = self._symbolTable.model().itemByIndex(index.row())
        return symbol

    def addSymbol(self):
        self._symbolTable.model().addItem(Symbol(name='Novo Simbolo'))

    def removeSymbol(self):
        symbol = self.selectedSymbol()
        if symbol is not None:
            self._symbolTable.model().removeItem(symbol)

    def _initTable(self, label, removeCallback, addCallback):
        table = QTableView()

        buttonRow, removeButton, addButton = self._createButtonRow(
            ['-', '+'], self._buttonMakeSmall)

        addButton.pressed.connect(addCallback)
        removeButton.pressed.connect(removeCallback)

        vbox = QVBoxLayout()
        vbox.addWidget(QLabel(label))
        vbox.addWidget(table)
        vbox.addLayout(buttonRow)

        return vbox, table, removeButton, addButton

    def _populateCategoryTable(self):
        self._categoryTable.setModel(CategoryTableModel(self.database))
        self._categoryTable.selectionModel().selectionChanged.connect(self._selectCategoryEvent)

    def _populateSymbolTable(self, category=None):
        if category is None:
            self._symbolTable.setModel(SymbolTableModel(Category('null')))
        else:
            self._symbolTable.setModel(SymbolTableModel(category))

        self._symbolTable.selectionModel().selectionChanged.connect(self._selectSymbolEvent)

    def __init__(self):
        super().__init__()

        self.database = self._load_db()

        displayRow = QHBoxLayout()
        categoryBox, self._categoryTable, self._categoryRemoveButton, self._categoryAddButton = \
            self._initTable("Categorias", self.removeCategory, self.addCategory)
        symbolBox, self._symbolTable, self._symbolRemoveButton, self._symbolAddButton = \
            self._initTable("Símbolos", self.removeSymbol, self.addSymbol)
        displayRow.addLayout(categoryBox)
        displayRow.addLayout(symbolBox)

        optionsRow = QVBoxLayout()
        rotationTimeBox, rotationTimeSlider = self._createTimeSlider()
        rotationTimeSlider.setValue(self.database.rotationTime)

        optionsRow.addLayout(rotationTimeBox)

        buttonRow, reloadButton, saveButton = self._createButtonRow(
            ["&Recarregar", "&Salvar"])

        reloadButton.pressed.connect(self.reload)
        saveButton.pressed.connect(self.save)

        layout = QVBoxLayout()
        layout.addItem(displayRow)
        layout.addItem(optionsRow)
        layout.addItem(buttonRow)

        self.setLayout(layout)

        self._populateCategoryTable()
        self._populateSymbolTable(None)

        self._categoryTable.setSelectionMode(QAbstractItemView.SingleSelection)
        self._symbolTable.setSelectionMode(QAbstractItemView.SingleSelection)

    def _load_db(self):
        database = Database.load()
        if database is None:
           database = Database.testData()

        return database

    def reload(self):
        self.database = self._load_db()

        self._populateCategoryTable()
        self._populateSymbolTable(None)

    def save(self):
        self.database.save()

