from pydoc import cli
import socket

HOST = "172.20.24.148"
SERVER_PORT = 65432
FORMAT = "utf8"

TOTALCONTACT = "TotalContacts"
SPECONTACT = "SpecificContact"

#Đầu ra là list 6 thuộc tính của 1 member 
def ReceiveList(client):
    option = None
    list = []
    while option != 'x':
        for i in range(0,6):
            list.append(client.recv(1024).decode(FORMAT))
            client.sendall('ok'.encode(FORMAT))
        option = client.recv(1024).decode(FORMAT)

    return list

#Nhận về danh sách tất cả thành viên trong danh bạ (list là mảng 2 chiều)
def TotalContact(client):
    list=[]
    option = None
    count = 0
    while option != 'x':
        list.append([])
        for i in range(0,6):
            list[count].append(client.recv(1024).decode(FORMAT))
            client.sendall(list[count][i].encode(FORMAT))
        count += 1
        option = client.recv(1024).decode(FORMAT)
    return list

#đầu ra là list chứa thuộc tính của 1 member có ID cụ thể,
#nếu không tìm thấy, in ra not found
def SendSpecificContact(client, ID):
    client.sendall(ID.encode(FORMAT))
    msg = client.recv(1024).decode(FORMAT)
    if(msg == 'found'):
        list = ReceiveList(client)
        return list
    else:
        print(msg)
#------------------main-----------------------

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("CLIENT SIDE")


try:
    client.connect( (HOST, SERVER_PORT) )
    print("client address:",client.getsockname())


    msg = None
    while (msg != "x"):
        msg = input("talk: ")
        client.sendall(msg.encode(FORMAT))

        # functions called by client 
        # if (msg == LOGIN): 
        #     # wait response
        #     client.recv(1024)
        #     clientLogin(client)
        if(msg == TOTALCONTACT):
            client.recv(1024)
            list = TotalContact(client)
            print(list)
        elif(msg == SPECONTACT):
            client.recv(1024)
            ID = input("Input ID to check contact: ")
            list = SendSpecificContact(client,ID)
            print(list)
    
except:
    print("Error")


client.close()