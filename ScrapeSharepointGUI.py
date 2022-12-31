# https://www.youtube.com/playlist?list=PL0MxHK9qnVo4koZLFrOsNuEEZixV1_JAu
# https://www.pythontutorial.net/tkinter/tkinter-treeview/#:~:text=Introduction%20to%20the%20Tkinter%20Treeview,has%20one%20or%20more%20columns.
# https://www.tutorialspoint.com/python/tk_menu.htm
# https://stackoverflow.com/questions/70552509/clearing-a-tkinter-root-subform-from-within-a-separate-function
# https://www.pythontutorial.net/tkinter/tkinter-toplevel/
# https://stackoverflow.com/questions/45171328/grab-set-in-tkinter-window
# https://docs.python.org/3/library/configparser.html

import tkinter as tk
from tkinter import ttk
import sys
import configparser

class NewSiteWindow(object):
    def __init__(self,parent):
        self.toplevel=tk.Toplevel(parent)
        newsiteWindowSize='240x80'

        self.toplevel.geometry(newsiteWindowSize)
        self.toplevel.title('Add new site')

        self.newsite=''

        self.frame=tk.Frame(self.toplevel)
        self.frame.pack(expand=True)

        lblnewsite = ttk.Label(self.frame, text="Add this site:")
        lblnewsite.grid(row=0, column=0, sticky="w")
        self.txtNewsite = ttk.Entry(self.frame)
        self.txtNewsite.grid(row=0, column=1, columnspan=4, sticky="w")
        
        def btnOK_click():
            self.newsite = self.txtNewsite.get() 
            self.toplevel.destroy()
            
        btnOK = ttk.Button(self.frame, text="OK", command=btnOK_click)
        btnOK.grid(row=1, column=2, sticky='w')

    def show(self):
        self.toplevel.grab_set()
        self.toplevel.wait_window()
        return self.newsite
        
class MultiPromptWindow(object):
    def __init__(self, parent, title, data):
        self.toplevel=tk.Toplevel(parent)
        self.toplevel.title(title)
        self.count=0
        self.answers=[]
        self.frame=tk.Frame(self.toplevel)
        self.frame.pack(expand=True)
        self.labels=[]
        self.entries=[]

        for prompt, value in data:
            self.answers.append(value)

            newlabel=ttk.Label(self.frame, text=prompt)
            newlabel.grid(row=self.count, column=0, sticky="w")
            self.labels.append(newlabel)

            newentry=ttk.Entry(self.frame)
            newentry.insert(0, value)
            newentry.grid(row=self.count, column=1, sticky="w")
            self.entries.append(newentry)

            self.count+=1
        
        def btnOK_click():
            for i in range (0,len(self.entries), 1):
                self.answers[i]=self.entries[i].get()
            self.toplevel.destroy()

        btnOK = ttk.Button(self.frame, text="OK", command=btnOK_click)
        btnOK.grid(row=self.count, column=2, columnspan=2, sticky='w')

    def show(self):
        self.toplevel.grab_set()
        self.toplevel.wait_window()
        return self.answers

class CredentialWindow(object):
    def __init__(self, parent, username, password):
        #super().__init__(parent)
        self.toplevel=tk.Toplevel(parent)
        credentialWindowSize='240x80'

        self.toplevel.geometry(credentialWindowSize)
        self.toplevel.title('Provide credentials')

        self.username=username #"Test user name"
        self.password=password #''

        self.frame=tk.Frame(self.toplevel)
        self.frame.pack(expand=True)

        lblusername = ttk.Label(self.frame, text="Username:")
        lblusername.grid(row=0, column=0, sticky="w")
        lblpassword = ttk.Label(self.frame, text="Password:")
        lblpassword.grid(row=1, column=0, sticky="w")

        self.txtUsername = ttk.Entry(self.frame)
        self.txtUsername.insert(0, self.username)
        self.txtUsername.grid(row=0, column=1, columnspan=2,sticky="w")

        self.txtPassword = ttk.Entry(self.frame)
        self.txtPassword.insert(0,self.password)
        self.txtPassword.grid(row=1, column=1, columnspan=2, sticky="w")

        def btnOK_click():
            self.username = self.txtUsername.get() #self.varUsername.get()
            self.password = self.txtPassword.get()
            self.toplevel.destroy()

        btnOK = ttk.Button(self.frame, text="OK", command=btnOK_click)
        btnOK.grid(row=2, column=2, columnspan=2, sticky='w')

    def show(self):
        self.toplevel.grab_set()
        self.toplevel.wait_window()
        return self.username, self.password

