import threading
from threading import Thread
import json
import time
import socket
import os
class Server:
    Thread_pool=[]
    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    is_running = False
    def __init__(self):
        pass
    def start(self,sock):
        print("~Started server on port : ", sock)
        self.serv.bind(('0.0.0.0', sock))
        self.serv.listen(100)
        print("~Listening for incoming connections")
        self.is_running = True
        while(True):
            #Clearing the Thread_pool
            for T in self.Thread_pool:
                if(not T.is_alive()):
                    self.Thread_pool.remove(T)
            #check if we have reached maximum number of clients or not
            if(len(self.Thread_pool)<=99):
                conn, addr = self.serv.accept()
                if(addr[0] in load_config('config.json')['banned_addresses']):
                    conn.send("BANNED".encode('utf8'))
                    print("a banned user tried to connect but was not accepted")
                else:
                    conn.send("connected".encode('utf8'))
                    self.Thread_pool.append(Thread(target=self.client_handler,args=(conn,addr)))
                    #Listen for incoming connections and add them to thread pool
                    self.Thread_pool[-1].start()
                    print("Connection from " + str(addr) + " Established. handling it with a thread")
        self.serv.detach()
        self.is_running = False


    def client_handler(self,conn,addr):

        while(True):
            #try:
            if(self.is_running==False):
                return
            data = False
            try:
                data = conn.recv(4096)
            except:
                data = False
            if (not data):
                print("Client " + str(addr) + " Disconnected. it's thread is free now")
                return
            if(str(addr[0]) in load_config('config.json')['banned_addresses']):
                print("Recived message from a banned ip , ignoring it ...")
                continue
            msg=data.decode('utf8')
            if(msg == 'disconnect'):
                print("Client " + str(addr)+" Disconnected. it's thread is free now")
                #TODO : removing it's thread from the Thread_pool
                return
            if(msg=="update"):
                files_list = get_files_list(load_config('config.json')['files_list'])
                files_name = [m.split(',')[0] for m in files_list]
                files_addr = [m.split(',')[1] for m in files_list]
                print("sending update file")
                send_data = "\n".join(files_name).encode('utf8')
                if(len(files_list)==0):
                    conn.send("Nothing".encode('utf8'))
                else:
                    conn.send(send_data)

            if(msg.startswith('GET*')):
                filename = msg.split('*')[1]
                print("sending file to client")#beautifilyfy this shit
                filenames = get_files_list('files_list.txt')
                is_in_files = False
                file_addr=""
                for row in filenames:
                    if(row.split(",")[0]==filename):
                        is_in_files,file_addr = True , row.split(',')[1]
                if(is_in_files):
                    conn.send(str("valid "+str(os.path.getsize(file_addr))).encode('utf8'))
                    #check if it is valid or not here
                    self.send_file(conn,file_addr)
                else:
                    conn.send(("invalid "+"File_NOT_FOUND").encode('utf8'))
            print("Recived from client "+str(addr)+" : ",msg)
            #conn.send(msg.encode('utf8'))
            #except:
                #print("Error")
                #return
    def send_file(self,conn,filename):
        conn.send(open(filename,"rb").read())
        return
    #start server with this
    def start_manager(self,sock):
        while(True):
            conf = load_config('config.json')
            files_list = get_files_list(conf['files_list'])
            files_name = [m.split(',')[0] for m in files_list]
            files_addr = [m.split(',')[1] for m in files_list]

            C = input("Server> ").split(' ')
            cmd = C[0]
            if(len(C)>1):
                C = [cmd , " ".join(C[1:])] #because of space in input (for exmple : add_file C:\....\new folder\file.pdf (to ignore the second space))
            if(cmd == 'start'):
                if(not self.is_running):
                    self.Thread_pool.append(Thread(target=self.start , args=([sock])))
                    self.Thread_pool[-1].start()
                else:
                    print("The server is already running.you must terminate it before starting again")
            elif(cmd == 'terminate'):
                self.is_running=False
                self.serv.close()
                break;
            elif(cmd == 'add_file'):
                if(C[1] in files_addr):
                    print("File already exists")
                    continue
                if(os.path.exists(C[1])):
                    files_list.append(get_file_name_from_address(files_name,C[1])+","+C[1])
                    save_files_list(files_list, conf)
                    print("File added to list successfully")
                else:
                    print("The file does not exist")
            elif (cmd == 'remove_file'):
                removed = False
                for fil in files_list:
                    if(fil.split(",")[1]==C[1]):
                        files_list.remove(fil)
                        removed = True
                        break
                if(removed):
                    save_files_list(files_list,conf)
                    print("File removed from the list successfully")
                else:
                    print("This file does not exist in the list")
            elif(cmd == 'ban'):
                if(not C[1] in conf['banned_addresses']):
                    conf['banned_addresses'].append(C[1])
                    save_config("config.json" , conf)
                    print("Address added to blocked list")
                else:
                    print("The address is already banned")
            elif(cmd == 'unban'):
                if(C[1] in conf['banned_addresses']):
                    conf['banned_addresses'].remove(C[1])
                    save_config("config.json" , conf)
                    print("The address is now free")
                else:
                    print("The address is not in ban_list")
            elif(cmd == 'ban_list'):
                print("Banned users : \n\n" + "\n".join(conf['banned_addresses']))
            elif(cmd == 'show_files'):
                if(len(files_list)!=0):
                    print("~>List of files :\n::::::" + "\n::::::".join(files_list))
                else:
                    print("There is no file in the list")
            elif(cmd == 'search'):
                if(C[1] in files_name):
                    print("::::::"+C[1] + " , "+files_addr[files_name.index(C[1])])
            elif(cmd == 'help'):
                print(open("help.txt",'r').read())
                #Shit to do here
            elif(cmd == 'clear_files'):
                save_files_list([], conf)
                print("File list cleared Successfully")
            elif(cmd == 'cnt_client'):
                if(self.is_running):
                    mtn = "Number of clients connected : " + str(len(self.Thread_pool)-1)+"\n"
                    print(mtn)
                else:
                    print("Server is not running!")
def get_files_list(filename):
    return [row for row in open(filename,'r').read().split('\n') if row!='']
def save_files_list(filenames, conf):
    with open(conf['files_list'] , "w") as file:
        mt = ""
        for i in range(len(filenames)):
            mt+= filenames[i]+"\n"
        file.write(mt)

def get_file_name_from_address(filenames , file_address):
    first_attempt = file_address.split('\\')[-1]
    if(not first_attempt in filenames):
        return first_attempt
    else:
        mm = first_attempt.split("_")
        if(len(mm)==1):
            name = "".join(file_address.split('.')[:-1])
            format = file_address.split('.')[-1]
            return get_file_name_from_address(filenames, name+"_1."+format)
        else:
            name = "".join(file_address.split('.')[:-1])
            format = file_address.split('.')[-1]
            newfilename = name.split("_")[0] +"_"+ str(int(name.split("_")[1])+1)+"."+format
            return get_file_name_from_address(filenames , newfilename)

def load_config(filename):
    with open(filename,'r') as file:
        return json.load(file)
def save_config(filename , config):
    with open(filename, "w") as file:
        file.write(json.dumps(config))

config = load_config('config.json')
S = Server()
S.start_manager(config['port_number'])
del(S)




