from base64 import encode
from http import client
from lib2to3.pgen2 import driver
from pdb import Restart
import socket
from sqlite3 import Cursor
import string
import threading
import pyodbc
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

# import server




HOST = "127.0.0.1"
PORT = 65432
FORMAT = "utf8"

TOTALCONTACT = "TotalContacts"
SPECONTACT = "SpecificContact"
LOGIN = "login"
LOGOUT = "logout"
ANIMAGE = "animage"
ALLIMAGE = "alliamge"

END = "x"
ADMIN_NAME = "socket"
ADMIN_PASS = "admin"


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

Live_Account = [] # [address - username,...]


def run():
    try:
        
        print("SERVER SIDE")
        print("server: ", HOST, PORT)
        print("Waiting for client")
        while True:
            conn, addr = server.accept()

           
            clientThread = threading.Thread(target = handle_client_resquest,args=[conn, addr] )
            clientThread.daemon = True
            clientThread.start()
        
    except KeyboardInterrupt:
        print("error")

def connect_db(db_name):
    # driver = "ODBC Driver 17 for SQL Server"
    # server = 'HUUTRONG'
    # user = 'socket'
    # password = '123456'

    driver = "ODBC Driver 17 for SQL Server"
    server = 'MINHTRI\MINHTRI'
    user = 'lmtri'
    password = '1'
    
    cnxn = pyodbc.connect('driver={%s};server=%s;database=%s;uid=%s;pwd=%s' % ( driver, server, db_name, user, password ) )
    return cnxn.cursor()


def checkLiveAccount(username):
    for live_acc in Live_Account:
        addr, user = live_acc.split('-')
        if(username == user):
            return 0
    return 1

def removeLiveAccount(conn, addr):
    for row in Live_Account:
        addr_saved, user_saved = row.split('-')
        print(addr_saved, addr)
        if(addr_saved == str(addr)):
            Live_Account.remove(row)
            print(Live_Account)
            break

def checkLogin(username: string, password: string):
    cursor = connect_db('SocketAccount')
    cursor.execute("select acc.username from Account acc ")
    
    if checkLiveAccount(username) == 0:
        return 0
    for row in cursor:
        st = str(row)
        check = st.find(',')
        user = st[2:check-1]

        if (username == user):
            cursor.execute("select acc.pass from Account acc where acc.username = (?)", (user))
            st = str(cursor.fetchone())
            check = st.find(',')
            psw = st[2:check-1]

            if(psw ==password):
                return 1
    return 2

def ClientLogin(sck: socket, addr):
    
    user_login = sck.recv(1024).decode(FORMAT)
    print(user_login)
    sck.sendall(user_login.encode(FORMAT))

    pass_login = sck.recv(1024).decode(FORMAT)

    flag = checkLogin(user_login, pass_login)
    
    if(flag == 1):
        Live_Account.append(str(addr) +"-"+ str(user_login) )
        print(Live_Account)

    sck.sendall(str(flag).encode(FORMAT))

def getTotalList():
    lists = []
    cursor = connect_db('Contacts')
    cursor.execute("select * from  Member ")
    for row in cursor:
        st = str(row)
        lists.append(st)
    return lists

def sendTotalList(sck: socket):
    lists = getTotalList()
    for item in lists:
        print(item)
        sck.sendall(item.encode(FORMAT))
        # waiting for client response
        sck.recv(1024)
    
    msg = "end"
    sck.sendall(msg.encode(FORMAT))

def sendSpecificContact(conn: socket, addr):
    id = conn.recv(1024).decode(FORMAT)
    cursor = connect_db('Contacts')
    cursor.execute("select * from Member M where M.ID = (?)", (id))
    contact = str(cursor.fetchone())
    print(contact)
    conn.sendall(contact.encode(FORMAT))


def handle_client_resquest(conn:socket, addr):
    try:
        option = None
        while option != END:
            option = conn.recv(1024).decode(FORMAT)
            print(option)
            if option == TOTALCONTACT:
                conn.sendall(option.encode(FORMAT))
                sendTotalList(conn)
            elif option == SPECONTACT:
                conn.sendall(option.encode(FORMAT))
                sendSpecificContact(conn, addr)
            elif option == LOGIN:
                conn.sendall(option.encode(FORMAT))
                ClientLogin(conn,addr)
            elif option == LOGOUT:
                conn.sendall(option.encode(FORMAT))
                removeLiveAccount(conn, addr)
            elif option == ANIMAGE:
                conn.sendall(option.encode(FORMAT))
                DownloadImage(conn)
            elif option == ALLIMAGE:
                conn.sendall(option.encode(FORMAT))
                DownloadFullImage(conn)
        print("stop")
        removeLiveAccount(conn, addr)
    except ConnectionResetError:
        #print("Client end!")
        removeLiveAccount(conn, addr)

