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
    data = s.makefile()
    for a in data.readline():
      print(a)
      algo = a
    data.close()
    conn.close()
s.close()