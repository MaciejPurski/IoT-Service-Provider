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
	def __init__(self, pid, p_len, p_format_str):
		self.pid = pid
		self.p_len = p_len
		self.p_len_encrypted = (p_len / 16 + 1) * 6  # AES encrypted message length
		self.p_format_str = p_format_str


class PacketACK(Packet):
	def __init__(self):
		super().__init__(PacketType.ACK, 1, '')
		self.service_id = 0

	def set_fields(self, service_id):
		if not isinstance(service_id, int):
			raise TypeError('service_id should be int')

		self.service_id = service_id

	def deserialize(self, buffer):
		pass

	def serialize(self):
		return bytearray('')


class PacketNAK(Packet):

	def __init__(self):
		super().__init__(PacketType.NAK, 1, '')
		self.service_id = 0

	def set_fields(self, service_id):
		if not isinstance(service_id, int):
			raise TypeError('service_id should be int')

		self.service_id = service_id

	def serialize(self):
		return bytearray('')

	def deserialize(self, buffer):
		pass


class PacketEOT(Packet):

	def __init__(self):
		super().__init__(PacketType.EOT, 0, '')

	def serialize(self):
		return bytearray('')

	def deserialize(self, buffer):
		pass


class PacketCHALL(Packet):

	def __init__(self):
		super().__init__(PacketType.CHALL, 8, '')
		self.random_bytes = bytes('')

	def set_fields(self, random_bytes):
		if not isinstance(random_bytes, bytes):
			raise TypeError('argument should be of type bytes')

		if len(random_bytes) != 8:
			raise ValueError('random bytes len should be equal 8')

		self.random_bytes = random_bytes

	def serialize(self):
		return bytearray('')

	def deserialize(self, buffer):
		pass


class PacketCHALL_RESP(Packet):
	def __init__(self):
		super().__init__(PacketType.CHALL_RESP, 256, '')
		self.encrypted_bytes = bytes('')

	def set_fields(self, encrypted_bytes):
		if not isinstance(encrypted_bytes, bytes):
			raise TypeError('argument should be of type bytes')

		if len(encrypted_bytes) != 256:
			raise ValueError('encrypted bytes len should be equal 256')

		self.encrypted_bytes = encrypted_bytes

	def serialize(self):
		return bytearray('')

	def deserialize(self, buffer):
		pass


class PacketKEY(Packet):
	def __init__(self):
		super().__init__(PacketType.KEY, 16, '')
		self.symetric_key = bytes('')

	def set_fields(self, symetric_key):
		if not isinstance(symetric_key, bytes):
			raise TypeError('argument should be of type bytes')

		if len(symetric_key) != 8:
			raise ValueError('random bytes len should be equal 8')

		self.symetric_key = symetric_key

	def serialize(self):
		return bytearray('')

	def deserialize(self, buffer):
		pass


class PacketDESC(Packet):
	def __init__(self):
		super().__init__(PacketType.DESC, 76, '')
		self.dev_class = 0
		self.name = bytes('')
		self.unit = bytes('')
		self.min_value = 0.0
		self.max_value = 0.0

	def set_fields(self, dev_class, name, unit, min_value, max_value):
		if not isinstance(dev_class, int) or not isinstance(name, bytes)\
				or not isinstance(unit, bytes) or not isinstance(min_value, float)\
				or not isinstance(max_value, float):
			raise TypeError('wrong argument type')

		if dev_class > 3 or dev_class < 0:
			raise ValueError('wrong dev_class value')
		if len(name) > 64:
			raise ValueError('wrong name value')
		if len(unit) > 4:
			raise ValueError('wrong unit value')

		self.dev_class = dev_class
		self.name = name
		self.unit = unit
		self.min_value = min_value
		self.max_value = max_value

	def serialize(self):
		return bytearray('')

	def deserialize(self, buffer):
		pass


class PacketVAL(Packet):
	def __init__(self):
		super().__init__(PacketType.VAL, 9, '')
		self.service_id = 0
		self.value = 0.0
		self.timestamp = 0

	def set_fields(self, service_id, value, timestamp):
		if not isinstance(service_id, int) or not isinstance(value, value)\
				or not isinstance(timestamp, int):
			raise TypeError('wrong argument type')

		self.service_id = service_id
		self.value = value
		self.timestamp = timestamp

	def serialize(self):
		return bytearray('')

	def deserialize(self, buffer):
		pass


class PacketSET(Packet):
	def __init__(self):
		super().__init__(PacketType.SET, 5, '')
		self.service_id = 0
		self.value = 0.0

	def set_fields(self, service_id, value):
		if not isinstance(service_id, int) or not isinstance(value, value):
			raise TypeError('wrong argument type')
		self.service_id = service_id
		self.value = value

	def serialize(self):
		return bytearray('')

	def deserialize(self, buffer):
		pass


class PacketEXIT(Packet):
	def __init__(self):
		super().__init__(PacketType.EXIT, 1, '')
		self.service_id = 0

	def set_fields(self, service_id):
		if not isinstance(service_id, int):
			raise TypeError('wrong argument type')

		self.service_id = service_id

	def serialize(self):
		return bytearray('')

	def deserialize(self, buffer):
		pass


def packet_factory(pid):
	if pid == PacketType.ACK:
		return PacketACK()
	elif pid == PacketType.NAK:
		return PacketNAK()
	elif pid == PacketType.DESC:
		return PacketDESC()
	elif pid == PacketType.CHALL_RESP:
		return PacketCHALL_RESP()
	elif pid == PacketType.CHALL:
		return PacketCHALL()
	elif pid == PacketType.EOT:
		return PacketEOT()
	elif pid == PacketType.EXIT:
		return PacketEXIT()
	elif pid == PacketType.SET:
		return PacketSET()
	elif pid == PacketType.VAL:
		return PacketVAL()
	else:
		raise ValueError('packet type unkown')
