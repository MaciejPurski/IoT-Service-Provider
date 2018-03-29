import socket
from CryptoCore import *
from PacketsTypes import packetFactory

class Connection:
	def __init__(self, ip, port):
		self.ip = ip
		self.port = port
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def establishConnection(self):
		self.sock.connect((self.ip, self.port))

	def packetRead(self, encrypted):
		packetId = self.sock.recv(1)
		bytesRcd = 0
		buffer = bytearray('')
		packet = packetFactory(packetId)
		pLength = packet.pLengthEncrypted if encrypted \
										  else packet.pLength
		while bytesRcd < pLength:
			chunk = self.sock.recv(pLength - bytesRcd)
			#TODO error check
			buffer.append(chunk)

		if encrypted:
			packet.deserialize(decryptAES(buffer))
		else:
			packet.deserialize(buffer)

		return packet


	def packetSend(self, packet, encrypted):
		if encrypted:
			buffer = encryptAES(packet.serialize())
		else:
			buffer = packet.serialize()

		self.sock.send(buffer)
		#TODO error checking