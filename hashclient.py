import socket 
import sys 
import argparse 
import json 

# Argparse, built into Python3, will help configure this app's relationship to the command line.

arguments = argparse.ArgumentParser(description='A data hashing network implementing the hash functions: sha1, sha256, sha512, md5.')
arguments.add_argument('-port', type=int, action='store', default='2345', help='Which port the client accesses. Default: 2345.')
arguments.add_argument('ip', action='store', default='127.0.0.1', help='Which network IP address to socket into.')
arguments.add_argument('algo', action='store', type=str, choices=['sha1', 'sha256', 'sha512', 'md5'], help='Which hashing algorithm to use.')
arguments.add_argument('files', action='store', nargs=argparse.REMAINDER, help='Which files the client wants to hash.')

#After the ArgumentParser object is configured, run parse_args to instantiate and bind it to the command line.
args = arguments.parse_args()

# Socket config and opening.
s = socket.socket()
host = socket.getfqdn(args.ip)
port = args.port
print(f'Connecting to {args.ip}:{port}...')
s.connect((host, port))

# All information sent over the socket will be encoded in binary for type variability. This is the hash algorithm the server will use.

arg_packet = json.dumps(args.algo)
# print(arg_packet)
s.send(arg_packet.encode())
files_packet = json.dumps(args.files)
s.send('\n'.encode())
# print(files_packet)
s.send(files_packet.encode())

# Loop through the files listed in the command line and read out their contents toward the server for hashing.

for idx, value in enumerate(args.files):
  with open(value, 'r') as x:
    while True:
      fax = x.read()
      if not fax:
        s.send('<ENDFILE>'.encode())
        break
      # print(fax)
      s.send(fax.encode())
  x.close()


# Here we write out the content sent back from the server over the socket into a file named readout.txt.


with open('readout.txt', 'w') as f:
  while True:
    data = s.recv(65536)
    if not data:
      break
    data = data.decode().split('<ENDHEX>')
    mod_data = data
    mod_data = mod_data[:-1]
    # print('trimming the list sent with hexes', mod_data)
    if len(mod_data) > 0:
      out = ''
      for idx, hex in enumerate(mod_data):
        a = hex
        b = '     '
        c = args.files[idx]
        out += str(a + b + c + '\n')
      f.write(out)
    # print('mod data', mod_data)
f.close()

with open('readout.txt', 'r') as fin:
  print(fin.read())

s.close()