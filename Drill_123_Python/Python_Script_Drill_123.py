#Python Drill 123 (GUI)
#David A. Simar



from tkinter import *
from tkinter import filedialog
import tkinter as tk

import os
import shutil
from datetime import datetime

import sqlite3




class ParentWindow(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        self.master = master
        self.master.minsize(500,170)
        self.master.maxsize(500,170)

        self.master.title("Check files")
        self.master.configure(bg="#f0f0f0")

        self.Browse = StringVar()
        self.BrowseDes = StringVar()

        self.btnBrowse = Button(self.master, text="Browse...", width=12, height=1, command=self.selectDirectory)
        self.btnBrowse.grid(row='0', column='0', padx=(15,0) , pady=(30,0))

        self.btnBrowseDes = Button(self.master, text="Browse...", width=12, height=1, command=self.selectDesDirectory)
        self.btnBrowseDes.grid(row='1', column='0', padx=(15,0) , pady=(10,0))

        self.btnCheck = Button(self.master, text="Check for files...", width=12, height=2, command=self.cutPasteTXT)
        self.btnCheck.grid(row='2', column='0', padx=(15,0) , pady=(10,0))

        self.txtBrowse_source = Entry(self.master,text=self.Browse, font=("Helvetica", 10), fg='black', bg='white')
        self.txtBrowse_source.grid(row='0', column='1', padx=(30,15), pady=(40,10), columnspan=2, sticky=W+E)

        self.txtBrowse_des = Entry(self.master,text=self.BrowseDes, font=("Helvetica", 10), fg='black', bg='white')
        self.txtBrowse_des.grid(row='1', column='1', padx=(30,15), pady=(10,0), columnspan=2, sticky=W+E)

        self.btnClose = Button(self.master, text="Close Program", width=12, height=2, command=self.close)
        self.btnClose.grid(row='2', column='2', padx=(0,15) , pady=(10,0), sticky=SE)

        self.master.columnconfigure(1,weight=1)


    def close(self):
        self.master.destroy()

    def selectDirectory(self):
        self.txtBrowse_source.delete(0, END)
        global selectDir
        selectDir = filedialog.askdirectory()
        self.txtBrowse_source.insert(0,selectDir)
        sourcePath = self.txtBrowse_source.get()

    def selectDesDirectory(self):
        self.txtBrowse_des.delete(0, END)
        global selectDirDes
        selectDirDes = filedialog.askdirectory()
        self.txtBrowse_des.insert(0,selectDirDes)
        desPath = self.txtBrowse_des.get()

    def cutPasteTXT(self):
        filePath = selectDir
        destPath = selectDirDes
        directoryFiles = os.listdir(filePath)
        conn = sqlite3.connect('Python123.db')

        with conn:
            cur = conn.cursor()
            cur.execute("create table if not exists tbl_files ( \
                id integer primary key autoincrement, \
                col_fileName text)")
            for file in directoryFiles:
                if file.endswith('.txt'):
                    abPath = os.path.join(filePath,file)
                    fileModTime = os.path.getmtime(abPath)
                    convertedModTime = datetime.fromtimestamp(fileModTime).strftime('%Y-%m-%d %H:%M:%S')
                    cur.execute("insert into tbl_files(col_fileName) values (?)", \
                    (file,))
                    print("File Name: {} \nLast Modified: {}\n".format(file,convertedModTime))
                    shutil.move(filePath+"/"+file,destPath)
            conn.commit()
        conn.close()
        
        
if __name__ == "__main__":
    root = tk.Tk()
    App = ParentWindow(root)
    root.mainloop()
