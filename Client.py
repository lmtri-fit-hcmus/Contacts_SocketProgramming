from pydoc import cli
import socket

HOST = "127.0.0.1"
SERVER_PORT = 65432
FORMAT = "utf8"

TOTALCONTACT = "TotalContacts"
SPECONTACT = "SpecificContact"
LOGIN = "login"

#Đầu ra là list 6 thuộc tính của 1 member 
def ReceiveList(client):
    option = None
    list = []
    while option != 'end':
        for i in range(0,6):
            list.append(client.recv(1024).decode(FORMAT))
            client.sendall('ok'.encode(FORMAT))
        option = client.recv(1024).decode(FORMAT)
    return list

#Nhận về danh sách tất cả thành viên trong danh bạ (list là mảng 2 chiều)
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

#đầu ra là list chứa thuộc tính của 1 member có ID cụ thể,
#nếu không tìm thấy, in ra not found
def GetSpecificContact(client, ID):
    client.recv(1024)
    client.sendall(ID.encode(FORMAT))
    msg = client.recv(1024).decode(FORMAT)
    return msg
#------------------main-----------------------

# client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# print("CLIENT SIDE")


# try:
#     client.connect( (HOST, SERVER_PORT) )
#     print("client address:",client.getsockname())

    
#     user = input("User:")
#     client.sendall(user.encode(FORMAT))
#     client.recv(1024)


#     passw = input("Pass:")
#     client.sendall(passw.encode(FORMAT))

#     accepted = int(client.recv(1024).decode(FORMAT))
#     print(accepted)
#     if (accepted == 0): 
#         print("Account has been login by another")
#     elif accepted == 1:
#         print("Successfully login")
#         msg = None
#         while (msg != "x"):
#             msg = input("talk: ")
#             client.sendall(msg.encode(FORMAT))

#             # functions called by client 
#             # if (msg == LOGIN): 
#             #     # wait response
#             #     client.recv(1024)
#             #     clientLogin(client)
#             if(msg == TOTALCONTACT):
#                 lists = TotalContact(client)
#                 print(lists)
#             elif(msg == SPECONTACT):
#                 client.recv(1024)
#                 ID = input("Input ID to check contact: ")
#                 lists = GetSpecificContact(client,ID)
#                 print(lists)
#     elif accepted == 2:
#         print("Wrong username or password")
#     input()
# except:
#     print("Error")


# client.close()