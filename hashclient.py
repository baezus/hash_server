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

# All information sent over the socket will be encoded in binary for type variability.

arg_packet = (args.algo).encode()
print(arg_packet)
s.send(arg_packet)


s.close()