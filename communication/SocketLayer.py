import socket
from communication.CryptoCore import *
import sys
import struct


class Connection:
	int_struct = struct.Struct('=I')

	def __init__(self, ip, port):
		self.ip = ip
		self.port = int(port)

	def establish_connection(self):
		try:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			#self.sock.settimeout(5.0)
			self.sock.connect((self.ip, self.port))
		except socket.gaierror as e:
			sys.stderr.write('Address related error connecting to server: ({0}) \n'.format(e))
			exit(1)
		except socket.timeout as e:
			sys.stderr.write('Socket timeout: ({0}) \n'.format(e))
			exit(1)
		except socket.error as e:
			sys.stderr.write('Error connecting to server: ({0}) \n'.format(e))
			exit(1)

		print('Connection successfully established')

	def next_packet(self):
		# 4 bytes contain msg length
		packet_length = Connection.int_struct.unpack(self.read_bytes(4))[0]

		# first byte contains information whether the packet is encrypted
		b = self.read_bytes(1)
		encrypted = True if b[0] == 0x01 else False
		# if packet is encrypted, calculate proper length
		if encrypted:
			packet_length = CipherAES.encrypted_msg_length(packet_length)

		packet_bytes = self.read_bytes(packet_length)

		# tuple containing information, if we should decrypt the data
		return (packet_bytes, encrypted)

	def send_data(self, buf):
		self.sock.send(buf)

	def read_bytes(self, n_bytes):
		bytes_rcd = 0
		chunks = []

		while bytes_rcd < n_bytes:
			chunk = self.sock.recv(n_bytes - bytes_rcd)
			if chunk == b'':  # socket has been closed
				raise socket.error('Socket closed suddenly')
			chunks.append(chunk)
			bytes_rcd += len(chunk)

		return b''.join(chunks)

	def close_connection(self):
		self.sock.shutdown(socket.SHUT_RDWR)
		self.sock.close()
		print('Connection closed')
