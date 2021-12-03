import socket
import os
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while(True):
    CMDS = input("Client>").split(' ')
    cmd = CMDS[0]
    if(cmd == 'connect'):
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((CMDS[1], int(CMDS[2])))
            recived = client.recv(1024).decode('utf8')
            if(recived == "connected"):
                print("Connected to server")
            else:
                print("Can not connect to server / you are banned")
        except:
            print("Error in connecting to server , maybe it does not exist or the portnumber is wrong")
    elif(cmd == 'terminate'):
        client.close()
        print("Shuting down the programm")
        break
    elif(cmd  == 'close'):
        client.close()
        print("disconnected from server")
    elif(cmd == 'update'):
        client.send("update".encode('utf8'))
        from_server = client.recv(8192)
        if(from_server.decode('utf8') == 'Nothing'):
            print("No files are available to download")
        else:
            print(from_server.decode('utf8'))
    elif(cmd == 'get'):
        file_to_get = CMDS[1]
        client.send(("GET*"+file_to_get).encode('utf8'))
        from_sever = client.recv(8192).decode('utf8')
        retarg = from_sever.split(' ')
        if(retarg[0]=='valid' and len(retarg)==2):
            filesize = retarg[1]
            print("Getting ("+str(filesize)+")Bytes as "+str(CMDS[1]))
            file_in_bytes = client.recv(int(filesize))
            with open(CMDS[1].split('\\')[-1],'wb') as file:
                file.write(file_in_bytes)
            print("Recived file successfully")
        else:
            print("Sorry you can not get the file from the sever\nErr:"+retarg[1])
    elif(cmd == 'ls'):
        print("List of files : \n")
        print("\n".join(os.listdir()))
    elif(cmd == 'help'):
        print(open("help.txt",'r').read())
    else:
        print("Command not found")
    #client.send(txttosend.encode('utf8'))
    #from_server = client.recv(4096)
    #print (from_server.decode('utf8'))

client.close()