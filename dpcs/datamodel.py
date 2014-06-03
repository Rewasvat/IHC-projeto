#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os.path
import pickle


class Symbol:
    _fields = ('name', 'text', 'image')

    def __init__(self, name, text='', image=''):
        super().__init__()

        self.name = name
        self.text = text
        self.image = image


class Category:
    _fields = ('name', 'text', 'image', 'color')

    def __init__(self, name, image='', color=None):
        super().__init__()

        self._categories = list()
        self._symbols = list()

        if not name:
            raise ValueError

        self.name = name
        self.image = image
        self.color = color

    def categories(self):
        for category in self._categories:
            if category:
                yield category

    def category(self, categoryName):
        return next((c for c in self._categories if c.name == categoryName), None)

    def categoryNameIndex(self, categoryName):
        return next(((i, c) for i, c in enumerate(self._categories)
                     if c.name == categoryName), (None,))[0]

    def categoryByIndex(self, index):
        return self._categories[index]

    def addCategory(self, category):
        self._categories.append(category)

    def removeCategory(self, category):
        old = None
        if isinstance(category, Category):
            for i, c in enumerate(self._categories):
                if c == category:
                    old = c
                    self._categories[i] = None
                    break
        else:
            categoryName = category

            for i, c in enumerate(self._categories):
                if c.name == categoryName:
                    old = c
                    self._categories[i] = None
                    break

        return old

    def symbols(self):
        for symbol in self._symbols:
            if symbol:
                yield symbol

    def symbolNameIndex(self, symbolName):
        return next(((i, s) for i, s in enumerate(self._symbols)
                     if s.name == symbolName), (None,))[0]

    def symbol(self, symbolName):
        return next((s for s in self._symbols if s.name == symbolName), None)

    def symbolByIndex(self, index):
        return self._symbols[index]

    def addSymbol(self, symbol):
        ex_symbol = self.symbol(symbol.name)
        if ex_symbol:
            raise ValueError

        self._symbols.append(symbol)

    def removeSymbol(self, symbol):
        if isinstance(symbol, Symbol):
            symbol_name = symbol.name
        else:
            symbol_name = symbol

        return self._symbols.pop(symbol_name, None)

    def __len__(self):
        return len(list(self.symbols()))


class Database(Category):
    defaultFilename = "./dpcs-database.dat"

    def __init__(self, tempoDeRotacao=4):
        super().__init__("Database", "null", None)
        self.tempoDeRotacao = tempoDeRotacao

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
