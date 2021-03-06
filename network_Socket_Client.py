from email.mime import application
from multiprocessing.connection import Client
from pydoc import cli
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

import Client

HOST = "127.0.0.1"
SERVER_PORT= 65432
FORMAT = "utf8"
LOGIN= "login"
LOGOUT = "logout"
PATH = "1.png"

def TotalContact(client):
    # list=[]
    # option = None
    # count = 0
    # while option != 'end':
    #     list.append([])
    #     for i in range(0,6):
    #         list[count].append(client.recv(1024).decode(FORMAT))
    #         client.sendall(list[count][i].encode(FORMAT))
    #     count += 1
    #     option = client.recv(1024).decode(FORMAT)
    # return list
    list = []
    item = client.recv(2048).decode(FORMAT)
    while (item != "end"):
        print(type(item))
        list.append(item)
        #response
        client.sendall("ok".encode(FORMAT))
        item = client.recv(2048).decode(FORMAT)
    
    return list

class TotalContactsWindow(tk.Frame):
    def __init__(self, parent, appController):
        tk.Frame.__init__(self, parent)

        #self.pack(side=tk.LEFT, padx=20)
        self.tv=ttk.Treeview(self)

        # Define our columns
        self.tv['column']=("ID","Name","Avatar","Download")
        
        # Formate our columns
        self.tv.column("#0",width=0,stretch=NO)
        self.tv.column("ID",anchor=W,width=75)
        self.tv.column("Name",anchor=W,width=200)
        self.tv.column("Avatar",anchor=CENTER,width=200)
        self.tv.column("Download",anchor=CENTER,width=75)
        
        # Create heading
       # tv.heading("#0",text="ID",anchor=CENTER)
        self.tv.heading("ID",text="ID",anchor=CENTER)
        self.tv.heading("Name",text="Name",anchor=CENTER)
        self.tv.heading("Avatar",text="Avatar",anchor=CENTER)
        self.tv.heading("Download",text="Download",anchor=CENTER)
        
        img=ImageTk.PhotoImage(Image.open(str(1)+".png"))

        my_label=Label(image=img)
        my_label.pack()

        self.tv.pack(pady=20)

        my_img=Label(image=img)
        my_img

        btn_download=tk.Button(self,text="Download avatar", command=lambda:Client.getFullImageFile(client))
        btn_download.pack()

        btn_logout=tk.Button(self,text="Back", command=lambda:self.back(appController))
        btn_logout.pack()
        # Pack to the screen
        self.tv.pack(pady=20)
    def back(self,appController):
        for item in self.tv.get_children():
            self.tv.delete(item)
        appController.ShowPage(SelectOptionWindow)      
            
        

        

class SpecificContactWindow(tk.Frame):
    def __init__(self, parent,appController):
        tk.Frame.__init__(self,parent)

        #img=Image.open(PATH)
        #img2=ImageTk.PhotoImage(img)
        #label_title=tk.Label(self,image=img2)
        #label_title.pack()
        self.label_mu=tk.Label(self,text="")
        btn_logout=tk.Button(self,text="Back", command=lambda:appController.ShowPage(SelectOptionWindow))

        self.label_mu.pack()
        btn_logout.pack()
        # global img
        #img.show()

class LogInWindow(tk.Frame):
    def __init__(self, parent,appController):
        tk.Frame.__init__(self,parent)

        label_title =tk.Label(self, text="LOGIN")
        label_user=tk.Label(self,text="username ")
        label_pswd=tk.Label(self,text="password ")

        self.label_notice=tk.Label(self, text="")
        self.entry_user=tk.Entry(self,width=20, bg='light yellow',borderwidth=5)
        #self.entry_user.insert(0,"Ex: lengocduc195@gmail.com")
        self.entry_pswd=tk.Entry(self,width=20, bg='light yellow',borderwidth=5)

        button_log=tk.Button(self, text="LOG IN", command=lambda:appController.LogIn(self, client))
        button_log.configure(width=10)

        label_title.pack()
        label_user.pack()
        self.entry_user.pack()
        label_pswd.pack()
        self.entry_pswd.pack()
        self.label_notice.pack()
        button_log.pack()

        #canvas=Canvas(self, width=500, height=300)
        #canvas.pack()
        # Create a line in canvas widget
        #canvas.create_line(200, 25, 200, 200, width=5)
        # Create a dashed line
        #canvas.create_line(210, 25,410 , 200,fill='red', dash=(10,5), width=2)

        #Label(self, text="I have default font-size").pack(pady=40)
        #Label(self, text="I have default font-size").pack(pady=20)
        #Label(self, text="I have default font-size",font=("Arial",25)).pack(pady=20)

