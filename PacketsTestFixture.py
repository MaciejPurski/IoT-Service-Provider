#!/usr/bin/python3.6

import unittest
import Packets
from Packets import *
from Crypto import Random

class PacketsTestCase(unittest.TestCase):
	def test_ack(self):
		ack = PacketACK.create(10)
		buf = Packets.serialize(ack)

		self.assertEqual(len(buf), 2)

		deserialized = Packets.deserialize(buf)

		self.assertEqual(deserialized.fields.service_id, 10)

	def test_nak(self):
		nak = PacketNAK.create(127)
		buf = Packets.serialize(nak)

		self.assertEqual(len(buf), 2)

		deserialized = Packets.deserialize(buf)

		self.assertEqual(deserialized.fields.service_id, 127)

	def test_eot(self):
		eot = PacketEOT.create()
		buf = Packets.serialize(eot)

		self.assertEqual(len(buf), 1)

	def test_chall(self):
		r_bytes = b'abcdefgh'
		chall = PacketCHALL.create(r_bytes)

		buf = Packets.serialize(chall)

		self.assertEqual(len(buf), 9)

		deserialized = Packets.deserialize(buf)

		self.assertEqual(deserialized.fields.random_bytes, r_bytes)

	def test_chall_wrong_length(self):
		r_bytes = b'this_buf_is_too_long'

		with self.assertRaises(ValueError):
			PacketCHALL.create(r_bytes)

	def test_chall_resp(self):
		r_bytes = Random.new().read(256)
		chall_resp = PacketCHALL_RESP.create(r_bytes)

		buf = Packets.serialize(chall_resp)

		self.assertEqual(len(buf), 257)

		deserialized = Packets.deserialize(buf)

		self.assertEqual(deserialized.fields.encrypted_bytes, r_bytes)

	def test_packet_key(self):
		r_bytes = Random.new().read(16)
		key = PacketKEY.create(r_bytes)

		buf = Packets.serialize(key)

		self.assertEqual(len(buf), 17)

		deserialized = Packets.deserialize(buf)

		self.assertEqual(deserialized.fields.symmetric_key, r_bytes)

	def test_val(self):
		val = PacketVAL.create(8, 13.89, 1234467)
		buf = Packets.serialize(val)

		self.assertEqual(len(buf), 10)

		deserialized = Packets.deserialize(buf)

		self.assertEqual(deserialized.fields.service_id, val.fields.service_id)
		self.assertEqual(round(deserialized.fields.value, 5), round(val.fields.value, 5))
		self.assertEqual(deserialized.fields.timestamp, val.fields.timestamp)

	def test_set(self):
		setp = PacketSET.create(8, 13.254)
		buf = Packets.serialize(setp)

		self.assertEqual(len(buf), 6)

		deserialized = Packets.deserialize(buf)

		self.assertEqual(deserialized.fields.service_id, setp.fields.service_id)
		self.assertEqual(round(deserialized.fields.value, 5), round(setp.fields.value, 5))

	def test_exit(self):
		exit = PacketEXIT.create(0)
		buf = Packets.serialize(exit)

		self.assertEqual(len(buf), 2)

		deserialized = Packets.deserialize(buf)

		self.assertEqual(deserialized.fields.service_id, 0)

	def test_id(self):
		exit = PacketID.create(3)
		buf = Packets.serialize(exit)

		self.assertEqual(len(buf), 2)

		deserialized = Packets.deserialize(buf)

		self.assertEqual(deserialized.fields.device_id, 3)

	def test_desc(self):
		name = b'abdefg'
		unit = b'Cels'
		desc = PacketDESC.create(2, name, unit, 0.0, 100.0)
		buf = Packets.serialize(desc)

		self.assertEqual(len(buf), 14 + len(name))

		deserialized = Packets.deserialize(buf)

		self.assertEqual(deserialized.fields.dev_class, 2)
		self.assertEqual(deserialized.fields.name, desc.fields.name)
		self.assertEqual(deserialized.fields.unit, desc.fields.unit)
		self.assertEqual(round(deserialized.fields.min_value, 5), round(desc.fields.min_value, 5))
		self.assertEqual(round(deserialized.fields.max_value, 5), round(desc.fields.max_value, 5))



if __name__ == '__main__':
    unittest.main()