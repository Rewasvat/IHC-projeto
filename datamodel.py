#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pickle

class Database:
    def __init__(self):
        self.categories = {}
        
    def addCategory(self, name):
        if name in self.categories:
            print("Category", name, "already exists")
            return
        self.categories[name] = Category(name)
    
    def getCategories(self):
        return tuple(self.categories.values())
        
    def save(self):
        with open("database", "wb") as f:
            pickle.dump(self, f)
            
    def Load():
        with open("database", "rb") as f:
            return pickle.load(f)

    def __getitem__(self, key):
        return self.categories[key]


class Category:
    def __init__(self, name=""):
        self.name = name
        self.symbols = {}
        
    def addSymbol(self, name, text, image):
        if name in self.symbols:
            print("Symbol already exists")
            return
        self.symbols[name] = Symbol(name, text, image)

    def getSymbols(self):
        return tuple(self.symbols.values())
        
    def __getitem__(self, key):
        return self.symbols[key]
        
        
class Symbol:
    def __init__(self, name, text, image):
        self.name = name
        self.text = text
        self.image = image
        
        
       
