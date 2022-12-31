import tkinter

class ucForm():
    def __init__ (self, parent, username):
        tkinter.Tk.__init__(self,parent)
        self.parent = parent
        password=''
        self.initialize(username, password)

    def initialize(self, username, password):
        self.grid()

        self.lblusername = tkinter.Label(self, text="Username:")
        self.lblusername.grid(row=0, column=0, sticky="w")
        self.lblpassword = tkinter.Label(self, text="Password:")
        self.lblpassword.grid(row=1, column=0, sticky="w")

        self.usernameVariable = tkinter.StringVar()
        self.username = tkinter.Entry(self, textvariable=self.usernameVariable)
        self.username.insert(0,username)
        self.username.grid(row=0, column=1,sticky="w")

        self.passwordVariable = tkinter.StringVar()
        self.password = tkinter.Entry(self, textvariable=self.passwordVariable)
        self.password.insert(0,password)
        self.password.grid(row=1, column=1, sticky="w")

if __name__ == "__main__":
    app = ucForm(None)
    app.title('Provide credentials')
    app.mainloop()