def DownloadImage(conn:socket, file_path):
    print(file_path)
    last_line = NONE
    with open(file_path, 'rb') as f:
        last_line = f.readlines()[-1]
        conn.sendall(last_line)
        conn.recv(2048)
    with open(file_path, 'rb') as file:
        print("starting")
        for data in file:
            print(data)
            conn.sendall(data)
            conn.recv(2048)
            # if data == last_line:
            #     conn.sendall("DONE".encode(FORMAT))
            #     print("DONE")
            # else:
            #     conn.sendall("UNF".encode(FORMAT))
            #     print("UNF")
    file.close()
    
def DownloadFullImage(conn: socket):
    sendTotalList(conn)
    file_path = ""
    while(file_path !="end"):
        file_path = conn.recv(1024).decode(FORMAT)
        print(file_path)
        DownloadImage(conn, file_path)

### ...........GUI..............###

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
        self.appController = appController
        client_and_port= Live_Account
        print(Live_Account)
        # client_and_port = server.Live_Account

        label_title=tk.Label(self, text="HOME PAGE",font="Arial,45")
        label_user=tk.Label(self,text="Client List")

        self.content = tk.Frame(self)
        self.listbox1=Listbox(self.content, width= 25)

        for x, y in enumerate(client_and_port):
            self.listbox1.insert(x+1,y)    
            print(self.listbox1)
       
    # def get_Port():
    #     entry1.delete(0,'end')
    #     cur_Client=listbox1.get(ANCHOR)
    #     entry1.insert(0,client_and_port[cur_Client])
        
    # pass 
        
        # button=tk.Button(self,text="Send",command=lambda:appController.Send(self,client))
        button_refresh=tk.Button(self,text="Refresh",command=self.Refresh)
        btn_logout=tk.Button(self,text="Log Out", command=lambda:[f() for f in [appController.showPage(StartPage), appController.resize(self,300,210)]])
        # button_Get_Port=Button(self,text="Get Port",command=get_Port)
        # entry1=Entry(self,width=20)
        

        self.label_notice1=tk.Label(self, text="")
        self.label_notice2=tk.Label(self, text="")
        self.label_notice3=tk.Label(self, text="")
        self.label_notice4=tk.Label(self, text="")
        self.label_notice5=tk.Label(self, text="")

        self.content.pack_configure()
        self.scroll = tk.Scrollbar(self.content)
        self.scroll.pack(side = RIGHT, fill= BOTH)
        self.listbox1.config(yscrollcommand=self.scroll.set)

        self.scroll.config(command=self.listbox1.yview)
        self.listbox1.pack()




        label_title.pack()
        self.label_notice1.pack(pady=5)
        self.listbox1.pack(anchor=CENTER)
        self.label_notice3.pack()
        # button_Get_Port.pack()
        self.label_notice4.pack()
        # entry1.pack()
        self.label_notice2.pack()
        # button.pack()
        button_refresh.pack()
        self.label_notice5.pack(pady=5)
        btn_logout.pack()
    
    # def restart(self):
    #     print("Restart")
    #     print(self.listbox1)
    #     self.refresh()
    #     self.appController.showPage(HomePage)
    # def refresh(self):
    #     print("Refresh")
    #     self.listbox1.delete(0, "end")
    #     # set focus to any widget except a Text widget so focus doesn't get stuck in a Text widget when page hides
    #     self.listbox1.focus_set()
    def Refresh(self): 
        self.listbox1.delete(0,len(Live_Account))
        for i in range(len(Live_Account)):
            self.listbox1.insert(i,Live_Account[i])

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
            
            check = -1
            if (user == ADMIN_NAME and pswd == ADMIN_PASS):
                check = 1
            elif user != ADMIN_NAME:
                check = 2
            else: check = 3

            # ____________________
            if(check == 1):
                self.showPage(HomePage)
            elif check == 2:
                curFrame.label_notice["text"]="Invalid username"
                return
            else:
                curFrame.label_notice["text"]="Invalid password"
                return

        
        except:
            print("Error: Server is not responding")

    def Send(self,curFrame, sck):
        option=LOGIN
        sck.sendall(option.encode(FORMAT))
        sck.recv(1024)

    

    def resize(self,curFrame,w,h):
        self.geometry(f"{w}x{h}")
        
# print("SERVER SIDE")
# print("server: ", HOST, PORT)
# print("Waiting for client")
# conn, addr = server.accept()
# print("Connection:", addr)
# DownloadFullImage(conn)
# DownloadImage(conn, "Avatar/SmallAvatar/lmtri.png")

# input()

 
sThread = threading.Thread(target=run)
sThread.daemon = True 
sThread.start()
print("Hello")


app=App()
#app.showPage(HomePage)
app.mainloop()