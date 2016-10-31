# !/usr/bin/python
# -*- coding: iso-8859-1 -*-

import Tkinter
import tkFileDialog

from Tkinter import Frame, Label, Menu

import ttk
import tkFont

import backend


class k4tress_tk(Tkinter.Frame):

    def __init__(self, parent):
        global top
        global password
        global treeContent

        Tkinter.Frame.__init__(self, parent)
        self.variable = Tkinter.StringVar()
        self.parent = parent
        self.initialize()
        self.createWidgits()
        backend.initialSetup()

        # Menu Support
        self.master.config(menu=self.menubar)

    def script(self):
        # Code for importing scripts goes here
        self.ftypes = [('Python Scripts', '*.py'), ('Shell Scripts', '*.sh')]
        dlg = tkFileDialog.Open(self, filetypes=self.ftypes)
        fm = dlg.show()
        # File Menu

        if fm != ' ':
            self.script = self.readscript(fm)

    # Should probally pass file to the backend
    def readscript(self, filename):
        f = open(filename, "r")
        # TODO with script

        def info():
            x = 0
            # Code for any using information goes here

    def PasswordEnter(self, event):
        self.password = self.entryPassword.get()
        # backend.updatePasswords((self.tree.item(currentFocus)['values'][0], password))
        # should indicate this some other way since the button is reclickable
        # self.labelVariable.set(self.entryVariable.get() + "Submitted the password!")

    def searchResult():
        self.variable.set("Sorry, item not found!")

    def searchItem(self, branch, findItem):
        compare = False
        if self.tree.item(branch)["values"][0] == findItem or self.tree.item(branch)["values"][1] == findItem or self.tree.item(branch)["values"][2] == findItem:
            compare = True

        return compare

    # hides all secure entries from the tree
    def OnHideClick(self):
        for item in self.treeContent:
            if backend.secureTest(item['values'][0]):
                item['values'][3] = "Secured"
            else:
                item['values'][3] = "Unsecured"

    # Both Search Function and onButtonClick do the same thing
    # Search Function
    # self.tree.item(currentFocus)['values'][0],self.entryVariable.get()
    def SearchOnEnter(self, event):
        global findItem
        findItem = self.entryVariable.get()
        notFound = True
        treeContent = self.tree.get_children()
        for branch in treeContent:
            if self.searchItem(branch, findItem):
                self.tree.selection_set(branch)
                notFound = False

        if notFound:
            self.searchResult

    # Some Appearance modifications
    def createWidgits(self):
        top = self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1, uniform=True)
        self.variable.set("Search Ready")
        # Menu Functionality
        # Functionality for importing script
        self.menubar = Menu(master=self)
        self.filemenu = Menu(self.menubar, tearoff=0)

        self.menubar.add_command(label="Scan", command=self.OnScan)
        self.menubar.add_cascade(label="Options", menu=self.filemenu)
        self.filemenu.add_command(label="Scripts", command=self.script)
        self.filemenu.add_command(label="Info", command=self.info)

    def OnScan(self):
        self.treeContents = backend.getDeviceList()
        for i in self.tree.get_children():
            self.tree.delete(i)

        # iterates over inputlist and inserts it all into the tree
        for entry in self.treeContents:
            self.tree.insert(
                "", 0, value=(entry[0], entry[1], entry[2], entry[3]))

    def initialize(self):
        # Appearance
        self.bigFont = tkFont.Font(family='times', size=13)
        self.option_add('*Button*font', self.bigFont)

        self.parent.resizable(True, True)
        self.parent.grid_rowconfigure(0, weight=1)
        self.parent.title("SpaceSecure")
        self.grid_columnconfigure(0, weight=1)

        # Tree Building
        self.tree = ttk.Treeview(selectmode="extended", columns=(
            'IP', 'MAC Address', 'Device', 'Security'), show="headings")
        self.treeview = self.tree

        # Search Bar
        # Device Search Entry Field
        self.entryVariable = Tkinter.StringVar()
        self.entry = Tkinter.Entry(
            self.parent, textvariable=self.entryVariable)

        # Search and Status of Search
        Label(self.parent, textvariable=self.variable, relief=Tkinter.SUNKEN,
              font=self.bigFont).grid(row=0, column=0, sticky='wnes')
        self.entry.grid(column=3, columnspan=2, row=0, sticky='nesw')

        self.entry.bind("<Return>", self.SearchOnEnter)

        # Password Field
        # Password Entry Field
        self.entryPassword = Tkinter.StringVar()
        self.entry = Tkinter.Entry(
            self.parent, textvariable=self.entryPassword)
        self.entry.grid(column=3, row=4, columnspan=2, sticky='new')
        self.entryPassword.set(u"Enter New Password!")

        # Button to Submit password to Devices in SQL Database
        button = Tkinter.Button(
            self.parent, text=u"Submit Password", command=self.PasswordEnter)
        button.grid(column=3, columnspan=2, row=3, sticky='swe')
        self.entry.bind("<Return>", self.PasswordEnter)

        # Secure Toggle
        # Button to hide secure entries, cleaning up the view
        hide = Tkinter.Button(
            self.parent, text=u"Toggle Secure View", command=self.OnHideClick,)
        # may need to reposition button within GUI
        hide.grid(column=3, columnspan=2, row=1, sticky='nwe')

        # TREE/DATABASE CONFIG
        # Tree scroll bar
        verticle = ttk.Scrollbar(orient='vertical', command=self.tree.yview)
        verticle.grid(row=1, rowspan=3, column=2, sticky='nes')
        self.tree.grid(row=1, column=0, rowspan=3, columnspan=3, sticky='news')
        self.tree.configure(yscrollcommand=verticle.set)

        # Columnn Customization
        self.tree.heading("Device", text="Device Name")
        self.tree.heading("IP", text="IP")
        self.tree.heading("MAC Address", text="MAC Address")
        self.tree.heading("Security", text="Secure")
        # Column Settings Continued
        self.tree.column('#0', width=0)
        self.tree.column("IP", stretch=True, width=90)
        self.tree.column("MAC Address", stretch=True)
        self.tree.column("Device", stretch=True)
        self.tree.column("Security", stretch=True, width=80)


def main():
    root = Tkinter.Tk()
    root.geometry('{}x{}'.format(750, 280))
    d = k4tress_tk(root)
    root.mainloop()

if __name__ == "__main__":
    main()
