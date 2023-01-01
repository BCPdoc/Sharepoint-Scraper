# https://www.youtube.com/playlist?list=PL0MxHK9qnVo4koZLFrOsNuEEZixV1_JAu
# https://www.pythontutorial.net/tkinter/tkinter-treeview/#:~:text=Introduction%20to%20the%20Tkinter%20Treeview,has%20one%20or%20more%20columns.
# https://www.tutorialspoint.com/python/tk_menu.htm
# https://stackoverflow.com/questions/70552509/clearing-a-tkinter-root-subform-from-within-a-separate-function
# https://www.pythontutorial.net/tkinter/tkinter-toplevel/
# https://stackoverflow.com/questions/45171328/grab-set-in-tkinter-window
# https://docs.python.org/3/library/configparser.html
# https://www.plus2net.com/python/tkinter-treeview.php

import tkinter as tk
from tkinter import ttk
import sys
import configparser
from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.user_credential import UserCredential
import threading

class MultiPromptWindow(object):
    def __init__(self, parent, title, data):
        self.toplevel=tk.Toplevel(parent)
        self.toplevel.title(title)
        self.answers=[]
        self.frame=tk.Frame(self.toplevel)
        self.frame.pack(expand=True)
        self.labels=[]
        self.entries=[]

        self.count=0
        for prompt, value in data:
            self.answers.append(value)

            newlabel=ttk.Label(self.frame, text=prompt)
            newlabel.grid(row=self.count, column=0, sticky="w")
            self.labels.append(newlabel)

            newentry=ttk.Entry(self.frame)
            newentry.insert(0, value)
            newentry.grid(row=self.count, column=1, sticky="w")
            self.entries.append(newentry)
            if self.count == 0:
                newentry.focus()

            self.count+=1
        
        def btnOK_click():
            for i in range (0,len(self.entries), 1):
                self.answers[i]=self.entries[i].get()
            self.toplevel.destroy()

        btnOK = ttk.Button(self.frame, text="OK", command=btnOK_click)
        btnOK.grid(row=self.count, column=1, columnspan=2, sticky='w')

    def show(self):
        self.toplevel.grab_set()
        self.toplevel.wait_window()
        return self.answers

class ScraperConfig(configparser.ConfigParser):
    def __init__(self):
        super().__init__()
        self.configfilename='config.ini'
        self.sectionname='Credentials'
        self.username='username'
        self.listname='Site'
        #self.sitename='Sites'
        self.descname='description'
        self.urlname='address'
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
        for i in range(0,len(sitearray),1):
            self[self.listname + str(i)]={}
            self[self.listname + str(i)][self.descname]=sitearray[i][0]
            self[self.listname + str(i)][self.urlname]=sitearray[i][1]
    
    def getsites(self):
        sitearray=[]
        i=0
        while self.listname + str(i) in self:
            data=[]
            for key,path in self.items(self.listname + str(i)):
                if key == self.descname:
                    desc=path
                if key == self.urlname:
                    url=path
            sitearray.append([desc,url])
            i+=1
        return sitearray
    
    def save(self):
        with open(self.configfilename, 'w') as configfile:
            self.write(configfile)

class Scraper(object):
    def __init__(self, username, password, site):
        
        credentials = UserCredential(username, password)
        self.ctx = ClientContext(site).with_credentials(credentials)

    def getRootFolder(self):
        target_folder_url = "Shared Documents"
        root_folder = self.ctx.web.get_folder_by_server_relative_path(target_folder_url)
        return root_folder

    
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
            data = [['Add a description:',''],['Paste site URL:','']]
            newsite=MultiPromptWindow(self,'Add new site', data).show()
            if newsite[0] != '' and newsite[1] != '':
                self.sitearray.append(newsite)
                self.scraperconfig.setsites(self.sitearray)
                self.scraperconfig.save()
            
        def menuLogin_click():
            #self.username,self.password = CredentialWindow(self, self.username, self.password).show()
            data= [['Username:', self.username], ['Password:',self.password]]
            self.username, self.password = MultiPromptWindow(self, 'This is the title',data).show()
            self.scraperconfig.setusername(self.username)
            self.scraperconfig.save()
            processTree()

        def processTree():
            #for each tree item, get the link
            for child in tree.get_children():
                print('-- ', tree.item(child)['values'][0], ' - ', tree.item(child)['values'][1])
                #for each link, create a scraper object and return the folder object
                scraper = Scraper(self.username, self.password, tree.item(child)['values'][1])
                rootfolder = scraper.getRootFolder()
                enum_folder(rootfolder, child)
                tree.item(child, open=False)

        def enum_folder(parentfolder, parenttree):
            parentfolder.expand(["Files", "Folders"]).get().execute_query()
            tree.item(parenttree, open=True)
            for file in parentfolder.files:  # type: File
                print(file.properties['ServerRelativeUrl'])
            for folder in parentfolder.folders:  # type: Folder
                newtreeitem = addToTree(parenttree, folder)
                enum_folder(folder, newtreeitem)
        
        def addToTree(parenttree, folder):
            newtreeitem = tree.insert(parent=parenttree, index=tk.END, values=(folder.name,folder.serverRelativeUrl))
            return newtreeitem

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
            print('Tree items:')
            processTree()

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
        tree = ttk.Treeview(self, columns=columns) #, show='headings')
        tree.heading('Item', text = 'Item')
        tree.heading('Link', text = 'Link')

        for site in self.sitearray:
            tree.insert('', tk.END, values=(site[0], site[1]), open=True)
        #tree.insert('', tk.END, values=('Item 1', 'Link 1'))
        #tree.insert('', tk.END, values=('Item 2', 'Link 2'))
        tree.grid(row=0, column=0, sticky='w')

if __name__ == "__main__":
    app = App()
    app.mainloop()
