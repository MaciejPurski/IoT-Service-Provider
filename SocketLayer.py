import socket
from PacketsTypes import packetsDict

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
		packetLen = packetsDict[packetId].pLengthEncrypted if encrypted else packetsDict[packetId].pLength
		while bytesRcd < packetLen:
			pass