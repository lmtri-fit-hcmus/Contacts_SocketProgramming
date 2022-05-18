from base64 import encode
from http import client
from lib2to3.pgen2 import driver
import socket
from sqlite3 import Cursor
import string
import threading
import pyodbc


HOST = "127.0.0.1"
PORT = 65535
FORMAT = "utf8"

TOTALCONTACT = "TotalContacts"
SPECONTACT = "SpecificContact"
LOGIN = "login"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print("SERVER SIDE")
print("server: ", HOST, PORT)
print("Waiting for client")

Live_Account = [] # [address - username,...]



# def chat(conn: socket, addr):
#     Login(conn, addr)
#     print("Connection:", conn.getsockname())
#     msg = None
#     while(msg!="x"):
#         msg = conn.recv(1024).decode(FORMAT)
#         #Response
#         conn.sendall(msg.encode(FORMAT))
#         print("Client ", addr, "says", msg)
#     print("client ", addr, "finished")
#     print(conn.getsockname(), "closed")
#     conn.close()



def run():
    try:
        while True:
            conn, addr = server.accept()
            print("Connection:", conn.getsockname(), addr)
            clientThread = threading.Thread(target = handle_client_resquest,args=[conn, addr] )
            clientThread.daemon = False
            clientThread.start()
    except KeyboardInterrupt:
        print("error")

def connect_db():
    driver = "ODBC Driver 17 for SQL Server"
    server = 'HUUTRONG'
    db = 'Contacts'
    user = 'socket'
    password = '123456'
    cnxn = pyodbc.connect('driver={%s};server=%s;database=%s;uid=%s;pwd=%s' % ( driver, server, db, user, password ) )
    return cnxn.cursor()


def checkLiveAccount(username):
    for live_acc in Live_Account:
        addr, user = live_acc.split('-')
        if(username == user):
            return 0
    return 1


def checkLogin(username: string, password: string):
    cursor = connect_db()
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

def Login(sck: socket, addr):
    
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
    cursor = connect_db()
    cursor.execute("select * from  Member ")
    for row in cursor:
        st = str(row)
        lists.append(st)
    return lists

def sendTotalList(sck: socket, addr):
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
    cursor = connect_db()
    cursor.execute("select * from Member M where M.ID = (?)", (id))
    contact = str(cursor.fetchone())
    conn.sendall(contact.encode(FORMAT))


def handle_client_resquest(conn:socket, addr):
    Login(conn,addr)
    while True:
        option = conn.recv(1024).decode(FORMAT)
        print(option)
        if option == TOTALCONTACT:
            sendTotalList(conn,addr)

run()


    
# id = "20120506"
# cursor = connect_db()
# cursor.execute("select * from Member M where M.ID = (?)", (id))
# print(str(cursor.fetchone()))





