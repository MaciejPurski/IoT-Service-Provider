import socket
from CryptoCore import *
from Packets import packet_factory


class Connection:
	def __init__(self, ip, port):
		self.ip = ip
		self.port = port
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def establish_connection(self):
		self.sock.connect((self.ip, self.port))

	def packet_read(self, encrypted):
		packet_id = self.sock.recv(1)
		bytes_rcd = 0
		buffer = bytearray('')
		packet = packet_factory(packet_id)
		p_length = packet.pLengthEncrypted if encrypted else packet.pLength
		while bytes_rcd < p_length:
			chunk = self.sock.recv(p_length - bytes_rcd)
			#TODO error check
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
