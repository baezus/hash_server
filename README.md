# Data Hashing Network

## To Run:

In one terminal tab, run 'python3 server.py.' If desired, a -p tag can be added to specify a different server port.

In another tab, run 'python3 hashclient.py -p 2345 127.0.1.1 [[ sha1, sha256, sha512, or md5 (one choice) ]] [[ files_to_hash (n amount allowed) ]]

To run the hash client, the port is optional, but the arguments that follow are mandatory.

## Readout:

In the client terminal, the response should be a hash hexcode followed by the name of the file that hex code corresponds to.

![Image of Client Output]
(./screenshot_of_data.png)


