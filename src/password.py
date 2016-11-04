# !/usr/bin/python
# -*- coding: iso-8859-1 -*-

import tkMessageBox
import menu
import Tkinter


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
