"""
pemu_lib.py
Copyright (C) 2007  Pavel Skovajsa

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""

from socket import socket, timeout, AF_INET, SOCK_STREAM
from dynamips_lib import NIO_udp, NOSEND, send, debug, DynamipsError, DynamipsErrorHandled, validate_connect, Bridge, DynamipsVerError
import random

(MAJOR, MINOR, SUB, RCVER) = (0,2,1,.1)
INTVER = MAJOR * 10000 + MINOR * 100 + SUB + RCVER
STRVER = "0.2.1-RC1"

class UDPConnection:
	def __init__(self, sport, daddr, dport):
		self.sport = sport
		self.daddr = daddr
		self.dport = dport


class Pemu (object):

	def __init__(self, name):
		self.port = 10525
		self.host = name

		#connect to PEMU Wrapper
		self.s = socket(AF_INET, SOCK_STREAM)
		self.s.setblocking(0)
		self.s.settimeout(300)
		self.type = 'pemuwrapper'
		if not NOSEND:
			try:
				self.s.connect((self.host,self.port))
			except:
				raise DynamipsError, "Could not connect to pemuwrapper at %s:%i" % (self.host, self.port) 
		#version checking
		version = send(self, 'pemuwrapper version')[0][4:]
		try:
			(major, minor, sub) = version.split('-')[0].split('.')
			release_candidate = version.split('-')[1]
			if release_candidate[:2] == 'RC':
				rcver = float('.' + release_candidate[2:])
			else:
				rcver = .999
			intver = int(major) * 10000 + int(minor) * 100 + int(sub) + rcver
		except:
			print 'Warning: problem determing pemuwrapper server version on host: %s. Skipping version check' % host
			intver = 999999
			
		if intver < INTVER:
			raise DynamipsVerError, 'This version of Dynagen requires at least version %s of pemuwrapper. \n Server %s is runnning version %s. \n Get the latest version from http://gdynagen.sourceforge.net/pemuwrapper/' % (STRVER, self.host, version)
		self.__version = version
		    
		#all other needed variables
		self.name = name
		self.devices = []
		self.baseconsole = 4000
		self.udp = 30000
		self.__workingdir = None


	def close(self):
		""" Close the connection to the Pemuwrapper (but leave it running)
		"""
		self.s.close()

	def reset(self):
		""" Reset the Pemuwrapper (but leave it running)
		"""
		send(self, 'pemuwrapper reset')


	def __setworkingdir(self, directory):
		""" Set the working directory for this network
		directory: (string) the directory
		"""
		if type(directory) not in [str, unicode]:
			raise DynamipsError, 'invalid directory'
		# send to pemuwrapper encased in quotes to protect spaces
		send(self, 'pemuwrapper working_dir %s' % '"' + directory + '"')
		self.__workingdir = directory

	def __getworkingdir(self):
		""" Returns working directory
		"""
		return self.__workingdir

	workingdir = property(__getworkingdir, __setworkingdir, doc = 'The working directory')


class FW (object):
	__instance_count = 0

	def __init__(self,pemu, name):
		self.p = pemu
		#create a twin variable to self.p but with name self.dynamips to keep things working elsewhere
		self.dynamips = pemu

		self.model_string = '525'

		self.__instance = FW.__instance_count
		FW.__instance_count += 1
		if name == None:
			self.name = 'fw' + str(self.__instance)
		else:
			self.name = name

		self.isrouter = 1 
		self.nios = {}
		for i in range(6):
			self.nios[i] = None
			
		self.__image = None

		self.default_serial = '0x12345678'
		self.__serial = self.default_serial

		self.default_key = '0x00000000,0x00000000,0x00000000,0x00000000'
		self.__key = self.default_key

		self.__console = None

		self.default_ram = 128
		self.__ram = self.default_ram

		self.state = 'stopped'
		self.first_mac_number = random.choice('abcdef123456789')
		self.second_mac_number = random.choice('abcdef123456789')
		
		self.idlepc = '0'
		self.idlemax = 0
		self.idlesleep = 0
		self.nvram = 0
		self.disk0 = 16
		self.disk1 = 0
		self.ghost_status = 0
		send(self.p   , 'pemu create %s' % (self.name))
		self.p.devices.append(self)
		#set the console to PEMU baseconsole 
		self.console = self.p.baseconsole
		self.p.baseconsole += 1

	def start (self):
		"""starts the fw instance in pemu"""
		if self.state == 'running':
			raise DynamipsError, 'firewall "%s" is already running' % self.name

		r = send(self.p   , 'pemu start %s' % (self.name))
		self.state = 'running'
		return r    

	def stop (self):
		"""stops the fw instance in pemu"""
		if self.state == 'stopped':
			raise DynamipsError, 'firewall "%s" is already stopped' % self.name
		r = send(self.p   , 'pemu stop %s' % (self.name))
		self.state = 'stopped'
		return r

	def suspend (self):
		"""suspends the fw instance in pemu"""
		return self.name + ' does not support suspending'

	def resume (self):
		"""resumes the fw instance in pemu"""
		return self.name + ' does not support resuming'

	def __setconsole(self, console):
		""" Set console port
		console: (int) TCP port of console
		"""
		if type(console) != int or console < 1 or console > 65535:
			raise DynamipsError, 'invalid console port'

		send(self.p, 'pemu set_con_tcp %s %i' % (self.name, console))
		self.__console = console

	def __getconsole(self):
		""" Returns console port
		"""
		return self.__console

	console = property(__getconsole, __setconsole, doc = 'The fw console port')

	def __setram(self, ram):
		""" Set amount of RAM allocated to this fw
		ram: (int) amount of RAM in MB
		"""
		if type(ram) != int or ram < 1:
			raise DynamipsError, 'invalid ram size'

		send(self.p, 'pemu set_ram  %s %i' % (self.name, ram))
		self.__ram = ram

	def __getram(self):
		""" Returns the amount of RAM allocated to this router
		"""
		return self.__ram

	ram = property(__getram, __setram, doc = 'The amount of RAM allocated to this fw')

	def __setimage(self, image):
		""" Set the IOS image for this fw
		image: path to IOS image file
		"""
		if type(image) not in [str, unicode]:
			raise DynamipsError, 'invalid image'

		# Can't verify existance of image because path is relative to backend
		#send the image filename enclosed in quotes to protect it
		send(self.p, 'pemu set_image %s %s' % (self.name,'"' + image + '"'))
		self.__image = image

	def __getimage(self):
		""" Returns path of the image being used by this fw
		"""
		return self.__image

	image = property(__getimage, __setimage, doc = 'The IOS image file for this fw')

	def __setserial(self, serial):
		""" Set the serial for this fw
		serial: serial number of this fw
		"""
		if type(serial) != str:
			raise DynamipsError, 'invalid serial'
		#TODO verify serial
		send(self.p, 'pemu set_serial %s %s' % (self.name, serial))
		self.__serial = serial

	def __getserial(self):
		""" Returns path of the serial being used by this fw
		"""
		return self.__serial

	serial = property(__getserial, __setserial, doc = 'The serial for this fw')

	def __setkey(self, key):
		""" Set the key for this fw
		key: key number of this fw
		"""
		if type(key) != str:
			raise DynamipsError, 'invalid key'
		#TODO verify key
		send(self.p, 'pemu set_key %s %s' % (self.name, key))
		self.__key = key

	def __getkey(self):
		""" Returns path of the key being used by this fw
		"""
		return self.__key

	key = property(__getkey, __setkey, doc = 'The key for this fw')

	def add_interface(self,pa1,port1):
		send(self.p, 'pemu create_nic %s %i 00:00:ab:cd:%s%s:0%i' % (self.name, port1,self.first_mac_number,self.second_mac_number, port1))

	def connect_to_dynamips (self, local_port, dynamips, remote_slot, remote_int, remote_port):
		#figure out the destionation port according to interface descritors
		if remote_slot.adapter in ['ETHSW', 'ATMSW', 'FRSW', 'Bridge']:
			# This is a virtual switch that doesn't provide interface descriptors
			dst_port = remote_port
		else:
			# Look at the interfaces dict to find out what the real port is as
			# as far as dynamips is concerned
			try:
				dst_port = remote_slot.interfaces[remote_int][remote_port]
			except KeyError:
				raise DynamipsError, 'invalid interface'

		#validate the connection
		if not validate_connect('e', remote_int, self.p, self, local_port, dynamips, remote_slot, remote_port):
			return
		
		# Allocate a UDP port for the local side of the NIO
		src_udp = self.p.udp
		self.p.udp = self.p.udp + 1
		debug("new base UDP port for pemuwrapper at " + self.p.name + ":" + str(self.p.port) + " is now: " + str(self.p.udp))

		# Now allocate one for the destination side
		dst_udp = dynamips.udp
		dynamips.udp = dynamips.udp + 1
		debug ("new base UDP port for dynamips at " + dynamips.host + ":" + str(dynamips.port) + " is now: " + str(dynamips.udp))

		if self.p.host == dynamips.host:
			# source and dest adapters are on the same dynamips server, perform loopback binding optimization
			src_ip = '127.0.0.1'
			dst_ip = '127.0.0.1'
		else:
			# source and dest are on different dynamips servers
			src_ip = self.p.name
			dst_ip = dynamips.host
		    
		#create the fw side of UDP connection
		send(self.p, 'pemu create_udp %s %i %i %s %i' % (self.name, local_port, src_udp, dst_ip, dst_udp))
		self.nios[local_port] = UDPConnection(src_udp, dst_ip, dst_udp)
		
		#create the dynamips side of UDP connection - the NIO and connect it to the router
		remote_nio = NIO_udp(dynamips, dst_udp, src_ip, src_udp)
		if isinstance(remote_slot, Bridge):
			# Bridges don't use ports
			remote_slot.nio(nio=remote_nio)
		else:
			remote_slot.nio(port=dst_port, nio=remote_nio)	

	def connect_to_fw (self, local_port, remote_fw, remote_port):
		# Allocate a UDP port for the local side
		src_udp = self.p.udp
		self.p.udp += 1
		debug("new base UDP port for pemuwrapper at " + self.p.name + ":" + str(self.p.port) + " is now: " + str(self.p.udp))

		# Now allocate one for the destination side
		dst_udp = remote_fw.p.udp
		remote_fw.p.udp += 1
		debug("new base UDP port for pemuwrapper at " + remote_fw.p.name + ":" + str(remote_fw.p.port) + " is now: " + str(remote_fw.p.udp))

		if self.p.host == remote_fw.p.host:
			# source and dest adapters are on the same dynamips server, perform loopback binding optimization
			src_ip = '127.0.0.1'
			dst_ip = '127.0.0.1'
		else:
			# source and dest are on different dynamips servers
			src_ip = self.p.name
			dst_ip = remote_fw.p.host
		
		#create the local fw side of UDP connection
		send(self.p, 'pemu create_udp %s %i %i %s %i' % (self.name, local_port, src_udp, dst_ip, dst_udp))
		self.nios[local_port] = UDPConnection(src_udp, dst_ip, dst_udp)

		#create the remote fw side of UDP connection
		send(remote_fw.p, 'pemu create_udp %s %i %i %s %i' % (remote_fw.name, remote_port, dst_udp, src_ip, src_udp))
		remote_fw.nios[remote_port] = UDPConnection(dst_udp, src_ip, src_udp)
		
		
