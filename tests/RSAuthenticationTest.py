#!/usr/bin/python3.6

import unittest
from communication.Packets import *
from Crypto import Random
from communication.CryptoCore import *
from communication.Packets import *
import struct
import sys


class AuthenticationTest(unittest.TestCase):
	def setUp(self):
		self.client_cipher_rsa = CipherRSA('keys/server-public.pem', 'keys/client-private.pem')
		self.server_cipher_rsa = CipherRSA('keys/client-public.pem', 'keys/server-private.pem')

	def test_simple_client_authentication(self):
		msg = get_random_bytes(8)
		signature = self.client_cipher_rsa.sign(msg)
		self.assertEqual(self.server_cipher_rsa.verify(msg, signature), True)

	def test_simple_server_authentication(self):
		msg = get_random_bytes(8)
		signature = self.server_cipher_rsa.sign(msg)
		self.assertEqual(self.client_cipher_rsa.verify(msg, signature), True)

	def test_packets_client_authentication(self):
		# server generate challenge
		msg = get_random_bytes(8)
		chall_packet = PacketCHALL.create(msg)

		chall_bytes = serialize(chall_packet)

		# server is sending a packet through the network
		rcv_packet = deserialize(chall_bytes)

		# send encrypted challenge response
		challenge_bytes = rcv_packet.fields.random_bytes
		signature = self.server_cipher_rsa.sign(challenge_bytes)

		resp_packet = PacketCHALL_RESP.create(signature)
		resp_bytes = serialize(resp_packet)
		# client sends the response

		rcv_packet = deserialize(resp_bytes)

		# server authentication - send random bytes
		result = self.client_cipher_rsa.verify(msg, rcv_packet.fields.encrypted_bytes)
		self.assertEqual(result, True)

	def test_packets_server_authentication(self):
		# server generate challenge
		msg = get_random_bytes(8)
		chall_packet = PacketCHALL.create(msg)

		chall_bytes = serialize(chall_packet)

		# server is sending a packet through the network
		rcv_packet = deserialize(chall_bytes)

		# send encrypted challenge response
		challenge_bytes = rcv_packet.fields.random_bytes
		signature = self.client_cipher_rsa.sign(challenge_bytes)

		resp_packet = PacketCHALL_RESP.create(signature)
		resp_bytes = serialize(resp_packet)
		# client sends the response

		rcv_packet = deserialize(resp_bytes)

		# server authentication - send random bytes
		result = self.server_cipher_rsa.verify(msg, rcv_packet.fields.encrypted_bytes)
		self.assertEqual(result, True)



if __name__ == '__main__':
    unittest.main()