import struct


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
	def __init__(self, pid, p_len, format_str):
		self.pid = pid
		self.p_len = p_len
		self.p_len_encrypted = (p_len / 16 + 1) * 16  # AES encrypted message length
		self.format_str = format_str
		self._values_tuple = ()

	def deserialize(self, buffer):
		self._values_tuple = struct.unpack(buffer, self.format_str)
		#TODO error check

	def serialize(self):
		return struct.pack(self.format_str, self._values_tuple)


class PacketACK(Packet):
	def __init__(self):
		super().__init__(PacketType.ACK, 1, 'b')

	def set_fields(self, service_id):
		if not isinstance(service_id, int):
			raise TypeError('service_id should be int')

		super()._values_tuple = (service_id, )

	def packet_id(self):
		return super()._values_tuple[0]


class PacketNAK(Packet):
	def __init__(self):
		super().__init__(PacketType.NAK, 1, 'b')

	def set_fields(self, service_id):
		if not isinstance(service_id, int):
			raise TypeError('service_id should be int')

		super()._values_tuple = (service_id,)

	def packet_id(self):
		return super()._values_tuple[0]


class PacketEOT(Packet):
	def __init__(self):
		super().__init__(PacketType.EOT, 0, '')


class PacketCHALL(Packet):
	def __init__(self):
		super().__init__(PacketType.CHALL, 8, '')

	def set_fields(self, random_bytes):
		if not isinstance(random_bytes, bytes):
			raise TypeError('argument should be of type bytes')

		if len(random_bytes) != 8:
			raise ValueError('random bytes len should be equal 8')

		super()._values_tuple = (random_bytes, )

	def random_bytes(self):
		return super()._values_tuple[0]


class PacketCHALL_RESP(Packet):

	def __init__(self):
		super().__init__(PacketType.CHALL_RESP, 256, '8c')

	def set_fields(self, encrypted_bytes):
		if not isinstance(encrypted_bytes, bytes):
			raise TypeError('argument should be of type bytes')

		if len(encrypted_bytes) != 256:
			raise ValueError('encrypted bytes len should be equal 256')

		super()._values_tuple = (encrypted_bytes, )

	def encrypted_bytes(self):
		return super()._values_tuple[0]


class PacketKEY(Packet):
	def __init__(self):
		super().__init__(PacketType.KEY, 16, '16c')
		self.symetric_key = bytes('')

	def set_fields(self, symetric_key):
		if not isinstance(symetric_key, bytes):
			raise TypeError('argument should be of type bytes')

		if len(symetric_key) != 8:
			raise ValueError('random bytes len should be equal 8')

		super()._values_tuple = (symetric_key, )


class PacketDESC(Packet):
	def __init__(self):
		super().__init__(PacketType.DESC, 77, '1b 64s 4s f f')

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

		super()._values_tuple = (dev_class, name, unit, min_value, max_value)

	def dev_class(self):
		return super()._values_tuple[0]

	def name(self):
		return super()._values_tuple[1]

	def unit(self):
		return super()._values_tuple[2]

	def min_value(self):
		return super()._values_tuple[3]

	def max_value(self):
		return super()._values_tuple[4]


class PacketVAL(Packet):
	def __init__(self):
		super().__init__(PacketType.VAL, 9, 'b f 4I')

	def set_fields(self, service_id, value, timestamp):
		if not isinstance(service_id, int) or not isinstance(value, value)\
				or not isinstance(timestamp, int):
			raise TypeError('wrong argument type')

		super()._values_tuple = (service_id, value, timestamp)

	def service_id(self):
		return super()._values_tuple[0]

	def value(self):
		return super()._values_tuple[1]

	def timestamp(self):
		return super()._values_tuple[2]


class PacketSET(Packet):
	def __init__(self):
		super().__init__(PacketType.SET, 5, 'b f')

	def set_fields(self, service_id, value):
		if not isinstance(service_id, int) or not isinstance(value, value):
			raise TypeError('wrong argument type')

		super()._values_tuple = (service_id, value)


class PacketEXIT(Packet):
	def __init__(self):
		super().__init__(PacketType.EXIT, 1, 'b')

	def set_fields(self, service_id):
		if not isinstance(service_id, int):
			raise TypeError('wrong argument type')

		super()._values_tuple = (service_id, )


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
		raise ValueError('Packet type unkown')
