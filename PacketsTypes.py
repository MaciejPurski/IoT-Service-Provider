class PacketType:
	ACK = 0x01
	NAK = 0x02
	EOT = 0x03
	CHALL = 0x04
	CHALL_RESP = 0x05
	KEY = 0x06
	DESC = 0x07
	VAL = 0x08
	SET = 0x09
	EXIT = 0xa0

class Packet:
	def __init__(self, pId, pLength, pFormat):
		self.pId = pId
		self.pLength = pLength
		self.pLengthEncrypted = (pLength / 16 + 1) * 6 # AES encrypted message length
		self.pFormatString = pFormat

packetsDict = { PacketType.ACK : Packet(PacketType.ACK, 1, ''),
				  PacketType.NAK : Packet(PacketType.NAK, 1, ''),
				  PacketType.EOT : Packet(PacketType.EOT, 0, ''),
                  PacketType.CHALL : Packet(PacketType.CHALL, 8, ''),
                  PacketType.CHALL_RESP : Packet(PacketType.CHALL_RESP, 256, ''),
                  PacketType.KEY : Packet(PacketType.ACK, 16, ''),
                  PacketType.DESC : Packet(PacketType.DESC, 76, ''),
                  PacketType.VAL : Packet(PacketType.VAL, 9, ''),
                  PacketType.SET : Packet(PacketType.SET, 5, ''),
                  PacketType.EXIT : Packet(PacketType.EXIT, 0, '') }
