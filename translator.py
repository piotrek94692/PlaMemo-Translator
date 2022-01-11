# -*- coding: utf-8 -*-

#
#    ___ _                                     _____                     _       _
#   / _ \ | __ _  /\/\   ___ _ __ ___   ___   /__   \_ __ __ _ _ __  ___| | __ _| |_ ___  _ __
#  / /_)/ |/ _` |/    \ / _ \ '_ ` _ \ / _ \    / /\/ '__/ _` | '_ \/ __| |/ _` | __/ _ \| '__|
# / ___/| | (_| / /\/\ \  __/ | | | | | (_) |  / /  | | | (_| | | | \__ \ | (_| | || (_) | |
# \/    |_|\__,_\/    \/\___|_| |_| |_|\___/   \/   |_|  \__,_|_| |_|___/_|\__,_|\__\___/|_|
#
# 2021
#
# This is an unofficial automatized translation tool
# for the PC port of the Plastic Memories visual novel game,
# released as an exclusive for PlayStation Vita.
#
# The tool probably can be used on any other Kaleido ADV Workshop games,
# including the PS Vita version of PlaMemo, but that needs to be verified.
# The tool will be rebranded in the future, with an option to turn on the classic Plastic Memories branding.
#
# Created by PIESEL and contributors.
#
#
#
# Links:
#
# r/PlaMemo - Isla's Paradise
# https://discord.com/invite/FattVGH
# PC port of the game and decompilation tools are available here.
# (Or you can get regular FreeMote decompilation tools from GitHub, here: https://github.com/UlyssesWu/FreeMote)
#
# Name Subject to Change
# https://discord.com/invite/zKpYhe3Qnf
# An early version of an English translation is available here.
#
# Contact: PIESEL#8040 [Discord]
# Please report if the links aren't working.
#

from config import config

import sys, subprocess, pkg_resources, ctypes, platform, os, glob, time, datetime, threading, json # Import basic modules
from subprocess import Popen
global plt; plt = platform.system()

global logf; logf = config.logf
global encoding; encoding = config.encoding
devnull = open(os.devnull, "w", encoding=encoding)

if plt == "Windows":
    try:
        subprocess.check_call(["chcp", "65001"], shell=True, stdout=devnull)
    except:
        pass
    try:
        subprocess.check_call(["set", '"PYTHONIOENCODING=UTF-8"'], shell=True, stdout=devnull)
    except:
        pass

# The version name can be set here.
# It should be changed only by an administrator of the project.
global versionstr; versionstr = "Alpha 4"
global version; version = "alpha4"

global title; title = "PlaMemo Translator - " + versionstr
global appid; appid = "plamemo.translator." + version

# Set console window title
if plt == "Windows":
    ctypes.windll.kernel32.SetConsoleTitleA(title + " (Log)") # ANSI
    ctypes.windll.kernel32.SetConsoleTitleW(title + " (Log)") # UNICODE

# A different app ID is required for a custom icon
if plt == "Windows":
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(appid)

class LoggerOut(object):
    def __init__(self):
        self.terminal = sys.stdout
        self.logfile = logf

    def write(self, message):
        self.terminal.write(message)
        with open(self.logfile, "a", encoding=encoding) as f:
            f.write(message)

    def flush(self):
        pass

class LoggerErr(object):
    def __init__(self):
        self.terminal = sys.stderr
        self.logfile = logf

    def write(self, message):
        self.terminal.write(message)
        with open(self.logfile, "a", encoding=encoding) as f:
            f.write(message)

    def flush(self):
        pass

def launchscript(cfile):
    scripttype = config.scripttype
    scriptmethod = config.scriptmethod
    if not scripttype == "auto":
        if scripttype == "bat":
            cfile = cfile + ".bat"
        elif scripttype == "sh":
            cfile = cfile + ".sh"
        elif scripttype == "bash":
            cfile = cfile + ".bash"
    else:
        if plt == "Windows":
            cfile = cfile + ".bat"
        elif plt == "Linux":
            cfile = cfile + ".sh"
        elif plt == "Darwin":
            cfile = cfile + ".bash"
    if not scripttype in ("auto", "bat", "sh", "bash"):
        scripttype = "auto"
    if not scriptmethod in ("auto", "plain", "dotslash", "shplain", "shdotslash"):
        scriptmethod = "auto"
    if not scriptmethod == "auto":
        if scriptmethod == "plain":
            os.system(cfile)
        elif scriptmethod == "dotslash":
            os.system("./" + cfile)
        elif scriptmethod == "shplain":
            os.system("sh " + cfile)
        elif scriptmethod == "shdotslash":
            os.system("sh ./" + cfile)
    else:
        if plt == "Windows":
            os.system(cfile)
        elif plt == "Linux":
            os.system("sh ./" + cfile)
        elif plt == "Darwin":
            os.system("./" + cfile)

