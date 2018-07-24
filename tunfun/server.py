#!/usr/bin/env python

import sys
import socket
import select
import pytun # pip install python-pytun
import pybrctl
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
parser.add_option('-p', '--port', dest='port', help="The port to listen on. Default: 80", type="int", default=80)
parser.add_option('-a', '--address', dest='address', help="The local address for the tun device. Default: 1.1.1.1", default="1.1.1.1", type="string")
parser.add_option('-m', '--netmask', dest='netmask', help="The netmask for the tun device. Default: 255.255.255.0", default="255.255.255.0", type="string")
parser.add_option('-t', '--tap', dest='tap', help="Create a tap device instead", action="store_true", default=False)
parser.add_option('-i', '--interface', dest='interface', help="The interface to bind the tap to", type="string", default="eth0")
parser.add_option('-k', '--key', dest='key', help="The AES key to use", type="string")

(options, args) = parser.parse_args()

# We need to create a bridge for tap devices
if options.tap:
	print "Not currently supported"
	sys.exit(0)
	brctl = pybrctl.BridgeController()
	bridge = brctl.addbr('tunfun0')

# Create the listening server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('0.0.0.0', options.port))

while True:
	s.listen(1)
	conn, addr = s.accept()

	# TUN and TAP devices have difference configuration needs
	if options.tap:
		tun = pytun.TunTapDevice(flags=pytun.IFF_TAP)
		bridge.addif(options.interface)
		bridge.addif(tun.name)
	else:
		tun = pytun.TunTapDevice()
		tun.addr = options.address
		tun.netmask = options.netmask

	tun.persist(False)
	tun.mtu = 1500
	tun.up()

	while True:
		try:
			(readable, writable, whocares) = select.select([tun, conn], [], [])

			for r in readable:
				if r == conn:
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
						conn.send(data)

		except pytun.Error as e:
			break

	# Remove the device from the bridge
	if options.tap:
		bridge.delif(options.interface)
		bridge.delif(tun.name)

	# Remove the old tun device
	tun.close()
	conn.close()
