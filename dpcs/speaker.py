#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
from urllib.request import Request, urlopen
from urllib.parse import urlencode

from PyQt5.QtCore import QUrl, QFileInfo
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

import steel


class Speaker:
    def __init__(self):
        self.player = QMediaPlayer()

        try:
            self.backup = steel.available_engines()[0]()
            self.backup.set("rate", 150)
        except:
            self.backup = None
            print("Could not start a backup offline speaker.")

    def speak(self, name, text, lang="pt-br"):
        fpath = "./speeches/" + name + ".mp3"
        if not os.path.isdir("./speeches"):
            os.mkdir("./speeches")
        if not os.path.isfile(fpath):
            print("Running TTS...")
            try:
                data = urlencode( [("tl", lang), ("q", text), ("ie", "UTF-8")] )
                bin_data = data.encode("utf8")
                req = Request("http://translate.google.com/translate_tts", bin_data, {"User-Agent":"My agent !"})
                fin = urlopen(req)
                mp3 = fin.read()
                fout = open(fpath, "wb")
                fout.write(mp3)
                fout.close()
            except Exception as exc:
                print("Error trying to get TTS file:", str(exc))
                if self.backup != None:
                    print("Proceeding to use backup speaker...")
                    self.backup.speak(text)
                return
        
        self.player.stop()
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(QFileInfo(fpath).absoluteFilePath())))
        self.player.play()
