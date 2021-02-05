import socket 
import hashlib
import re
import argparse 

# Setting up the one server argument.
arguments = argparse.ArgumentParser(description='A data hashing network implementing the hash functions: sha1, sha256, sha512, md5.')
arguments.add_argument('-port', type=int, action='store', default='2345', help='Which port the client accesses. Default: 2345.')
args = arguments.parse_args()

s = socket.socket()
host = socket.gethostname()
s.bind((host, args.port))
s.listen(3)

print(f'Connecting to {host}:{args.port}.')

while True:
    conn, addr = s.accept() # Accept waiting clients.
    print(f'Got connection from {addr}.')

    #Receive the name of the hash algorithm to use.
    data = conn.recv(1024)
    print(data.decode())
    conn.send(data)
    conn.close()

s.close()