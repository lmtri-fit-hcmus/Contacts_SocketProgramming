from ast import For
from asyncio.windows_events import NULL
from ctypes import sizeof
from re import I
import socket 
import threading 
import pyodbc
import tkinter as tk

HOST = "172.20.24.148" 
SERVER_PORT = 65432 
FORMAT = "utf8"
LOGIN = "login"
SUCCESS = "SUCCESS"
FAILED = 'FAILED'

TOTALCONTACT = "TotalContacts"
SPECONTACT = "SpecificContact"

DemoListContacts = [['123','Le Minh Tri', '1111111', 'asdfsdf@gmail','123','234']]

#================================GUI===========================================



#===========================================================================

def SendList(conn,list):
    for i in list:
        conn.sendall(i.encode(FORMAT))
        conn.recv(1024)
    conn.sendall('x'.encode(FORMAT))
    
def SendTotalContacts(conn):
    for i in DemoListContacts:
        for j in i:
            conn.sendall(j.encode(FORMAT))
            conn.recv(1024)
    conn.sendall('x'.encode(FORMAT))

def SendSpecificContact(conn):
    ID = conn.recv(1024).decode(FORMAT)
    for i in DemoListContacts:
        if i[0] == ID:
            conn.sendall('found'.encode(FORMAT))
            SendList(conn,i)
            return
    conn.sendall('not found'.encode(FORMAT))

def handleClient(conn: socket, addr):
    
    print("conn:",conn.getsockname())
    
    msg = None
    while (msg != "x"):
        msg = conn.recv(1024).decode(FORMAT)
        print("client ",addr, "says", msg)

        if (msg == LOGIN):
            #response
            conn.sendall(msg.encode(FORMAT))
            #msg = serverLogin(conn)
            conn.sendall(msg.encode(FORMAT))
        elif(msg == TOTALCONTACT):
            conn.sendall(msg.encode(FORMAT))
            SendTotalContacts(conn)
        elif(msg == SPECONTACT):
            conn.sendall(msg.encode(FORMAT))
            SendSpecificContact(conn)

    
    
    print("client" , addr, "finished")
    print(conn.getsockname(), "closed")
    conn.close()

#-----------------------main----------------------------------------------------------------------------------------------------------

conx = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=MINHTRI\MINHTRI;DATABASE=SocketAccount;UID=lmtri;PWD=1')
cursor = conx.cursor()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

s.bind((HOST, SERVER_PORT))
s.listen()

print("SERVER SIDE")
print("server:", HOST, SERVER_PORT)
print("Waiting for Client")


nClient = 0
while (nClient < 3):
    try:
        conn, addr = s.accept()
        
        thr = threading.Thread(target=handleClient, args=(conn,addr))
        thr.daemon = False
        thr.start()

    except:
        print("Error")
    
    nClient += 1


print("End")

s.close();
conx.close()