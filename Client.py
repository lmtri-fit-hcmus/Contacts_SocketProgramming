from pydoc import cli
import socket

HOST = "127.0.0.1"
SERVER_PORT = 65432
FORMAT = "utf8"

TOTALCONTACT = "TotalContacts"
SPECONTACT = "SpecificContact"
LOGIN = "login"
ANIMAGE = "animage"
ALLIMAGE = "alliamge"
downloadDir = "Download_Image/"


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


def getImageFile(client, file_path):
    client.sendall(file_path.encode(FORMAT))
    # print("Send path")
    print(downloadDir+file_path.split("/")[-1])
    last_line = client.recv(2048)
    client.sendall(last_line)
    print(downloadDir+file_path.split("/")[-1])
    with open(downloadDir+file_path.split("/")[-1], "wb") as file:
        while True:
            data = client.recv(2048)
                # client.sendall(data)
                # flag = int(client.recv(1024).decode(FORMAT))
            client.sendall(data)
            # state = client.recv(1024).decode(FORMAT)
            if data ==last_line:
                break
            file.write(data)
        print("Break")
        file.close()
    print("Done")
    # client.recv(1024)
    

def getFullImageFile(client):
    # option = TOTALCONTACT
    client.sendall(ALLIMAGE.encode(FORMAT))
    client.recv(1024)
    lists = TotalContact(client)
    print(lists)
    for item in lists:
        item = item[1:len(item)-1]
        item = item.split(', ')
        print(item)
        image_path = (item[5])
        # [1:len(image_path)-1]
        image_path = image_path[1:len(image_path) -1]
        print(image_path)
        getImageFile(client, image_path)
    client.sendall("end".encode(FORMAT))