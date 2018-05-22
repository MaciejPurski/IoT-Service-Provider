import socket
from CryptoCore import *
from Packets import packet_factory
import sys
import struct

class Connection:
	int_struct = struct.Struct('=I')

	def __init__(self, ip, port):
		self.ip = ip
		self.port = int(port)
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
			raise RuntimeError('Connection failed')
		except socket.error as e:
			sys.stderr.write('Error connecting to server: ({0})'.format(e))
			raise RuntimeError('Connection failed')

		print('Connection successfully established')

	def next_packet(self):
		# 4 bytes contain msg length
		packet_length = Connection.int_struct.unpack(self.read_bytes(4))[0]

		# first byte contains information whether the packet is encrypted
		b = self.read_bytes(1)
		encrypted = True if b[0] == 0x01 else False
		# if packet is encrypted, calculate proper length
		if encrypted:
			packet_legnth = CipherAES.encrypted_msg_length(packet_length)

		packet_bytes = self.read_bytes(packet_length)

		# tuple containing information, if we should decrypt the data
		return (packet_bytes, encrypted)

	def send_data(self, buf):
		self.sock.send(buf)
		#TODO error checking

	def read_bytes(self, n_bytes):
		bytes_rcd = 0
		chunks = []

		while bytes_rcd < n_bytes:
			chunk = self.sock.recv(n_bytes - bytes_rcd)
			print(type(chunk))
			if chunk == b'': # socket has been closed
				raise socket.error('Socket closed suddenly')
			chunks.append(chunk)
			bytes_rcd += len(chunk)

		return b''.join(chunks)

	def close_connection(self):
		self.sock.close()
		print('Connection closed')