def skillapp(): ThisIsNotAnError.KillAppFunction(HasBeenUsed) # Watch out for the second kill app function

sys.stdout = LoggerOut()
sys.stderr = LoggerErr()

print("Loading...")

print()

print(title)

print()

print("Importing extras...")
from datetime import datetime
try:
    from googletrans import Translator
except ImportError:
    launchscript("install")
    skillapp()
print("Importing UI base...")
try:
    from PyQt5 import QtCore, QtGui, QtWidgets, uic
except ImportError:
    launchscript("install")
    skillapp()
print("Importing UI extras...")
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import *
print("Importing done.")

# Set the clock
global now; now = datetime.now()
global current_time; current_time = now.strftime("%H:%M:%S")

print()

print("Loading resources...")
import resource_rc
print("Loading resources done.")

print("Loading UI...")

global app; app = QApplication(sys.argv)
app.setStyle(config.skin)

fontDatabase = QtGui.QFontDatabase()
fontDatabase.addApplicationFont("fonts/KosugiMaru-Regular.ttf") # Set font for text boxes

global mw # Use "mw" to reference "self" from the main window, outside of it

global line; line = 1
global scene; scene = 1

global loaded; loaded = False # Is a file loaded?
global notlooping; notlooping = False
global aboutopen; aboutopen = False # Is the About window open?

def openFileNameDialog(self):
    global file
    global fileName
    global encoding
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    dialog = QFileDialog
    fileName, _ = dialog.getOpenFileName(None,"Select JSON File","","JSON Files (*.json);;All Files (*)",options=options) # Set available file types here
    if fileName:
        print()
        print("Loaded " + fileName)
        with open(fileName, encoding=encoding) as f:
            file = json.load(f)
            mw.updateline()

class AboutUi(QDialog):
    def __init__(self):
        global aboutopen
        global versionstr
        aboutopen = True
        super(AboutUi, self).__init__()
        loadUi("about.ui", self) # Load the About window UI file
        self.abouttext_2.setText("Made by PIESEL#8040.                                             Version: " + versionstr)
        self.setWindowFlags(self.windowFlags() | Qt.CustomizeWindowHint)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.closebutton.clicked.connect(self.close)
        self.show()

    def closeEvent(self, event):
        global aboutopen
        aboutopen = False

