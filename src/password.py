# !/usr/bin/python
# -*- coding: iso-8859-1 -*-
try:
    # Python 2
    import Tkinter as tkinter
    
except ImportError:
    # Python 3
    import tkinter
    from tkinter import messagebox as tkMessageBox

import menu

def checkroot():
    result = tkMessageBox.askyesno(
        "Root", "Do you have Root access to device?")
    if (result):
        dialog()
    else:
        quit()


def dialog():
    root = Tkinter.Tk()
    cred = menu.Menu(root).loginScreen()
    menu.windowDestroy()
    return cred


def quit():
    status = 0
    return status
