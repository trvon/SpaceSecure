import Tkinter
# import tkMessageBox


class Menu(Tkinter.Frame):

    global cred

    def __init__(self, master):
        Tkinter.Frame.__init__(self, master)
        self.master = master

    def loginScreen(self):
        # Login Label
        self.master.title("Password")
        self.label_1 = Tkinter.Label(self, text="Username")
        self.label_2 = Tkinter.Label(self, text="Password")
        # Login Fields
        self.entry_1 = Tkinter.Entry(self)
        self.entry_2 = Tkinter.Entry(self, show="*")
        # Login Layout
        self.label_1.grid(row=0, sticky='e')
        self.label_2.grid(row=1, sticky='e')
        self.entry_1.grid(row=0, column=1)
        self.entry_2.grid(row=1, column=1)

        self.login = Tkinter.Button(
            self, text="Login", command=self.loginButton)
        self.login.grid(columnspan=2)
        self.pack()

    def loginButton(self):
        # print("Clicked")
        username = self.entry_1.get()
        password = self.entry_2.get()
        cred = [username, password]
        self.master.destroy()
        return cred
        # if username == "john" and password == "password":
        # tm.showinfo("Login info", "Welcome John")
        # else:
        # tm.showerror("Login error", "Incorrect username")
