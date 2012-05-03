#!/usr/bin/python
# vim: expandtab ts=4 sw=4 sts=4 fileencoding=utf-8:

# server

# this is a beta version of the dynamips image management server.
# An ios image must be of the form 'router_type'.image (e.g. c7200.image)
# It creates a dynamips instance and connect to its control port.
# it then create router instances and define their control port and UDP stream ports.
# The ios images must be in the working directory.

import socket
import sys
import select
from struct import *
import subprocess
import os
import time
import signal

def handler(signum, frame):
	globalState._server._socket.close()
	print "\rSIGINT caught. Exciting gracefully"
	sys.exit(0)

signal.signal(signal.SIGINT, handler)

def getInfos(client):
	print 'getInfos'

def sendData(client):
	clientOut = globalState._server._clients[globalState._negociator._socket]
	print client.getCurrentPayLoad()
	clientOut.feedWrite(client.getCurrentPayLoad())
	print "client write buffer : ", clientOut._writeQueue
	globalState._server._outgoing.append(clientOut._socket)
	print globalState._server._outgoing


#global vars
funcsHash = { 1: getInfos, 2: sendData }
globalState = None
#-----------

class GlobalState:
	_port = None
	_dynamipsPath = None
	_workingDirectory = None
	_instanceDesc = None
	_server = None
	_negociator = None

	def __init__(self, argv):
		self._port = argv[1]
		self._dynamipsPath = argv[2]
		self._workingDirectory = argv[3]

		i = 4
		self._instanceDesc = []

		while (i + 2) <= len(argv):
			self._instanceDesc.append([argv[i], argv[i + 1], int(argv[i + 1]) + 1])
			i += 2

class DynamipsNegociator:
	_port = None
	_process = None
	_nullFd = None
	_socket = None

	def __init__(self, port):
		self._port = port
		self._nullFd = os.open(os.devnull, os.O_WRONLY)
		self._process = subprocess.Popen([globalState._dynamipsPath, "-H",  str(self._port)], stdout = self._nullFd)

		# create connection to Dynamips Hypervisor console
		print "Trying to create socket on port", self._port, "for process' pid", self._process.pid

		while self._socket == None:
			for res in socket.getaddrinfo("127.0.0.1", self._port, socket.AF_UNSPEC, socket.SOCK_STREAM):
				af, socktype, proto, canonname, sa = res

				try:
					self._socket = socket.socket(af, socktype, proto)
				except socket.error, msg:
					self._socket = None
					continue

				try:
					self._socket.connect(sa)
				except socket.error, msg:
					self._socket.close()
					self._socket = None
					continue

				break

		if self._socket is None:
			print 'could not open socket'
			sys.exit(1)
		else:
			print 'connection to console successfully created'

class Connection:
	TCP, UDP = range(2)

	def __init__(self, socket, type = TCP):
		self._queue = []
		self._writeQueue = []
		self._write = False
		self._socket = socket

	def feed(self, data):
		print "feeding with", data

		if len(data) == 0:
			return

		if len(self._queue) > 0:
			if len(self._queue[len(self._queue) - 1][0]) != self._queue[len(self._queue) - 1][1]:
				self._queue[len(self._queue) - 1][0] += data

			if self._queue[len(self._queue) - 1][1] == -1:
				self._queue[len(self._queue) - 1] = [self._queue[len(self._queue) - 1][0][calcsize('i'):], unpack('!i', self._queue[len(self._queue) - 1][0][:calcsize('i')])[0]]

		else:
			if len(data) > calcsize('i'):
				self._queue.append([data[calcsize('i'):], unpack('!i', data[:calcsize('i')])[0]])
			else:
				self._queue.append([data, -1])

		print self._queue

		if len(self._queue[len(self._queue) - 1][0]) == self._queue[len(self._queue) - 1][1]:
			#print 'Able to write data : ' + self._queue.pop()[0]
			self._write = True

	def feedWrite(self, data):
		self._writeQueue.append([data])

	def getWriteData(self):
		if (len(self._writeQueue) > 0):
			return "".join(self._writeQueue[0]) + "\r\n"
		return ""

	def delWriteData(self, length):
		if length > 0:
			if len(self._writeQueue) > 0:
				if length >= len(self._writeQueue[0]):
					self._writeQueue.pop(0)
				else:
					self._writeQueue[0] = self._writeQueue[length:]

	def ready(self):
		return self._write

	def getCurrentCMD(self):
		return int(unpack('!c', self._queue[len(self._queue) - 1][0][:calcsize('c')])[0])

	def getCurrentPayLoad(self):
		return self._queue[len(self._queue) - 1][0][calcsize('c'):]

	def pop(self):
		del self._queue[0]

