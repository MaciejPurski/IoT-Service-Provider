import SocketLayer
from Packets import *
import socket
import sys
from Crypto import Random
from CryptoCore import *
import struct


class Protocol:
	def __init__(self, server_ip, port, public_key, private_key):
		self.cipher_rsa = CipherRSA(public_key, private_key)
		self.connection = SocketLayer.Connection(server_ip, port)
		self.cipher_aes = CipherAES()
		self.prefix_struct = struct.Struct('=B I')

	def authenticate(self):
		# authenticate client in for the server
		rcv_packet = parse_packet()
		if not isinstance(rcv_packet, Packets.PacketCHALL):
			raise TypeError('wrong packet received')

		encrypted_bytes = CipherRSA.encrypt_rsa(rcv_packet.fields.random_bytes)
		chall_resp = PacketCHALL_RESP(encrypted_bytes)

		send_packet(chall_resp, False)
		# server authentication
		random_bytes = Random.new().read(8)
		chall = PacketCHALL(random_bytes)
		send_packet(chall)


	def register_seq(self, descriptorsList):
		self.connection.establish_connection()
		try:
			self.authenticate()
		except socket.error as e:
			sys.stderr.write('Network connection problem ({0})'.format(e))
			sys.exit(1)
		except (ValueError, TypeError) as e:
			sys.stderr.write('Protocol error ({0})'.format(e))
			self.connection.sock.close()
			sys.exit(1)

	def parse_packet(self):
		packets_data = self.connection.next_packet()

		# encrypted
		if packets_data[1]:
			packets_buf = self.cipher_aes.decrypt_aes(packets_data[0])
		else:
			packets_buf = packets_data[0]

		# TODO exceptions handling
		packet = Packets.deserialize(packets_buf)
		print('Packet received:')
		print(packet.fields)
		return packet

	def send_packet(self, packet, should_encrypt):
		packets_data = Packets.serialize(packet)
		initial_data_length = len(packets_data)

		if should_encrypt:
			packets_data = self.cipher_aes.encrypt_aes(packets_data)
	

		# TODO exceptions handling
		self.connection.send_data(packets_data)
		print('Packet sent:')
		print(packet.fields)
