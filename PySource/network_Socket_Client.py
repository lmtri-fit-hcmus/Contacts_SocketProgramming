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
PATH = "1.png"

class SearchListWindow(tk.Frame):
    def __init__(self, parent, appController):
        tk.Frame.__init__(self, parent)

        #self.pack(side=tk.LEFT, padx=20)
        tv=ttk.Treeview(self)

        # Define our columns
        tv['column']=("ID","Name","Avatar","Download")
        
        # Formate our columns
        tv.column("#0",width=0,stretch=NO)
        tv.column("ID",anchor=W,width=75)
        tv.column("Name",anchor=W,width=200)
        tv.column("Avatar",anchor=CENTER,width=200)
        tv.column("Download",anchor=CENTER,width=75)
        
        # Create heading
       # tv.heading("#0",text="ID",anchor=CENTER)
        tv.heading("ID",text="ID",anchor=CENTER)
        tv.heading("Name",text="Name",anchor=CENTER)
        tv.heading("Avatar",text="Avatar",anchor=CENTER)
        tv.heading("Download",text="Download",anchor=CENTER)

        img=ImageTk.PhotoImage(Image.open(str(1)+".png"))

        my_label=Label(image=img)
        my_label.pack()
        tv.pack(pady=20)

        my_img=Label(image=img)
        my_img

        # Add data test
        # for i in range(1,5):
        #     tv.insert(parent='',index='end',iid=i,text="",values=(str(i),"Le Ngoc Duc",ImageTk.PhotoImage(Image.open(str(i)+".png")),"Down"))
        
        btn_logout=tk.Button(self,text="Log Out", command=lambda:appController.showPage(HomePage))
        btn_logout.pack()
        # Pack to the screen
        tv.pack(pady=20)

        

class SearchEntire(tk.Frame):
    def __init__(self, parent,appController):
        tk.Frame.__init__(self,parent)

        #img=Image.open(PATH)
        #img2=ImageTk.PhotoImage(img)
        #label_title=tk.Label(self,image=img2)
        #label_title.pack()

        label_mu=tk.Label(self,text="Heloo")
        btn_logout=tk.Button(self,text="Log Out", command=lambda:appController.showPage(HomePage))

        label_mu.pack()
        btn_logout.pack()
        # global img
        #img.show()

class StartPage(tk.Frame):
    def __init__(self, parent,appController):
        tk.Frame.__init__(self,parent)

        label_title =tk.Label(self, text="LOGIN")
        label_user=tk.Label(self,text="username ")
        label_pswd=tk.Label(self,text="password ")

        self.label_notice=tk.Label(self, text="")
        self.entry_user=tk.Entry(self,width=20, bg='light yellow',borderwidth=5)
        #self.entry_user.insert(0,"Ex: lengocduc195@gmail.com")
        self.entry_pswd=tk.Entry(self,width=20, bg='light yellow',borderwidth=5)

        button_log=tk.Button(self, text="LOG IN", command=lambda:appController.logIn(self, client))
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

class HomePage(tk.Frame):
    def __init__(self,parent, appController):
        tk.Frame.__init__(self, parent)

        label_title=tk.Label(self, text="HOME PAGE",font="Arial,45")
        label_user=tk.Label(self,text="Find")
        self.entry_user=tk.Entry(self,width=20, bg='light yellow',borderwidth=5)
        btn_SearchList=tk.Button(self,text="Search List",command=lambda:appController.showPage(SearchListWindow))
        btn_Search=tk.Button(self,text="Search",command=lambda:appController.showPage(SearchEntire))
        btn_logout=tk.Button(self,text="Log Out", command=lambda:appController.showPage(StartPage))
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
        self.geometry("700x200")
        self.resizable(width=True, height=True)

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
        for F in (StartPage,HomePage,SearchEntire,SearchListWindow):
            frame=F(container, self)
            frame.grid(row=0,column=0,sticky="nsew")
            self.frames[F]=frame

        #self.frames[SearchListWindow].tkraise()
        #self.frames[SearchEntire].tkraise()
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


client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print("CLIENT SIDE")

app=App()
#app.showPage(HomePage)
app.mainloop()