class Server:
	_socket = None
	_lineFeed = None

	_incoming = []
	_outgoing = []

	_clients = {}

	_instancePool = None
	_funcsHash = None

	def __init__(self, funcsHash, port, host=None, linefeed=None):
		self._socket = None
		self._lineFeed = linefeed

		self._funcsHash = funcsHash

		for res in socket.getaddrinfo(host, port, socket.AF_UNSPEC, socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
			af, socktype, proto, canonname, sa = res

			try:
				self._socket = socket.socket(af, socktype, proto)
				self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			except socket.error, msg:
				self._socket = None
				continue

			try:
				self._socket.bind(sa)
				self._socket.listen(5)
			except socket.error, msg:
				self._socket.close()
				self._socket = None
				continue

			break

		if self._socket is None:
			print 'could not open socket'
			sys.exit(1)
		else:
			print 'Server ready'
			self._incoming.append(self._socket)

			self._incoming.append(globalState._negociator._socket)
			self._outgoing.append(globalState._negociator._socket)
			self._clients[globalState._negociator._socket] = Connection(globalState._negociator._socket)

	def run(self):
		while self._incoming:
			(readable, writeable, exceptionable) = select.select(self._incoming, self._outgoing, self._incoming)

			# reading
			for s in readable:
				#print s
				if s is self._socket:
					(conn, addr) = self._socket.accept()
					conn.setblocking(0)
					self._incoming.append(conn)
					#self._outgoing.append(conn)

					self._clients[conn] = Connection(conn)

					print 'successfully registered new connection'
				elif s is globalState._negociator._socket:
					print "Dynamips hypervisor read", s.recv(1024).rstrip(self._lineFeed)
					if len(self._clients[s]._writeQueue) > 0:
						self._outgoing.append(s)
				else:
					data = s.recv(1024)

					if data:
						self._clients[s].feed(data.rstrip(self._lineFeed))

						if self._clients[s].ready():
							if self._funcsHash[self._clients[s].getCurrentCMD()] != None:
								self._funcsHash[self._clients[s].getCurrentCMD()](self._clients[s])
								self._clients[s].pop()
					else:
						self._incoming.remove(s)
						del self._clients[s]

						s.close()
						print 'client disconnected'

			for s in writeable:
				#print s
				client = self._clients[s]

				if len(client.getWriteData()) > 0:
					#print "Sending :", client.getWriteData()
					length = s.send(client.getWriteData())
					client.delWriteData(length)
					#print "".join(client.getWriteData())

					#if len(client._writeQueue) == 0:
					self._outgoing.remove(s)

# do the server/instances setup, create classes and create a class to negociate the creation

if __name__ == '__main__':
	if (len(sys.argv) < 6):
		print "Usage : port dynamips_binary working_directory [image port]*"
		sys.exit(1)

	globalState = GlobalState(sys.argv)

	negociator = DynamipsNegociator(7200)
	globalState._negociator = negociator

	server = Server(funcsHash, globalState._port, None, '\r\n')
	globalState._server = server

	client = globalState._server._clients[globalState._negociator._socket]

	client.feedWrite("hypervisor working_dir " + sys.argv[3])
	client.feedWrite("vm create R" + str(sys.argv[5]) + " 0 c7200")
	client.feedWrite("vm set_con_tcp_port R" + str(sys.argv[5]) + " " + str(sys.argv[3]))
	client.feedWrite("vm set_ios R" + str(sys.argv[5]) + " " + sys.argv[3] + "/" + sys.argv[4] + ".image")
	client.feedWrite("c7200 set_npe R" + sys.argv[5] + " npe-400")
	client.feedWrite("vm slot_add_binding R" + sys.argv[5] + " 1 0 PA-2FE-TX")
	client.feedWrite("nio create_udp nio_udp0 " + str(int(sys.argv[5]) + 1) + " 127.0.0.1 " + str(int(sys.argv[5]) + 2))
	client.feedWrite("vm slot_add_nio_binding R" + sys.argv[5] + " 1 0 nio_udp0")
	client.feedWrite("vm start R" + sys.argv[5])
	print client._writeQueue

	server.run()