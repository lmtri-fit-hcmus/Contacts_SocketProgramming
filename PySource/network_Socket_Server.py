from http import server
import tkinter as tk
from tkinter import ttk 
from tkinter.ttk import *
import socket
from tkinter.ttk import Label
from tkinter import *
from PIL import ImageTk,Image
import sqlite3
from tkinter import Tk, Button, Canvas
from PIL import Image, ImageFont
from matplotlib import image

HOST = "127.0.0.1"
SERVER_PORT= 65432
FORMAT = "utf8"
LOGIN= "login"
PATH = "E:\\Python\\tkinter\\image\\1.png"

#       Hàm đăng nhập trên máy server 
class StartPage(tk.Frame):
    def __init__(self, parent,appController):
        tk.Frame.__init__(self,parent)

        #appController.resize(self,300,210)

        label_title =tk.Label(self, text="LOGIN")
        label_user=tk.Label(self,text="username ")
        label_pswd=tk.Label(self,text="password ")

        self.label_notice=tk.Label(self, text="")
        self.entry_user=tk.Entry(self,width=20, bg='light yellow',borderwidth=5)
        #self.entry_user.insert(0,"Ex: lengocduc195@gmail.com")
        self.entry_pswd=tk.Entry(self,width=20, bg='light yellow',borderwidth=5)

        button_log=tk.Button(self, text="LOG IN", command=lambda:[f() for f in [appController.logIn(self, client), appController.resize(self,300,500)]])
        button_log.configure(width=10)

        self.label_notice.pack()
        label_title.pack()
        label_user.pack()
        self.entry_user.pack()
        label_pswd.pack()
        self.entry_pswd.pack()
        self.label_notice.pack()
        button_log.pack()

#       Hàm hiển thị danh sách các máy client
class HomePage(tk.Frame):
    def __init__(self,parent, appController):
        tk.Frame.__init__(self, parent)

        #appController.resize(self,300,500)

        client_and_port={'U1984': '5',
                            'U34325': '2'}

        label_title=tk.Label(self, text="HOME PAGE",font="Arial,45")
        label_user=tk.Label(self,text="Client List")
        listbox1=Listbox(self)

        for x,y in enumerate(client_and_port):
            listbox1.insert(x+1,y)    
       
        def get_Port():
            entry1.delete(0,'end')
            cur_Client=listbox1.get(ANCHOR)
            entry1.insert(0,client_and_port[cur_Client])
        
        pass 
        
        button=Button(self,text="Send",command=lambda:appController.Send(self,client))
        btn_logout=tk.Button(self,text="Log Out", command=lambda:[f() for f in [appController.showPage(StartPage), appController.resize(self,300,210)]])
        button_Get_Port=Button(self,text="Get Port",command=get_Port)
        entry1=Entry(self,width=20)
        
       
        self.label_notice1=tk.Label(self, text="")
        self.label_notice2=tk.Label(self, text="")
        self.label_notice3=tk.Label(self, text="")
        self.label_notice4=tk.Label(self, text="")
        self.label_notice5=tk.Label(self, text="")


        label_title.pack()
        self.label_notice1.pack(pady=5)
        listbox1.pack(anchor=CENTER)
        self.label_notice3.pack()
        button_Get_Port.pack()
        self.label_notice4.pack()
        entry1.pack()
        self.label_notice2.pack()
        button.pack()
        self.label_notice5.pack(pady=5)
        btn_logout.pack()
        
    

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.title("Socket Application")
        self.geometry("300x210")
        self.resizable(width=FALSE, height=FALSE)

        container=tk.Frame()
        container.configure(bg="red")
        
        container.pack()
        #home_page.pack()

        #start_page.pack()

        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0,weight=1)

        #start_page=StartPage(container)
        #home_page=HomePage(container)

        #start_page.grid(row=0,column=0,sticky="nsew")
        #home_page.grid(row=0,column=0,sticky="nsew")

        #start_page.tkraise()
        
        #home_page.tkraise()

        self.frames={}
        for F in (StartPage,HomePage):
            frame=F(container, self)
            frame.grid(row=0,column=0,sticky="nsew")
            self.frames[F]=frame

        #self.frames[SearchListWindow].tkraise()
        #self.frames[SearchEntire].tkraise()
        #self.resize(self,300,210)
        self.frames[StartPage].tkraise()

    def showPage(self, FrameClass):
        self.frames[FrameClass].tkraise()
        

    def logIn(self, curFrame, sck):
        try:
            # Get data from box
            user=curFrame.entry_user.get()
            pswd=curFrame.entry_pswd.get()

            # If boxes are empty
            if user == "" or pswd == "":
                curFrame.label_notice["text"]="Fields cannot be empty"
                return
            
            print(user, pswd)

            #option=LOGIN
            #sck.sendall(option.encode(FORMAT))
            #sck.recv(1024)
            #sck.sendall(user.encode(FORMAT))
            #sck.recv(1024)
            #sck.sendall(pswd.encode(FORMAT))
            #sck.recv(1024)

            #msg = sck.recv(1024).decode(FORMAT)
            
            # ____________________
            # TEST
            
            msg='true'
            
            # ____________________
            if(msg=="fail"):
                curFrame.label_notice["text"]="Invalid password"
                return
            else:
                self.showPage(HomePage)

        
        except:
            print("Error: Server iss not responding")

    def Send(self,curFrame, sck):
        option=LOGIN
        sck.sendall(option.encode(FORMAT))
        sck.recv(1024)

    def resize(self,curFrame,w,h):
        self.geometry(f"{w}x{h}")
        

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print("CLIENT SIDE")

app=App()
#app.showPage(HomePage)
app.mainloop()