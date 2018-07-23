#!/usr/bin/env python

import sys
import socket
import select
import pytun # pip install python-pytun
import optparse

parser = optparse.OptionParser()
parser.add_option('-p', '--port', dest='port', help="The port to listen on. Default: 80", type="int", default=80)
parser.add_option('-a', '--address', dest='address', help="The local address for the tun device. Default: 1.1.1.1", default="1.1.1.1", type="string")
parser.add_option('-m', '--netmask', dest='netmask', help="The netmask for the tun device. Default: 255.255.255.0", default="255.255.255.0", type="string")
(options, args) = parser.parse_args()

while True:

	# Create the listening server
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind(('0.0.0.0', options.port))
	s.listen(1)
	conn, addr = s.accept()

	# Create the virtual tun device for the new connection
	tun = pytun.TunTapDevice()
	tun.addr = options.address
	tun.netmask = options.netmask
	tun.mtu = 1500
	tun.persist(False)
	tun.up()

	while True:
		try:
			(readable, writable, whocares) = select.select([tun, conn], [], [])

			for r in readable:
				if r == conn:
					tun.write(r.recv(tun.mtu))
				else:
					conn.send(r.read(tun.mtu))

		except pytun.Error as e:
			break

	tun.close()
