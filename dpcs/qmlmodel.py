#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import QObject, pyqtSlot, pyqtProperty, pyqtSignal
from PyQt5.QtQml import QQmlListProperty
from PyQt5.QtGui import QColor
from . import datamodel

###
class Database(QObject):
    def __init__(self, parent=None):
        super(Database,self).__init__(parent)
        self.data = datamodel.Database.load()
        
    @pyqtSlot()
    def save(self):
        self.data.save()
        
    @pyqtSlot()
    def load(self):
        self.data = datamodel.Database.load()
        
    @pyqtProperty(QQmlListProperty, constant=True)
    def categories(self):
        categs = []
        for c in self.data.categories():
            categs.append(Category(self, c))
        return QQmlListProperty(Category, self, categs)

###
class Category(QObject):
    def __init__(self, parent=None, categ=None):
        super(Category,self).__init__(parent)
        self.categ = categ
        self.isSelected = False
        
    nameChanged = pyqtSignal(str)
    
    @pyqtProperty(str, notify=nameChanged)
    def name(self):
        return self.categ.name
    @name.setter
    def name(self, name):
        self.categ.name = name
        
    imageChanged = pyqtSignal(str)
    
    @pyqtProperty(str, notify=imageChanged)
    def image(self):
        return self.categ.image
    @image.setter
    def image(self, image):
        self.categ.image = image
        
    colorChanged = pyqtSignal(QColor)
    
    @pyqtProperty(QColor, notify=colorChanged)
    def bgColor(self):
        return self.categ.color
    @bgColor.setter
    def bgColor(self, color):
        self.categ.color = color

    selectedChanged = pyqtSignal(bool)

    @pyqtProperty(bool, notify=selectedChanged)
    def isSelected(self):
        return self.categ.selected
    @isSelected.setter
    def isSelected(self, value):
        self.categ.selected = value

        
    @pyqtProperty(QQmlListProperty, constant=True)
    def symbols(self):
        syms = []
        for s in self.categ.symbols():
            syms.append(Symbol(self, s))
        v1 = Symbol(self, datamodel.Symbol("voltar", "Voltar", "./simbolos/seta.jpg"))
        v2 = Symbol(self, datamodel.Symbol("voltar", "Voltar", "./simbolos/seta.jpg"))
        syms.insert(0, v1)
        syms.insert(1+int(len(syms)/2), v2)
        return QQmlListProperty(Symbol, self, syms)
   
###
class Symbol(QObject):
    def __init__(self, parent=None, sym=None):
        super(Symbol,self).__init__(parent)
        self.symbol = sym
    
    nameChanged = pyqtSignal(str)
    
    @pyqtProperty(str, notify=nameChanged)
    def name(self):
        return self.symbol.name
    @name.setter
    def name(self, name):
        self.symbol.name = name

    stextChanged = pyqtSignal(str)
    
    @pyqtProperty(str, notify=stextChanged)
    def stext(self):
        return self.symbol.text
    @stext.setter
    def stext(self, text):
        self.symbol.text = text
        
    imageChanged = pyqtSignal(str)
    
    @pyqtProperty(str, notify=imageChanged)
    def image(self):
        return self.symbol.image
    @image.setter
    def image(self, image):
        self.symbol.image = image

