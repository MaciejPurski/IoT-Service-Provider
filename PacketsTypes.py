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

class PacketACK(Packet):
	def __init__(self):
		self.super(PacketType.ACK, 1, '')

	def setFields(self, serviceID):
		self.serviceID = serviceID

	def deserialize(self, buffer):
		pass

	def serialize(self):
		return bytearray('')

class PacketNAK(Packet):
	def __init__(self):
		self.super(PacketType.NAK, 1, '')

	def setFields(self, serviceID):
		self.serviceID = serviceID

	def serialize(self):
		return bytearray('')

	def deserialize(self, buffer):
		pass


class PacketEOT(Packet):
	def __init__(self):
		self.super(PacketType.EOT, 0, '')

	def serialize(self):
		return bytearray('')

	def deserialize(self, buffer):
		pass


class PacketCHALL(Packet):
	def __init__(self):
		self.super(PacketType.CHALL, 8, '')

	def setFields(self, randomBytes):
		self.randomBytes = randomBytes

	def serialize(self):
		return bytearray('')

	def deserialize(self, buffer):
		pass

class PacketCHALL_RESP(Packet):
	def __init__(self):
		self.super(PacketType.CHALL_RESP, 256, '')

	def setFields(self, encryptedBytes):
		self.encryptedBytes = encryptedBytes

	def serialize(self):
		return bytearray('')

	def deserialize(self, buffer):
		pass


class PacketKEY(Packet):
	def __init__(self):
		self.super(PacketType.KEY, 16, '')

	def setFields(self, symetricKey):
		self.symetricKey = symetricKey

	def serialize(self):
		return bytearray('')

	def deserialize(self, buffer):
		pass

class PacketDESC(Packet):
	def __init__(self):
		self.super(PacketType.DESC, 76, '')

	def setFields(self, devClass, name, unit, minValue, maxValue):
		self.devClass = devClass
		self.name = name
		self.unit = unit
		self.minValue = minValue
		self.maxValue = maxValue

	def serialize(self):
		return bytearray('')

	def deserialize(self, buffer):
		pass

class PacketVAL(Packet):
	def __init__(self):
		self.super(PacketType.VAL, 9, '')

	def setFields(self, serviceId, nValue, timestamp):
		self.serviceId = serviceId
		self.nValue = nValue
		self.timestamp = timestamp

	def serialize(self):
		return bytearray('')

	def deserialize(self, buffer):
		pass

class PacketSET(Packet):
	def __init__(self):
		self.super(PacketType.SET, 5, '')

	def setFields(self, serviceId, value):
		self.serviceId = serviceId
		self.value = value

	def serialize(self):
		return bytearray('')

	def deserialize(self, buffer):
		pass

class PacketEXIT(Packet):
	def __init__(self):
		self.super(PacketType.EXIT, 1, '')

	def setFields(self, serviceId):
		self.serviceId = serviceId

	def serialize(self):
		return bytearray('')

	def deserialize(self, buffer):
		pass

def packetFactory(pId):
	if pId == PacketType.ACK:
		return PacketACK()
	elif pId == PacketType.NAK:
		return PacketNAK()
	elif pId == PacketType.DESC:
		return PacketDESC()
	elif pId == PacketType.CHALL_RESP:
		return PacketCHALL_RESP()
	elif pId == PacketType.CHALL:
		return PacketCHALL()
	elif pId == PacketType.EOT:
		return PacketEOT()
	elif pId == PacketType.EXIT:
		return PacketEXIT()
	elif pId == PacketType.SET:
		return PacketSET()
	elif pId == PacketType.VAL:
		return PacketVAL()
	else:
		raise ValueError('packet type unkown')

