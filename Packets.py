import struct
from collections import namedtuple

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
	EXIT = 0x0a
	ID = 0x0b

def packet_factory(pid):
	if pid == PacketType.ACK:
		return PacketACK
	elif pid == PacketType.NAK:
		return PacketNAK
	elif pid == PacketType.DESC:
		return PacketDESC
	elif pid == PacketType.CHALL_RESP:
		return PacketCHALL_RESP
	elif pid == PacketType.CHALL:
		return PacketCHALL
	elif pid == PacketType.KEY:
		return PacketKEY
	elif pid == PacketType.EOT:
		return PacketEOT
	elif pid == PacketType.EXIT:
		return PacketEXIT
	elif pid == PacketType.SET:
		return PacketSET
	elif pid == PacketType.VAL:
		return PacketVAL
	elif pid == PacketType.ID:
		return PacketID
	else:
		raise ValueError('Packet type unkown')

def deserialize(buf):
	# recognize packet based on its pid TODO: mapa
	Packet_class = packet_factory(buf[0])
	# create packet instance
	if Packet_class == PacketDESC:
		pack_object = Packet_class(len(buf) - 14)
		fields_tuple = pack_object.Packet_struct.unpack(buf)
	else:
		pack_object = Packet_class()
		# parse fields according to given format string in packet_struct
		fields_tuple = Packet_class.Packet_struct.unpack(buf)

	# cast fields to the corresponding nameduple
	pack_object.fields = Packet_class.Packet_tuple._make(fields_tuple)

	return pack_object


def serialize(packet):
	return packet.Packet_struct.pack(*packet.fields)


class PacketACK:
	pid = 0x01
	Packet_tuple = namedtuple('ACK', 'pid service_id')
	Packet_struct = struct.Struct('=B B')

	@classmethod
	def create(cls, service_id):
		pack = cls()
		pack.fields = pack.Packet_tuple(cls.pid, service_id)
		return pack


class PacketNAK:
	pid = 0x02
	Packet_tuple = namedtuple('NAK', 'pid service_id')
	Packet_struct = struct.Struct('=B B')

	@classmethod
	def create(cls, service_id):
		pack = cls()
		pack.fields = pack.Packet_tuple(cls.pid, service_id)
		return pack


class PacketEOT:
	pid = 0x03
	Packet_tuple = namedtuple('EOT', 'pid')
	Packet_struct = struct.Struct('=B')

	@classmethod
	def create(cls):
		pack = cls()
		pack.fields = pack.Packet_tuple(cls.pid)
		return pack


class PacketCHALL:
	pid = 0x04
	Packet_tuple = namedtuple('CHALL', 'pid random_bytes')
	Packet_struct = struct.Struct('=B 8s')

	@classmethod
	def create(cls, random_bytes):
		if len(random_bytes) != 8:
			raise ValueError("{}: Expected 8 bytes buffer, got: {}".format(cls.__name__, len(random_bytes)))

		pack = cls()
		pack.fields = pack.Packet_tuple(cls.pid, random_bytes)
		return pack


class PacketCHALL_RESP:
	pid = 0x05
	Packet_tuple = namedtuple('CHALL_RESP', 'pid encrypted_bytes')
	Packet_struct = struct.Struct('=B 256s')

	@classmethod
	def create(cls, encrypted_bytes):
		if len(encrypted_bytes) != 256:
			raise ValueError("{}: Expected 256 bytes buffer, got: {}".format(cls.__name__, len(encrypted_bytes)))

		pack = cls()
		pack.fields = pack.Packet_tuple(cls.pid, encrypted_bytes)
		return pack

class PacketKEY:
	pid = 0x06
	Packet_tuple = namedtuple('KEY', 'pid symmetric_key')
	Packet_struct = struct.Struct('=B 256s')

	@classmethod
	def create(cls, symmetric_key):
		if len(symmetric_key) != 256:
			raise ValueError("{}: Expected 256 bytes buffer, got: {}".format(cls.__name__, len(symmetric_key)))

		pack = cls()
		pack.fields = pack.Packet_tuple(cls.pid, symmetric_key)
		return pack


class PacketDESC:
	pid = 0x07
	Packet_tuple = namedtuple('DESC', 'pid dev_class name unit min_value max_value')

	def __init__(self, name_len=64):
		format_str = '=B 1B ' + str(name_len + 1) + 's 4s f f'
		self.Packet_struct = struct.Struct(format_str)

	@classmethod
	def create(cls, dev_class, name, unit, min_value, max_value):
		if len(name) > 2048:
			raise ValueError("Human readable name too long")

		pack = cls(len(name))
		pack.fields = pack.Packet_tuple(cls.pid, dev_class, name + b'\0x00', unit + b'\x00', min_value, max_value)
		with open('desc', 'wb') as f:
			f.write(serialize(pack))
			f.close()
		return pack

class PacketVAL:
	pid = 0x08
	Packet_tuple = namedtuple('VAL', 'pid service_id value timestamp')
	Packet_struct = struct.Struct('=B B f I')

	@classmethod
	def create(cls, service_id, value, timestamp):
		pack = cls()
		pack.fields = pack.Packet_tuple(cls.pid, service_id, value, timestamp)
		with open('val', 'wb') as f:
			f.write(serialize(pack))
			f.close()
		return pack

class PacketSET:
	pid = 0x09
	Packet_tuple = namedtuple('SET', 'pid service_id value')
	Packet_struct = struct.Struct('=B B f')

	@classmethod
	def create(cls, service_id, value):
		pack = cls()
		pack.fields = pack.Packet_tuple(cls.pid, service_id, value)
		return pack

class PacketEXIT:
	pid = 0x0a
	Packet_tuple = namedtuple('EXIT', 'pid service_id')
	Packet_struct = struct.Struct('=B B')

	@classmethod
	def create(cls, service_id):
		pack = cls()
		pack.fields = pack.Packet_tuple(cls.pid, service_id)
		return pack

class PacketID:
	pid = 0x0b
	Packet_tuple = namedtuple('ID', 'pid device_id')
	Packet_struct = struct.Struct('=B B')

	@classmethod
	def create(cls, device_id):
		pack = cls()
		pack.fields = pack.Packet_tuple(cls.pid, device_id)
		return pack