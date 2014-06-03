#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os.path
import pickle
from collections import namedtuple, OrderedDict


class Symbol(namedtuple('Symbol', 'name text image')):
    pass


class Category:
    def __init__(self, name, image, color):
        self._categories = OrderedDict()
        self._symbols = OrderedDict()

        if not name:
            raise ValueError

        self.name = name
        self.image = image
        self.color = color

    def categories(self):
        for category in self._categories.values():
            yield category

    def category(self, categoryName):
        return self._categories.get(categoryName, None)

    def addCategory(self, category):
        self._categories[category.name] = category

    def removeCategory(self, category):
        if isinstance(category, Category):
            category_name = category.name
        else:
            category_name = category

        return self._categories.pop(category_name, None)

    def symbols(self):
        for symbol in self._symbols.values():
            yield symbol

    def symbol(self, symbolName):
        return self._categories.get(symbolName, None)

    def addSymbol(self, symbol):
        self._symbols[symbol.name] = symbol

    def removeSymbol(self, symbol):
        if isinstance(symbol, Symbol):
            symbol_name = symbol.name
        else:
            symbol_name = symbol

        return self._symbols.pop(symbol_name, None)

#    def allSymbols(self):
#        yield from self.symbols()
#
#        for category in self.categories():
#            yield from category.symbols()


class Database(Category):
    defaultFilename = "./dpcs-database.dat"

    def __init__(self):
        super().__init__("Database", "null", None)

    def addSymbol(self, symbol):
        raise NotImplementedError

    def removeSymbol(self, symbol):
        raise NotImplementedError

    def save(self, filename=None):
        filename = filename or self.defaultFilename

        with open(filename, 'wb') as fp:
            return pickle.dump(self, fp)

    @classmethod
    def load(cls, filename=None):
        filename = filename or cls.defaultFilename

        if os.path.exists(filename):
            with open(filename, 'rb') as fp:
                return pickle.load(fp)

        return None

    @classmethod
    def testData(cls, save=True):
        from PyQt5.QtGui import QColor
        db = Database()
        c1 = Category('test', 'testImage', QColor('red'))
        c2 = Category('meuDeus', '2222Image', QColor('blue'))

        s1 = Symbol('1', '1', '1')
        s2 = Symbol('2', '2', '2')
        s3 = Symbol('3', '3', '3')

        c1.addSymbol(s1)
        c1.addSymbol(s2)
        c2.addSymbol(s3)

        db.addCategory(c1)
        db.addCategory(c2)

        if save:
            db.save()

        return db

__all__ = ('Symbol', 'Category', 'Database')
