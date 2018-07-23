#!/usr/bin/env python

import sys
import socket
import select
import pytun # pip install python-pytun (not pytun)
import optparse

parser = optparse.OptionParser()
parser.add_option('-s', '--server', dest='server', help="The address of the server instance.", type="string")
parser.add_option('-p', '--port', dest='port', help="The port of the server instance. Default: 80", type="int", default=80)
parser.add_option('-a', '--address', dest='address', help="The local address for the tun device. Default: 1.1.1.2", default="1.1.1.2", type="string")
parser.add_option('-m', '--netmask', dest='netmask', help="The netmask for the tun device. Default: 255.255.255.0", default="255.255.255.0", type="string")
(options, args) = parser.parse_args()

if not options.server:
	print "Server required"
	sys.exit(0)

while True:
    
    # Connect to the server
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((options.server, options.port))

    # Create our virtual device
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
				tun.write(r.recv(tun.mtu))
			else:
				s.send(r.read(tun.mtu))
