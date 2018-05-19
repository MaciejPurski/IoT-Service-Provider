#!/usr/bin/python3.6

import unittest
import Packets

class PacketsTestCase(unittest.TestCase):
	def test_ack(self):
		ack = Packets.packet_factory(Packets.PacketType.ACK)
		ack.fields = ack.values_namedtuple(Packets.PacketType.ACK, 10)
		buf = ack.serialize()

		self.assertEqual(len(buf), 2)

		print("pid value")
		print(int(buf[0]))

		deserialized_ack = Packets.packet_deserialize(buf)

		self.assertEqual(deserialized_ack.fields.packet_id, 10)

if __name__ == '__main__':
    unittest.main()