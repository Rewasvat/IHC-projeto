#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, os, tempfile, time
from urllib.request import Request, urlopen
from urllib.parse import urlencode

from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

class pytts():

    def __init__(self):
        self.player = QMediaPlayer()

    def speak(self, text, lang="pt-br"):
        data = urlencode( [("tl", lang), ("q", text), ("ie", "UTF-8")] )
        bin_data = data.encode("utf8")
        req = Request("http://translate.google.com/translate_tts", bin_data, {"User-Agent":"My agent !"})
        fin = urlopen(req)
        mp3 = fin.read()
        
        fd, fpath = tempfile.mkstemp()
        fout = os.fdopen(fd, "r+b")
        fout.write(mp3)
        fout.close()
        
        self.player.stop()
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(fpath)))
        self.player.play()
        
        count = 0
        lastpos = 0
        while True:
            time.sleep(0.1)
            pos = self.player.position()
            print(pos, lastpos, count)
            if pos == lastpos:
                count += 1
                if count > 5:
                    self.player.stop()
                    break
            else:
                count = 0
            lastpos = pos
        print("finishing")
        os.remove(fpath)
    
