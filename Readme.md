# File Sharing
A python file server implementation using socket programming and multi-threading

# Server
```bash
python3 Server.py
```
```
Server Help :
[~]>Commands and how to use them :

1)start
	it will start the server on the port wich is in config file and start listening for clients
2)terminate
	it will terminate the server and stop all threads and end the programm
3)add_file FILEADDRESS
	it will add a new file to sharing files (and it'll set a unique name for Similar files with different locations)
4)remove_file FILEADDRESS
	it will remove the file from sharing list
5)show_files
	it will list the sharing files
6)search FILENAME
	it will find the file from it's unique name and show the address of it
7)ban IPADDRESS
	it will ban connection or communication from that IPADDRESS (if the connection was set before the banning , it will not proccess the clients requests anymore)
8)unban IPADDRESS
	it will unban that IPADDRESS from banlist
9)cnt_client
	if will show you how many clients are connected to this server

10)help
	it will print this message
```

# client
```bash
python3 Client.py
```
```
Client help :
[~]>List of commands and how to use them:

1)connect IPADDRESS PORTNUMBER
	it will connect to the server with following information
2)terminate
	it will terminate the client and stop the programm
3)close
	it will terminate the connection but will keep the programm running (you can connect to server after this again
4)update
	it will recive the list of filenames(not addresses) from server
5)get FILENAME(NOT ADDRESS)
	it will download the file from server. you don't need to know the address of file , only it's name is needed
6)help
	it will print this message
  ```
