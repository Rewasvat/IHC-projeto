#!/usr/bin/python3
# -*- coding: utf-8 -*-

from dpcs.datamodel import Database, Category, Symbol
from dpcs.speaker import Speaker
from PyQt5.QtGui import QColor
import os
import time

print( "Script utilitário para ajudar a criar um database inicial do projeto ")

def runNewDB():
    rootdir = "./simbolos/"
    categs = os.listdir(rootdir)
    categsImages = {}
    db = Database()

    for cpathname in categs:
        if not os.path.isdir(rootdir+cpathname):
            categsImages[cpathname.split(".")[0]] = cpathname
            continue
        print("-----------------------------")
        print("Insira nome e depois o nome da cor para categoria: " + cpathname)
        cname = input()
        cimage = rootdir+cpathname + ".jpg"
        ccolor = QColor( input() )
        c = Category(cname, cimage, ccolor)
        db.addCategory(c)
        
        cpath = rootdir + cpathname + "/"
        syms = os.listdir(cpath)
        for spath in syms:
            print("Insira 'nome,texto' para simbolo: " + spath)
            print("Se texto for vazio, será igual ao nome. Se nome for vazio, será igual ao nome do arquivo do simbolo.")
            sname, stext = input().split(",")
            if sname == "":
                sname = spath.split(".")[0]
            if stext == "":
                stext = sname
            s = Symbol(sname, stext, cpath + spath)
            c.addSymbol(s)

    db.save()

    print( "\n==============================")

    for c in db.categories():
        print ( "%s (%s | %s)" % (c.name, c.image, c.color.name()))
        for s in c.symbols():
            print("\t- %s: %s (%s)" % (s.name, s.text, s.image))
        
        
def runSpeakAll():
    db = Database.load()
    sp = Speaker()
    for c in db.categories():
        print ( "%s (%s | %s)" % (c.name, c.image, c.color.name()))
        for s in c.symbols():
            print("\t- %s: %s (%s)" % (s.name, s.text, s.image))
            sp.speak(s.name,s.text)
            time.sleep(5)
            
if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "speech":
        runSpeakAll()
    else:
        runNewDB()
