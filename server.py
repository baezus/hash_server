import socket 
import hashlib
import re 

port = 2345
s = socket.socket()
host = socket.gethostname()
s.bind((host, port))
s.listen(3)

print(f'Connecting to {host}:{port}.')

while True:
    conn, addr = s.accept() # Accept waiting clients.
    print(f'Got connection from {addr}.')

    #Receive the name of the hash algorithm to use.
    data = conn.recv(1024)
    print(data.decode())
    conn.send(data)

conn.close()
s.close()