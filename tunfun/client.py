#!/usr/bin/env python

import sys
import socket
import select
import pytun # pip install python-pytun (not pytun)
import optparse

from Crypto import Random
from Crypto.Cipher import AES

BS = 16

def pad(s):
        return s + (BS - len(s) % BS) * chr(BS - len(s) % BS)

def unpad(s):
        return s[0:-ord(s[-1])]

def aes_encrypt(data, key):
        iv = Random.new().read(AES.block_size)
        return iv + AES.new(pad(key), AES.MODE_CBC, iv).encrypt(pad(data))

def aes_decrypt(data, key):
        iv = data[:16]
        return unpad(AES.new(pad(key), AES.MODE_CBC, iv).decrypt(data[16:]))

parser = optparse.OptionParser()
parser.add_option('-s', '--server', dest='server', help="The address of the server instance.", type="string")
parser.add_option('-p', '--port', dest='port', help="The port of the server instance. Default: 80", type="int", default=80)
parser.add_option('-a', '--address', dest='address', help="The local address for the tun device. Default: 1.1.1.2", default="1.1.1.2", type="string")
parser.add_option('-m', '--netmask', dest='netmask', help="The netmask for the tun device. Default: 255.255.255.0", default="255.255.255.0", type="string")
parser.add_option('-t', '--tap', dest='tap', help="Create a tap device instead", action="store_true", default=False)
parser.add_option('-k', '--key', dest='key', help="The AES key to use", type="string")
(options, args) = parser.parse_args()

if not options.server:
	print "Server required"
	sys.exit(0)

if options.tap:
	print "Not currently supported"
	sys.exit(0)

while True:
    
	# Connect to the server
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((options.server, options.port))

	# Create our virtual device
	if options.tap:
		tun = pytun.TunTapDevice(flags=pytun.IFF_TAP)
	else:
		tun = pytun.TunTapDevice()
		tun.addr = options.address
		tun.netmask = options.netmask

	tun.mtu = 1500
	tun.persist(False)
	tun.up()

	while True:
		(readable, writable, whocares) = select.select([tun, s], [], [])

		for r in readable:
			if r == s:
				data = r.recv(tun.mtu)

				if data:
					if options.key:
						data = aes_decrypt(data, options.key)
					tun.write(data)
			else:
				data = r.read(tun.mtu)

				if data:
					if options.key:
						data = aes_encrypt(data, options.key)
					s.send(data)

