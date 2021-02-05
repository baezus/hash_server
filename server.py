import socket 
import hashlib
import re 

port = 2345
s = socket.socket()
host = socket.gethostname()
s.bind((host, port))
s.listen(3)

print(f'Connecting to {host}:{port}.')