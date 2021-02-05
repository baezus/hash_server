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

    # Receive meta data sent from the client.
    data = conn.recv(1024)
    working_data = data.decode()
    print('working data', working_data)
    file_names = re.findall(r'"([^"]*)"', working_data)
    algo = file_names.pop(0)
    print('algorithm', algo)
    print('file names', file_names)
    conn.send(data)

    # Loop as file content is sent in, hash, send back, and start over.

    file_content = conn.recv(1024)
    file_slices = file_content.decode().split('<ENDFILE>')
    remainder = file_slices.pop()
    print('file content', file_content.decode())
    print('file slices', file_slices)
    hex_buf = ''
    
    while file_slices:
      material = file_slices.pop(0)
      h = hashlib.new(algo)
      h.update(material.encode())
      result = h.hexdigest()
      hex_buf += result
      hex_buf += '<ENDHEX>' 
      print('hex buf', hex_buf)
    print('file hex', hex_buf)
    conn.send(hex_buf.encode())  
    conn.close()

s.close()