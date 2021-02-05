import socket 
import hashlib
import re
import argparse 

# Setting up the one server argument.
arguments = argparse.ArgumentParser(description='A data hashing network implementing the hash functions: sha1, sha256, sha512, md5.')
arguments.add_argument('-port', type=int, action='store', default='2345', help='Which port the client accesses. Default: 2345.')
args = arguments.parse_args()

# Basic configuration for the socket
s = socket.socket()
host = socket.gethostname()
s.bind((host, args.port))
s.listen(10)

print(f'Connecting to {host}:{args.port}.')

while True:
    conn, addr = s.accept() # Accept waiting clients.
    print(f'Got connection from {addr}.')

    # Receive meta data sent from the client.
    data = conn.recv(65536)
    working_data = data.decode()
    file_names = re.findall(r'"([^"]*)"', working_data)
    algo = file_names.pop(0)
    conn.send(data)

    # Loop as file content is sent in, hash, send back, and start over.
    file_content = conn.recv(65536)
    file_slices = file_content.decode().split('<ENDFILE>')
    if len(file_slices) >= len(file_names): # This removes the empty [].
      remainder = file_slices.pop()

    # This is the buffer our hexdigested hash values will go into.
    hex_buf = ''
    while file_slices:
      material = file_slices.pop(0)
      h = hashlib.new(algo) # Instances on loop the client commanded hasher.
      h.update(material.encode())
      result = h.hexdigest()
      hex_buf += result
      hex_buf += '<ENDHEX>' # Protocol to allow the client to split data.
    print('File(s) Hex: ', hex_buf)
    conn.send(hex_buf.encode())  
    conn.close()

s.close()