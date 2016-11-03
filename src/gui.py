# !/usr/bin/python
# -*- coding: iso-8859-1 -*-

# Authors: Rahul, Trvon, and Parker
# Contributors:

import Tkinter
import tkFileDialog
import os
# import tkColorChooser

from Tkinter import Label, Menu

import ttk
import tkFont
import webbrowser
import backend


class k4tress_tk(Tkinter.Frame):

    def __init__(self, parent):
        global top
        global password
        global treeContent
        global current
        Tkinter.Frame.__init__(self, parent)
        self.variable = Tkinter.StringVar()
        self.parent = parent
        self.grid(sticky='nwes')
        self.initialize()
        self.createWidgits()
        backend.initialSetup()
        # Menu Support
        self.master.config(menu=self.menubar)

    # Importing scripts support
    def script(self):
        # Code for importing scripts goes here
        self.ftypes = [('Python Scripts', '*.py'), ('Shell Scripts', '*.sh'),
                       ('C Scripts', '*.c')]
        dlg = tkFileDialog.Open(self, filetypes=self.ftypes)
        fm = dlg.show()
        # File Menu
        if fm != ' ':
            self.script = self.readscript(fm)

    # Reloads previously imported scripts
    def reloadScripts(self):
        for file in os.listdir("../src/import/"):
            self.name = os.path.basename(file)
            self.importTree.insert("", 0, values=self.name)

    # Deletes scripts in the window and in the import directory
    def scriptDelete(self):
        for item in self.importTree.selection():
            self.file = self.importTree.item(item)["values"][0]
            os.remove('../src/import/' + self.file)
            self.importTree.delete(item)

    # Should probally pass file to the backend
    def readscript(self, filename):
        self.file = os.path.basename(filename)
        backend.importscript(filename, self.file)
        self.importTree.insert("", 0, values=self.file)

    # Opens Github Repo until popup info window is configured
    def info(self):
        webbrowser.open_new_tab('https://github.com/trvon/SpaceSecure')

    # Changes the password of device that is accessible
    # NEEDS TO BE SETUP
    def PasswordButton(self):
        self.password = self.entryPassword.get()
        self.passSubmit(self.password)

    # Button linking to field, need to condense
    def PasswordEnter(self, event):
        self.password = self.entryPassword.get()
        self.passSubmit(self.password)

    def passSubmit(self, password):
        backend.updatePasswords(
            (self.tree.item(self.tree.focus())['values'][0], password))
        # should indicate this some other way since the button is reclickable
        self.labelVariable.set(password +
                               "Submitted the password!")

    # Search Bar alert functions
    def searchResult(self):
        self.variable.set('Sorry, item not found!')

    def defaultSearch(self, event):
        self.variable.set('Search Ready!')

    # Condense the compare of search
    def searchItem(self, branch, findItem):
        compare = False
        columnOne = self.tree.item(branch)["values"][0].lower()
        columnTwo = self.tree.item(branch)["values"][1].lower()
        columnThree = self.tree.item(branch)["values"][2].lower()
        if (columnOne.startswith(findItem) or columnTwo.startswith(findItem) or
                columnThree.startswith(findItem)):
            compare = True
        return compare

    # Search Function
    # self.tree.item(currentFocus)['values'][0],self.entryVariable.get()
    def SearchOnEnter(self, event):
        global findItem
        findItem = self.entryVariable.get().lower()
        notFound = True
        treeContent = self.tree.get_children()
        for branch in treeContent:
            if self.searchItem(branch, findItem):
                self.tree.focus(branch)
                self.tree.selection_set(branch)
                self.variable.set('Item Found!')
                notFound = False
        if notFound:
            self.searchResult()

    # TODO: Needs to be fixed
    # hides all secure entries from the tree
    def OnHideClick(self):
        for item in self.tree.get_children():
            if backend.secureTest(self.tree.item(item)["values"][0]):
                self.variable.set('Tested Devices is Secure')
                self.treeview.item(item)["values"][3] = "Secured"
            else:
                self.variable.set('Tested Devices is Unsecure')
                self.tree.item(item)["values"][3] = "Unsecured"

        # self.variable.set()
        # Add function where label is set to Username and Password
        # Scripted used to successfully get into device

    # Some Appearance modifications
    def createWidgits(self):
        top = self.winfo_toplevel()
        top.rowconfigure(3, weight=1)
        top.columnconfigure(3, weight=1)
        # Resizable settings
        top.columnconfigure(0, weight=1)
        top.rowconfigure(0, weight=0)
        top.columnconfigure(3, weight=0)
        self.columnconfigure(0, weight=1, uniform=True)
        self.variable.set('Search Ready!')
        # Menu Functionality
        # Functionality for importing script
        self.menubar = Menu(master=self, relief=Tkinter.RAISED)
        self.filemenu = Menu(self.menubar, tearoff=0)
        # Menu Buttons
        self.menubar.add_command(label="Scan", command=self.OnScan)
        self.menubar.add_separator()
        self.menubar.add_cascade(label="Options", menu=self.filemenu)
        self.filemenu.add_command(label="Scripts", command=self.script)
        self.filemenu.add_command(label="Info", command=self.info)
        # Adds previously loaded scripts
        self.reloadScripts()

    def OnScan(self):
        self.treeContents = backend.getDeviceList()
        # Clears Tree so tree doesn't duplicate
        for i in self.tree.get_children():
            self.tree.delete(i)
        # iterates over inputlist and inserts it all into the tree
        for entry in self.treeContents:
            self.tree.insert(
                "", 0, value=(entry[0], entry[1], entry[2], entry[3]))

    # GUI settings
    def initialize(self):
        # Appearance
        self.bigFont = tkFont.Font(family='times', size=13)
        self.option_add('*Button*font', self.bigFont)
        # Main from settings
        self.parent.resizable(True, True)
        self.parent.grid_rowconfigure(0, weight=3)
        self.parent.title("SpaceSecure")
        self.grid_columnconfigure(0, weight=1, minsize=25)
        # Tree Building
        self.tree = ttk.Treeview(selectmode="extended", columns=(
            'IP', 'MAC Address', 'Device', 'Security'), show="headings")
        self.treeview = self.tree
        # Script Tree
        self.importTree = ttk.Treeview(selectmode="extended",
                                       column=('Scripts'), show="headings")
        self.treeviewImport = self.tree
        # Search Bar
        # Device Search Entry Field
        self.entryVariable = Tkinter.StringVar()
        self.entry = Tkinter.Entry(
            self.parent, textvariable=self.entryVariable)
        # Search and Status of Search
        Label(self.parent, textvariable=self.variable, relief=Tkinter.SUNKEN,
              font=self.bigFont).grid(row=0, column=0, sticky='wnes')
        self.entry.grid(
            column=1, columnspan=4, row=0, rowspan=1, sticky='nesw')
        self.entry.bind('<Enter>', self.defaultSearch)
        self.entry.bind('<Return>', self.SearchOnEnter)

        # Password Field
        # Password Entry Field
        self.entryPassword = Tkinter.StringVar()
        self.entry = Tkinter.Entry(
            self.parent, textvariable=self.entryPassword)
        self.entry.grid(column=4, row=4, columnspan=3, sticky='new')
        self.entryPassword.set(u"Enter New Password!")
        self.entry.bind("<Return>", self.PasswordEnter)

        # Button to Submit password to Devices in SQL Database
        button = Tkinter.Button(
            self.parent, text=u"Submit Password", command=self.PasswordButton)
        button.grid(column=4, columnspan=2, row=3, sticky='swe')
        # Auto selects the text field
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)

        # Secure Toggle
        # Button to hide secure entries, cleaning up the view
        hide = Tkinter.Button(
            self.parent, text=u"Check Device", command=self.OnHideClick)
        # may need to reposition button within GUI
        hide.grid(column=4, columnspan=1, row=1, sticky='nwe')

        delete = Tkinter.Button(self.parent, text=u"Delete Script",
                                command=self.scriptDelete,)
        delete.grid(column=4, row=2, columnspan=1, sticky='nsew')

        # IMPORTED FILE VIEW
        self.scrollScript = ttk.Scrollbar(
            orient='vertical', command=self.importTree.yview)
        self.scrollScript.grid(
            row=3, rowspan=1, column=6, columnspan=1, sticky='nswe')
        # Script Tree Setup
        self.importTree.grid(
            row=3, column=4, rowspan=2, columnspan=1, sticky='news')
        self.importTree.configure(yscrollcommand=self.scrollScript.set)
        # Columns settings
        self.importTree.heading("Scripts", text="Scripts")
        self.importTree.column("Scripts", stretch=True)
        self.importTree.column('#0', width=0)

        # TREE/DATABASE CONFIG
        # Tree scroll bar
        self.verticle = ttk.Scrollbar(
            orient='vertical', command=self.tree.yview)
        self.verticle.grid(row=1, rowspan=3, column=2, sticky='nes')
        self.tree.grid(row=1, column=0, rowspan=3, columnspan=3, sticky='news')
        self.tree.configure(yscrollcommand=self.verticle.set)
        # Columnn Customization
        self.tree.heading("Device", text="Device Name")
        self.tree.heading("IP", text="IP")
        self.tree.heading("MAC Address", text="MAC Address")
        self.tree.heading("Security", text="Secure")
        # Column Settings Continued
        self.tree.column('#0', width=0)
        self.tree.column("IP", stretch=True, width=95)
        self.tree.column("MAC Address", stretch=True, width=120)
        self.tree.column("Device", stretch=True)
        self.tree.column("Security", stretch=True, width=80)


def main():
    root = Tkinter.Tk()
    root.geometry('{}x{}'.format(900, 280))
    d = k4tress_tk(root)
    root.mainloop()

if __name__ == "__main__":
    main()
