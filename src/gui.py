"""Thanks for looking under the hood."""

# !/usr/bin/python
# -*- coding: iso-8859-1 -*-

# Authors: Rahul, Trvon, and Parker
# Contributors:

import Tkinter as tkinter

import tkFileDialog
import os
import ttk
import tkFont
import webbrowser

from Tkinter import Label, Menu

import backend
import password


class SpaceSecure(tkinter.Frame):
    """class declaration of the object."""

    def __init__(self, parent):
        """Creation."""
        tkinter.Frame.__init__(self, parent)
        self.variable = tkinter.StringVar()
        global top
        global password
        global treeContent
        global current
        self.parent = parent
        self.grid(sticky='nwes')
        # Sets up features
        self.initialize()
        self.createwidgits()
        backend.initialSetup()
        # Menu Support
        self.master.config(menu=self.menubar)

    def script(self):
        """Importing scripts support to backend."""
        # Code for importing scripts goes here
        self.ftypes = [('Python Scripts', '*.py'), ('Shell Scripts', '*.sh'),
                       ('C Scripts', '*.c')]
        dlg = tkFileDialog.Open(self, filetypes=self.ftypes)
        fm = dlg.show()
        # File Menus
        if fm != ' ':
            self.script = self.readscript(fm)

    def runscript(self):
        """Function runs scripts against selected devices."""
        cred = password.checkroot()
        if cred != 0:
            for item in self.importTree.selection():
                self.file = self.importTree.item(item)["values"][0]
                for branch in self.tree.selection():
                    self.device = self.tree.item(branch)["values"][0]
                    # Pass to backend with username and password
                    backend.scriptrunpass(
                        self.file, self.device, cred[0], cred[1])
        else:
            for item in self.importTree.selection():
                self.file = self.importTree.item(item)["values"][0]
                for branch in self.tree.selection():
                    self.device = self.tree.item(branch)["values"][0]
                    # Pass to backend with username and password
                    backend.scriptrun(self.file, self.device)

    def reloadscripts(self):
        """Function reloads previously imported scripts."""
        for file in os.listdir("../src/import/"):
            self.name = os.path.basename(file)
            self.importTree.insert("", 0, values=self.name)

    def scriptdelete(self):
        """Function deletes selected scripts globally."""
        for item in self.importTree.selection():
            self.file = self.importTree.item(item)["values"][0]
            os.remove('../src/import/' + self.file)
            self.importTree.delete(item)

    def readscript(self, filename):
        """Should probally pass file to the backend."""
        self.file = os.path.basename(filename)
        backend.importscript(filename, self.file)
        self.importTree.insert("", 0, values=self.file)

    # Need to create an about popup informational page
    def info(self):
        """Function opens Github Repo."""
        webbrowser.open_new_tab('https://github.com/trvon/SpaceSecure')

    def clearpassword(self, event):
        """Function clears password field."""
        self.entry.delete(0, 'end')

    def passwordbutton(self):
        """Function should change device password."""
        self.password = self.entryPassword.get()
        self.passsubmit(self.password)

    def passwordenter(self, event):
        """Button linking to field, need to condense."""
        self.password = self.entryPassword.get()
        self.passSubmit(self.password)

    def passsubmit(self, password):
        """Function connects Password Submit field to button."""
        backend.updatePasswords(
            (self.tree.item(self.tree.focus())['values'][0], password))
        # should indicate this some other way since the button is reclickable
        self.labelVariable.set(password +
                               "Submitted the password!")

    def searchresult(self):
        """Search Bar alert functions."""
        self.variable.set('Sorry, item not found!')

    # Cosmetic function
    def defaultsearch(self, event):
        """Function sets search bar back to default."""
        self.variable.set('Search Ready!')

    # This was to short code used in other search function
    def searchitem(self, branch, finditem):
        """Condense the compare of search."""
        compare = False
        columnone = self.tree.item(branch)["values"][0].lower()
        columntwo = self.tree.item(branch)["values"][1].lower()
        columnthree = self.tree.item(branch)["values"][2].lower()
        if (columnone.startswith(finditem) or columntwo.startswith(finditem) or
                columnthree.startswith(finditem)):
            compare = True
        return compare

    def clearsearch(self):
        """Function clears text in search bar."""
        self.entrySearch.delete(0, 'end')

    # Search Function
    def searchonenter(self, event):
        """Function controls program search bar."""
        global findItem
        # Removes selected Items
        for branch in self.tree.selection():
            self.tree.selection_remove(branch)

        # Selects found items fitting the search
        findItem = self.entryVariable.get().lower()
        notfound = True
        itemcount = 0
        treecontent = self.tree.get_children()
        for branch in treecontent:
            if self.searchitem(branch, findItem):
                # self.itemLocation = self.treeview.index(branch)
                self.tree.focus(branch)
                self.tree.selection_add(branch)
                self.tree.see(self.tree.selection()[0])
                itemcount += 1
                self.variable.set('Item\'(s) Found: ' + str(itemcount))
                notfound = False
        if notfound:
            self.searchresult()
        self.clearsearch()

    # TODO: Needs to be fixed
    # hides all secure entries from the tree
    def onhideclick(self):
        """Function runs scripts against toggled devices."""
        if str(self.tree.selection()) == "":
            self.variable.set("No Item Selected")
        else:
            for item in self.tree.selection():
                if backend.secureTest(self.tree.item(item)["values"][0]):
                    self.variable.set('Tested Devices is Secure')
                    self.treeview.item(item)["values"][3].append("Secured")
                else:
                    self.variable.set('Tested Devices is Unsecure')
                    self.tree.item(item)["values"][3].append("Unsecured")

    # Some Appearance modifications
    def createwidgits(self):
        """Function Initializes some appearance features."""
        top = self.winfo_toplevel()
        # Resizable settings
        # Row Configurations
        top.rowconfigure(0, weight=0)
        top.rowconfigure(1, weight=0)
        top.rowconfigure(3, weight=0)
        top.rowconfigure(4, weight=1)
        # Column Configuration
        top.columnconfigure(0, weight=1)
        top.columnconfigure(2, weight=0)
        top.columnconfigure(3, weight=0)
        top.columnconfigure(4, weight=0)
        self.columnconfigure(0, weight=1, uniform=True)
        # Default alert bar settings
        self.variable.set('Search Ready!')
        # Menu Functionality
        # Functionality for importing script
        self.menubar = Menu(master=self, relief=tkinter.RAISED)
        self.filemenu = Menu(self.menubar, tearoff=0)
        # Menu Buttons
        self.menubar.add_command(label="Scan", command=self.onscan)
        self.menubar.add_separator()
        self.menubar.add_cascade(label="Options", menu=self.filemenu)
        self.filemenu.add_command(label="Scripts", command=self.script)
        self.filemenu.add_command(label="Info", command=self.info)
        # Adds previously loaded scripts to Tree
        self.reloadscripts()

    # Start Network Scan
    def onscan(self):
        """Function starts network scan."""
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
        """Everything else appearance."""
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
        self.entryVariable = tkinter.StringVar()
        self.entrySearch = tkinter.Entry(
            self.parent, textvariable=self.entryVariable)
        # Search and Status of Search
        Label(self.parent, textvariable=self.variable, width=75,
              relief=tkinter.SUNKEN, font=self.bigFont).grid(row=0, column=0,
                                                             sticky='wnes')
        self.entrySearch.grid(
            column=3, columnspan=4, row=0, rowspan=1, sticky='nesw')
        self.entrySearch.bind('<Enter>', self.defaultsearch)
        self.entrySearch.bind('<Return>', self.searchonenter)
        self.entrySearch.focus_set()

        # Password Field
        # Password Entry Field
        self.entryPassword = tkinter.StringVar()
        self.entry = tkinter.Entry(
            self.parent, textvariable=self.entryPassword)
        self.entry.grid(column=4, row=7, columnspan=4, sticky='new')
        self.entryPassword.set(u"Enter New Password!")
        self.entry.bind("<Return>", self.passwordenter)
        self.entry.bind('<FocusIn>', self.clearpassword)

        # Button to Submit password to Devices in SQL Database
        button = tkinter.Button(
            self.parent, text=u"Submit Password", command=self.passwordbutton)
        button.grid(column=4, columnspan=3, row=6, sticky='swe')
        # Auto selects the text field
        self.entry.selection_range(0, tkinter.END)

        # Secure Toggle
        # Button to hide secure entries, cleaning up the view
        hide = tkinter.Button(
            self.parent, text=u"Check Device", command=self.onhideclick)
        # may need to reposition button within GUI
        hide.grid(column=4, columnspan=3, row=1, sticky='nwe')
        delete = tkinter.Button(self.parent, text=u"Delete Script",
                                command=self.scriptdelete,)
        delete.grid(column=4, row=2, columnspan=3, sticky='nsew')

        # IMPORTED SCRIPT FILE VIEW
        # Scrollbar for script view window
        self.scrollScript = ttk.Scrollbar(
            orient='vertical', command=self.importTree.yview)
        self.scrollScript.grid(
            row=4, rowspan=2, column=6, columnspan=1, sticky='nswe')
        # Script Tree Setup
        self.importTree.grid(
            row=4, column=4, rowspan=2, columnspan=1, sticky='news')
        self.importTree.configure(yscrollcommand=self.scrollScript.set)
        # Columns settings
        self.importTree.heading("Scripts", text="Scripts")
        self.importTree.column("Scripts", stretch=True)
        self.importTree.column('#0', width=0)
        # Button For Starting import scripts
        self.startScript = tkinter.Button(
            self.parent, text=u"Run Script", command=self.runscript,)
        self.startScript.grid(column=4, columnspan=3, row=3, sticky='nswe')

        # TREE/DATABASE CONFIG
        # Tree scroll bar
        self.verticle = ttk.Scrollbar(
            orient='vertical', command=self.tree.yview)
        self.verticle.grid(row=1, rowspan=6, column=3, sticky='nes')
        self.tree.grid(row=1, column=0, rowspan=6, columnspan=4, sticky='news')
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
    """And here is the main."""
    root = tkinter.Tk()
    root.geometry('{}x{}'.format(900, 420))
    d = SpaceSecure(root)
    root.mainloop()

if __name__ == "__main__":
    main()
