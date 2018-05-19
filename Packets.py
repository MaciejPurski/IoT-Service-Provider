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
	EXIT = 0xa0
	ID = 0xa1

class Packet:
	def __init__(self, pid, format_str, values_namedtuple):
		self.pid = pid
		self.packet_struct = struct.Struct(format_str)
		self.values_namedtuple = values_namedtuple
		self.fields = ()

	def serialize(self):
		print("pid: {}".format(self.pid))
		print(bytes(self.pid))

		return self.packet_struct.pack(self.pid, *self.fields)


class PacketACK(Packet):
	ACK = namedtuple('ACK', 'packet_id')
	format_str = '=b b'

	def __init__(self):
		super().__init__(PacketType.ACK, PacketACK.format_str, PacketACK.ACK)


class PacketNAK(Packet):
	NAK = namedtuple('NAK', 'packet_id')
	format_str = '=b b'
	packet_type = PacketType.NAK

	def __init__(self):
		super.__init__(packet_type, format_str, NAK)


class PacketEOT(Packet):
	EOT = namedtuple('EOT', '')
	format_str = '=b'
	packet_type = PacketType.EOT

	def __init__(self):
		super.__init__(packet_type, format_str, EOT)


class PacketCHALL(Packet):
	CHALL = namedtuple('CHALL', 'random_bytes')
	format_str = '=b 8b'
	packet_type = PacketType.EOT

	def __init__(self):
		super.__init__(packet_type, format_str, CHALL)


class PacketCHALL_RESP(Packet):
	CHALL_RESP = namedtuple('CHALL_RESP', 'encrypted_bytes')
	format_str = '=b 256b'
	packet_type = PacketType.CHALL_RESP

	def __init__(self):
		super.__init__(packet_type, format_str, CHALL_RESP)

class PacketKEY(Packet):
	KEY = namedtuple('KEY', 'symmetric_key')
	format_str = '=b 16b'
	packet_type = PacketType.CHALL_RESP

	def __init__(self):
		super.__init__(packet_type, format_str, KEY)


class PacketDESC(Packet):
	DESC = namedtuple('CHALL_RESP', 'dev_class name unit min_value max_value')
	packet_type = PacketType.DESC

	def __init__(self, name_len = 64):
		format_str = '=b 1b ' + bytes(name_len) + 's 4s f f'
		super.__init__(packet_type, format_str, DESC)

class PacketVAL(Packet):
	VAL = namedtuple('VAL', 'service_id value timestamp')
	packet_type = PacketType.VAL
	format_str = '=b b f 4I'

	def __init__(self):
		super.__init__(packet_type, format_str, VAL)

class PacketSET(Packet):
	SET = namedtuple('SET', 'service_id value')
	packet_type = PacketType.SET
	format_str = '=b b f'

	def __init__(self):
		super.__init__(packet_type, format_str, SET)


class PacketEXIT(Packet):
	EXIT = namedtuple('EXIT', 'service_id')
	packet_type = PacketType.EXIT
	format_str = '=b b'

	def __init__(self):
		super.__init__(packet_type, format_str, EXIT)


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


def packet_deserialize(buf):
	pack = packet_factory(buf[0])
	pack.fields = pack.values_namedtuple._make(pack.packet_struct.unpack(buf))
	return pack