class ScraperConfig(configparser.ConfigParser):
    def __init__(self):
        super().__init__()
        self.configfilename='config.ini'
        self.sectionname='Credentials'
        self.username='Username'
        self.listname='List'
        self.sitename='Sites'
        self.read(self.configfilename)
        self.sections()

    def getusername(self):
        if self.sectionname in self:
            return self[self.sectionname][self.username]
        else:
            return ''

    def setusername(self,username):
        self[self.sectionname]={}
        self[self.sectionname][self.username]=username

    def setsites(self,sitearray):
        self[self.listname]={}
        for i in range(0,len(sitearray),1):
            self[self.listname][self.sitename + str(i)]=sitearray[i]
    
    def getsites(self):
        sitearray=[]
        if self.listname in self:
            for key, path in self.items(self.listname):
                sitearray.append(path)
        return sitearray
    
    def save(self):
        with open(self.configfilename, 'w') as configfile:
            self.write(configfile)

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        #load existing username from file
        self.scraperconfig=ScraperConfig()
        self.username=self.scraperconfig.getusername()
        self.password=''
        self.sitearray=self.scraperconfig.getsites()

        def menuAdd_click():
            #newsite=NewSiteWindow(self).show()
            data = [['Paste site URL:','']]
            newsite=MultiPromptWindow(self,'Add new site', data).show()
            if newsite[0] != '':
                self.sitearray.append(newsite[0])
                self.scraperconfig.setsites(self.sitearray)
                self.scraperconfig.save()
            
        def menuLogin_click():
            #self.username,self.password = CredentialWindow(self, self.username, self.password).show()
            data= [['Username:', self.username], ['Password:',self.password]]
            self.username, self.password = MultiPromptWindow(self, 'This is the title',data).show()
            self.scraperconfig.setusername(self.username)
            self.scraperconfig.save()

        def menuDebug_click():
            #data= [['First prompt', 'First answer'], ['Second prompt','']]
            #answers = MultiPromptWindow(self, 'This is the title',data).show()
            #print ('Returned these answers:')
            #for answer in answers:
            #    print (answer)
            print('Username: ', self.username)
            print('Password: ', self.password)
            print('Sites: ')
            for site in self.sitearray:
                print('-- ', site)

        def menuExit_click():
            sys.exit(0)

        mainWindowSize='600x600'
        self.geometry(mainWindowSize)
        self.title('Sharepoint Scraper')

        # Add menu
        menubar = tk.Menu(self)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Login", command=menuLogin_click)
        filemenu.add_command(label="Add project", command=menuAdd_click)
        filemenu.add_command(label="Debug", command=menuDebug_click)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=menuExit_click)
        menubar.add_cascade(label="File", menu=filemenu)
        self.config(menu=menubar)

        # Add treeview
        columns = ('Item', 'Link')
        tree = ttk.Treeview(self, columns=columns, show='headings')
        tree.heading('Item', text = 'Item')
        tree.heading('Link', text = 'Link')

        tree.insert('', tk.END, values=('Item 1', 'Link 1'))
        tree.insert('', tk.END, values=('Item 2', 'Link 2'))
        tree.grid(row=0, column=0, sticky='w')

if __name__ == "__main__":
    app = App()
    app.mainloop()