class Ui(QMainWindow):

    def __init__(self):

        global mw; mw = self
        global title

        def resettranslate():
            global translate1; translate1 = "Please wait..."
            global translate2; translate2 = "Please wait..."

        resettranslate()

        super(Ui, self).__init__()
        loadUi("translator.ui", self) # Load the main window UI file
        self.setWindowFlags(self.windowFlags() | Qt.CustomizeWindowHint)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)
        self.setWindowTitle(title)

        def showabout():
            # Allow only one About window
            if not aboutopen:
                windowabout = AboutUi(); windowabout.exec()

        def returnline():
            global line
            if loaded:
                line = 1
                resettranslate()
                resetempty()
                mw.updateline()

        def left():
            global line
            global loaded
            if loaded:
                if line > 1:
                    line -= 1
                    resettranslate()
                    resetempty()
                    mw.updateline()

        def sceneleft():
            global scene
            global loaded
            if loaded:
                if scene > 1:
                    scene -= 1
                    resettranslate()
                    resetempty()
                    mw.updateline()

        def sceneright():
            global scene
            global loaded
            global file
            realscene = scene - 1
            if loaded:
                if scene < len(file["scenes"]):
                    scene += 1
                    resetempty()
                    resettranslate()
                    mw.updateline()

        def right():
            global line
            global loaded
            global file
            if loaded:
                if line < len(file["scenes"][0]["texts"]):
                    line += 1
                    resetempty()
                    resettranslate()
                    mw.updateline()

        def reset(): self.newtext.setPlainText(self.oldtext.toPlainText())
        def resetempty(): self.newtext.setPlainText("")
        def translatetransfer1(): self.newtext.setPlainText(self.translatetext1.toPlainText())
        def translatetransfer2(): self.newtext.setPlainText(self.translatetext2.toPlainText())

        def compilescript():
            print()
            print("Compiling...")
            print()
            cfile = "compile.bat" # Windows support is priority
            scripttype = config.scripttype
            scriptmethod = config.scriptmethod
            customfile = config.customfile
            if not scripttype in ("auto", "bat", "sh", "bash"):
                scripttype = "auto"
            if not scriptmethod in ("auto", "plain", "dotslash", "shplain", "shdotslash"):
                scriptmethod = "auto"
            if not customfile == "none":
                cfile = customfile
            else:
                if not scripttype == "auto":
                    if scripttype == "bat":
                        cfile = "compile.bat"
                    elif scripttype == "sh":
                        cfile = "compile.sh"
                    elif scripttype == "bash":
                        cfile = "compile.bash"
                else:
                    if plt == "Windows":
                        cfile = "compile.bat"
                    elif plt == "Linux":
                        cfile = "compile.sh"
                    elif plt == "Darwin":
                        cfile = "compile.bash"
            if not scriptmethod == "auto":
                if scriptmethod == "plain":
                    subprocess.call([cfile]); print(); print("Compiling done.")
                elif scriptmethod == "dotslash":
                    subprocess.call([r"./" + cfile]); print(); print("Compiling done.")
                elif scriptmethod == "shplain":
                    subprocess.call(["sh", cfile]); print(); print("Compiling done.")
                elif scriptmethod == "shdotslash":
                    subprocess.call(["sh", r"./" + cfile]); print(); print("Compiling done.")
            else:
                if plt == "Windows":
                    subprocess.call([cfile]); print(); print("Compiling done.")
                elif plt == "Linux":
                    subprocess.call(["sh", r"./" + cfile]); print(); print("Compiling done.")
                elif plt == "Darwin":
                    subprocess.call([r"./" + cfile]); print(); print("Compiling done.")

        def killapp(): global notlooping; notlooping = True; ThisIsNotAnError.KillAppFunction(HasBeenUsed) # Watch out for the second kill app function

        def apply():
            global file
            global line
            global scene
            global fileName
            global encoding
            realline = line - 1
            realscene = scene - 1
            file["scenes"][realscene]["texts"][realline][2] = self.newtext.toPlainText()
            with open(fileName, "w", encoding=encoding) as f:
                json.dump(file, f, ensure_ascii=False, indent=config.indent)
                print()
                print("Saved the line number " + str(line) + " in scene " + str(scene))

        self.aboutbutton.clicked.connect(showabout)
        self.killapp.clicked.connect(killapp)

        self.compilebutton.clicked.connect(compilescript)

        self.leftbutton.clicked.connect(left)
        self.rightbutton.clicked.connect(right)
        self.sceneleftbutton.clicked.connect(sceneleft)
        self.scenerightbutton.clicked.connect(sceneright)

        self.returnbutton.clicked.connect(returnline)

        self.resetbutton.clicked.connect(reset)
        self.trashbutton.clicked.connect(resetempty)
        self.applybutton.clicked.connect(apply)

        self.translatetransfer1.clicked.connect(translatetransfer1)
        self.translatetransfer2.clicked.connect(translatetransfer2)

        self.action_Open.triggered.connect(openFileNameDialog)

        self.show()

        # This code is always executed in a loop
        def loop():
            while True:
                global line; self.linelabel.setText("Line: " + str(line))
                global scene; self.scenelabel.setText("Scene: " + str(scene))
                global current_time; global now; now = datetime.now(); current_time = now.strftime("%H:%M:%S"); self.time.setText(current_time)
                global notlooping
                if notlooping:
                    break

        theloop = threading.Thread(target=loop)
        theloop.start()

    def translate(self, text):
        gtranslator = Translator()
        translation1 = gtranslator.translate(text, src="ja", dest="en")
        global translate1; translate1 = translation1
        self.translatetext1.setPlainText(translate1.text)

    def updateline(self):
        global linetext; global file; global line; global char1; global char2; global loaded; global scene; global scenelabel
        realline = line - 1
        realscene = scene - 1
        try:
            linetext = file["scenes"][realscene]["texts"][realline][2]
        except Exception:
            scene += 1
            realscene = scene - 1
            linetext = file["scenes"][realscene]["texts"][realline][2]
        self.oldtext.setPlainText(linetext)
        try:
            char1 = file["scenes"][realscene]["texts"][realline][3][0]["name"]; self.character.setPlainText(char1)
        except Exception:
            self.character.setPlainText("")
        try:
            char2 = file["scenes"][realscene]["texts"][realline][0]; self.characterextra.setPlainText(char2)
        except Exception:
            self.characterextra.setPlainText("")
        mw.translate(linetext)
        if line == len(file["scenes"][0]["texts"]):
            linetext.setStyleSheet("color: red;")
        else:
            linetext.setStyleSheet("color: black;")
        if scene == len(file["scenes"]):
            scenelabel.setStyleSheet("color: red;")
        else:
            linetext.setStyleSheet("color: black;")
        loaded = True

window = Ui()

print("Loading done.")

app.exec()