class SelectOptionWindow(tk.Frame):
    def __init__(self,parent, appController):
        tk.Frame.__init__(self, parent)

        label_title=tk.Label(self, text="HOME PAGE",font="Arial,45")
        label_user=tk.Label(self,text="Find")
        self.entry_user=tk.Entry(self,width=20, bg='light yellow',borderwidth=5)
        btn_SearchList=tk.Button(self,text="Search List",command=lambda:appController.ShowTotalContact(TotalContactsWindow,client))
        btn_Search=tk.Button(self,text="Search",command=lambda:appController.ShowSpecificContact(self,client))
        btn_logout=tk.Button(self,text="Log Out", command=lambda:appController.LogOut(client))
        self.label_notice1=tk.Label(self, text="")
        self.label_notice2=tk.Label(self, text="")
        self.label_notice3=tk.Label(self, text="")


        label_title.pack()
        self.label_notice1.pack(pady=5)
        btn_SearchList.pack()
        self.label_notice2.pack()
        self.entry_user.pack()
        btn_Search.pack()
        #label_user.grid(row=3,column=3)
        #self.entry_user.grid(self,row=6,column=3)
        self.label_notice3.pack(pady=5)
        btn_logout.pack()

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.title("Socket Application")
        self.geometry("900x300")
        self.resizable(width=True, height=True)

        container=tk.Frame()
        container.configure(bg="red")
        
        container.pack()

        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0,weight=1)

        self.frames={}
        for F in (LogInWindow,SelectOptionWindow,SpecificContactWindow,TotalContactsWindow):
            frame=F(container, self)
            frame.grid(row=0,column=0,sticky="nsew")
            self.frames[F]=frame

        self.frames[LogInWindow].tkraise()

    def ShowPage(self, FrameClass):
        self.frames[FrameClass].tkraise()
        

    def LogIn(self, curFrame, sck):
        try:
            # Get data from box
            client.sendall(LOGIN.encode(FORMAT))
            client.recv(1024)
            user=curFrame.entry_user.get()
            pswd=curFrame.entry_pswd.get()
            client.sendall(user.encode(FORMAT))
            client.recv(1024)

            client.sendall(pswd.encode(FORMAT))
            accepted = int(client.recv(1024).decode(FORMAT))

            # If boxes are empty
            if user == "" or pswd == "":
                curFrame.label_notice["text"]="Fields cannot be empty"
                return
            
            print(user, pswd)
            if(accepted==2):
                curFrame.label_notice["text"]="Invalid password"
                return
            elif(accepted==0):
                curFrame.label_notice["text"]="Account has been login by another"
                return
            else:
                self.ShowPage(SelectOptionWindow)

        
        except:
            print("Error: Server iss not responding")

    def ShowTotalContact(self, curFrame, sck):
        sck.sendall(Client.TOTALCONTACT.encode(FORMAT))
        sck.recv(1024)
        ListContacts = TotalContact(sck)
        i = 1
        self.listSmallAvaPath=[]
        for contanct in ListContacts:
            contanct = contanct[1:len(contanct)-1]
            contanct = contanct.split(', ')
            self.frames[TotalContactsWindow].tv.insert(parent='',index='end',iid=i,text="",values=(contanct[0],contanct[1],contanct[5],"Down"))
            self.listSmallAvaPath.append(contanct[5])
            i +=1
        self.ShowPage(curFrame)

    def ShowSpecificContact(self,curFrame,sck):
        ID = curFrame.entry_user.get()
        if(ID==''):
            self.frames[SelectOptionWindow].label_notice3["text"] = "Field can not be empty"
        else:
            sck.sendall(Client.SPECONTACT.encode(FORMAT))
            SpeClient = Client.GetSpecificContact(sck,ID)
            if SpeClient == 'None':
                self.frames[SpecificContactWindow].label_mu["text"] = "Not Found"
            else:
                self.frames[SpecificContactWindow].label_mu["text"] = SpeClient
            self.ShowPage(SpecificContactWindow)

    def LogOut(self, sck):
        sck.sendall(LOGOUT.encode(FORMAT))
        sck.recv(1024)
        self.ShowPage(LogInWindow)

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print("CLIENT SIDE")
try:
    client.connect( (HOST, SERVER_PORT) )
    print("client address:",client.getsockname())
except:
    print("Unable to connect to HOST")
app=App()
#app.showPage(HomePage)
app.mainloop()
client.sendall(LOGOUT.encode(FORMAT))
client.recv(1024)

    