import socket
from CryptoCore import *
from Packets import packet_factory
import sys

class Connection:
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

	def packet_read(self, encrypted):
		#check packet type
		packet_id = self.sock.recv(1)
		packet = packet_factory(packet_id)

		bytes_rcd = 0
		buffer = bytearray('')
		p_length = packet.pLengthEncrypted if encrypted else packet.pLength

		while bytes_rcd < p_length:
			chunk = self.sock.recv(p_length - bytes_rcd)
			if chunk == 0: #socket has been closed
				raise socket.error('Socket closed suddenly')
			buffer.append(chunk)

		if encrypted:
			packet.deserialize(decrypt_aes(buffer))
		else:
			packet.deserialize(buffer)

		return packet

	def packet_send(self, packet, encrypted):
		if encrypted:
			buffer = encrypt_aes(packet.serialize())
		else:
			buffer = packet.serialize()

		self.sock.send(buffer)
		#TODO error checking
