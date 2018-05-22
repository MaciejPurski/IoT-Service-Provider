#!/usr/bin/python3.6
import SocketLayer
from Packets import *
import socket
import sys
from Crypto import Random
from CryptoCore import *
import struct
import sys


class AuthenticationTest:
	def __init__(self, serv_public_key, serv_private_key, client_public_key, client_private_key):
		self.client_cipher_rsa = CipherRSA(serv_public_key, client_private_key)
		self.server_cipher_rsa = CipherRSA(client_public_key, serv_private_key)
		self.cipher_aes = CipherAES()
		self.prefix_struct = struct.Struct('=I B')


	def authenticate(self):
		# Server generates challenge
		random_bytes = Random.new().read(8)
		chall_pack = PacketCHALL.create(random_bytes)

		# client receives data
		client_rcd_data = deserialize(serialize(chall_pack))
		encrypted_data = self.client_cipher_rsa.sign(client_rcd_data.fields.random_bytes)
		chall_resp = PacketCHALL_RESP.create(encrypted_data)

		#client resend chall_resp

		# server decrypts data
		server_rcd_data = deserialize(serialize(chall_resp))
		self.server_cipher_rsa.verify_signature(random_bytes, server_rcd_data.fields.encrypted_bytes)
		if random_bytes == decrypted:
			print("positive verification")
		else:
			print("Negative verification")

		#random_bytes = Random.new().read(8)
		#chall = PacketCHALL.create(random_bytes)
		#self.send_packet(chall, False)

		# verify server's signature
		#rcv_packet = self.parse_packet()
		#if not isinstance(rcv_packet, PacketCHALL_RESP):
			#raise TypeError('wrong packet received')



p = AuthenticationTest(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

p.authenticate()