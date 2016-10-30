#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import os
import Tkinter
from Tkinter import *

import csv
import ttk
import backend
import tkFont

class k4tress_tk(Tkinter.Frame):

    def __init__(self, parent):
        global top
        global password
        global treeContent

        Tkinter.Frame.__init__(self,parent)
        self.parent = parent
        self.initialize()
        self.createWidgits()
        backend.initialSetup()

    #Database entry search
    def OnTreeSearchClick(self, event):
        #iterates through the tree, and sets the selection to the item that matches selection provided
        findItem = self.entryVariable.get()
        treeContent = self.get_children('')
        for item in treeContent:
            if str(item['values'][0]) == findItem:
                self.selection_set(item)

    #
    #Takes input from Password Text Box on both enter ra button Press
    def PasswordEntry(self):
        password = self.entryPassword.get()
        

    def PasswordEnter(self,event):
        password = self.entryPassword.get()

    #
    # Search Function 
    def SearchOnEnter(self,event):
        global findItem 
        findItem = self.entryVariable.get()
       
        currentFocus = self.tree.focus()
        # backend.updatePasswords((self.tree.item(currentFocus)['values'][0],self.entryVariable.get()))
        #should indicate this some other way since the button is reclickable
        #self.labelVariable.set(self.entryVariable.get() + "Submitted the password!")

        #Auto selects the text field
        self.entry.focus_set()
        self.entry.selection_range(0,Tkinter.END)
        # print self.tree.item(currentFocus)['values'][0],self.entryVariable.get()

    #hides all secure entries from the tree         
    def OnHideClick(self, event):
        for entry in self.tree.get_children():
            if str(item['values'][0]) == "Secure":
                self.tree.delete(entry)

    #On Button Click Activity
    def OnButtonClick(self):
        global findItem 
        findItem = self.entryVariable.get()
       # print findItem 
        print findItem
        currentFocus = self.tree.focus()
        # backend.updatePasswords((self.tree.item(currentFocus)['values'][0],self.entryVariable.get()))
        #should indicate this some other way since the button is reclickable
        #self.labelVariable.set(self.entryVariable.get() + "Submitted the password!")

        #Auto selects the text field
        self.entry.focus_set()
        self.entry.selection_range(0,Tkinter.END)

        # print self.tree.item(currentFocus)['values'][0],self.entryVariable.get()

    # Some Appearance modifications
    def createWidgits(self):
        top=self.winfo_toplevel()
        top.rowconfigure(0,weight=1)
        top.columnconfigure(0,weight=1)
        self.rowconfigure(0,weight=1)
        self.columnconfigure(0, weight=1, uniform=True)
        
    def OnScan(self):
        treeContents = backend.getDeviceList()
        for i in self.tree.get_children():
            self.tree.delete(i) #clears current values from tree
        #Populates the database with Devices
        
        #iterates over inputlist and inserts it all into the tree
        for entry in treeContents:
            self.tree.insert("","end", value = (entry[0], entry[1], entry[2], entry[3]))


    def initialize(self):
        # Appearance
        self.bigFont = tkFont.Font(family='times', size=13)
        self.option_add('*Button*font', self.bigFont)

        self.parent.resizable(False,False)
        self.parent.grid_rowconfigure(0,weight=1)
        self.parent.title("K4TRESS")
        self.grid_columnconfigure(0, weight=1)

        #Tree Building
        self.tree = ttk.Treeview(selectmode="extended",columns=('IP','MAC Address','Device','Security'), show="headings")
        self.treeview = self.tree

        #
        # Search Bar   
        #Device Search Entry Field
        self.entryVariable = Tkinter.StringVar()
        self.entry = Tkinter.Entry(self.parent, textvariable=self.entryVariable)
        self.entry.grid(column=0,columnspan=3,rowspan=1,row=0,sticky=Tkinter.W+Tkinter.E+ Tkinter.N + Tkinter.S)   
        self.entry.bind("<Return>", self.SearchOnEnter)

        #Button to search for Devices in SQL Database
        button = Tkinter.Button(self.parent, text=u"Search Devices", command=self.OnButtonClick)
        button.grid(column=3,columnspan=2,rowspan=1,row=0, sticky=Tkinter.W + Tkinter.E + Tkinter.N + Tkinter.S)

        #
        # Starts Scan Script
        #Button to Search f +r devices 
        search = Tkinter.Button(self.parent, text=u"Scan", command = self.OnScan)
        search.grid(column=3, columnspan=2, row=1, sticky=Tkinter.W + Tkinter.E + Tkinter.N)
        
        #
        # Password Field
        # Password Entry Field
        self.entryPassword = Tkinter.StringVar()
        self.entry = Tkinter.Entry(self.parent, textvariable=self.entryPassword)
        self.entry.grid(column=3,row=4,columnspan=1, sticky=Tkinter.W+Tkinter.E+ Tkinter.N + Tkinter.S)
        self.entryPassword.set(u"Enter New Password!")

        #Button to Submit password to Devices in SQL Database
        button = Tkinter.Button(self.parent, text=u"Submit Password", command=self.PasswordEntry)
        button.grid(column=2,columnspan=1,row=4, sticky=Tkinter.W + Tkinter.E + Tkinter.N + Tkinter.S)
        self.entry.bind("<Return>", self.PasswordEnter)

        #Auto selects the text field
        self.entry.focus_set()
        self.entry.selection_range(0,Tkinter.END)

        #
        # Secure Toggle
        #Button to hide secure entries, cleaning up the view
        hide = Tkinter.Button(self.parent, text=u"Toggle Secure View", command = self.OnHideClick)
        #may need to reposition button within GUI
        hide.grid(column=3, columnspan=2,rowspan=1,row=3,sticky=Tkinter.W + Tkinter.E + Tkinter.S)

        #
        #   TREE/DATABASE CONFIG
        # Tree scroll bar
        verticle = ttk.Scrollbar(orient='vertical', command=self.tree.yview)
        verticle.grid(row=1,rowspan=3, column=2, sticky='nes')
        self.tree.grid(row=1,rowspan=3,columnspan=3,sticky='news')
        self.tree.configure(yscrollcommand=verticle.set)

        # Columnn Customization
        self.tree.heading("Device", text="Device Name")
        self.tree.heading("IP",text="IP")
        self.tree.heading("MAC Address", text="MAC Address")
        self.tree.heading("Security", text="Secure")

        self.tree.column('#0',width=0)
        self.tree.column("IP", stretch=True,width=50)
        self.tree.column("MAC Address", stretch=True)
        self.tree.column("Device", stretch=True)
        self.tree.column("Security",stretch=True, width=50)

def main():
    root=Tkinter.Tk()
    root.geometry('{}x{}'.format(1000, 300))
    d=k4tress_tk(root)
    root.mainloop()


if __name__ == "__main__":
    main()