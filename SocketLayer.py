import socket
from CryptoCore import *
from Packets import packet_factory
import sys
import struct

class Connection:
	int_struct = struct.Struct('=I')

	def __init__(self, ip, port):
		self.ip = ip
		self.port = port
		try:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		except socket.error as e:
			sys.stderr.write('Error creating socket: ({0})'.format(e))
			sys.exit(1)

	def establish_connection(self):
		try:
			self.sock.connect((self.ip, self.port))
		except socket.gaierror as e:
			sys.stderr.write('Address related error connecting to server: ({0})'.format(e))
		except socket.error as e:
			sys.stderr.write('Error connecting to server: ({0})'.format(e))

	def next_packet(self):
		# first byte contains information whether the packet is encrypted
		b = read_bytes(1)
		encrypted = if b[0] == 0x01 True else False

		packet_length = int_struct.unpack(read_bytes(4))

		# if packet is encrypted, calculate proper length
		if encrypted:
			packet_legnth = CipherAES.encrypted_msg_length(packet_length)

		packet_bytes = read_bytes(packet_length)

		# tuple containing information, if we should decrypt the data
		return (packet_bytes, encrypted)

	def packet_send(self, packet):
		self.sock.send(buffer)
		#TODO error checking

	def read_bytes(self, n_bytes):
		bytes_rcd = 0
		buf = bytearray()

		while bytes_rcd < n_bytes:
			chunk = self.sock.recv(n_bytes - bytes_rcd)
			if chunk == 0: # socket has been closed
				raise socket.error('Socket closed suddenly')
			buf.append(chunk)

		return buf
