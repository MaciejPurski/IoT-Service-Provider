import SocketLayer
from Packets import *
import socket
import sys
from Crypto import Random
from CryptoCore import *
import struct


class Protocol:
	def __init__(self, server_ip, port, device_id, public_key, private_key):
		self.cipher_rsa = CipherRSA(public_key, private_key)
		self.connection = SocketLayer.Connection(server_ip, port)
		self.device_id = int(device_id)
		self.cipher_aes = CipherAES()
		self.prefix_struct = struct.Struct('=I B')


	def authenticate(self):
		# introduce client to the server
		id_packet = PacketID.create(self.device_id)
		self.send_packet(id_packet, False)

		# authenticate client
		rcv_packet = self.parse_packet()
		if not isinstance(rcv_packet, PacketCHALL):
			raise TypeError('Wrong packet received')

		# send encrypted challenge response
		challenge_bytes = rcv_packet.fields.random_bytes
		signature = self.cipher_rsa.sign(challenge_bytes)

		chall_resp = PacketCHALL_RESP.create(signature)
		self.send_packet(chall_resp, False)

		# server authentication - send random bytes
		random_bytes = Random.new().read(8)
		chall = PacketCHALL.create(random_bytes)
		self.send_packet(chall, False)

		# verify server's signature
		rcv_packet = self.parse_packet()
		if not isinstance(rcv_packet, PacketCHALL_RESP):
			raise TypeError('wrong packet received')

		if not self.cipher_rsa.verify(random_bytes, rcv_packet.fields.encrypted_bytes):
			self.send_NAK()
			raise RuntimeError('Server verification failed')

		# if the authentication goes OK, the server should send the symmetric key
		rcv_packet = self.parse_packet()
		if not isinstance(rcv_packet, PacketKEY):
			raise TypeError('Wrong packet received')

		self.cipher_aes.set_key(rcv_packet.fields.symmetric_key)


	def register(self, services_list):
		self.connection.establish_connection()
		try:
			self.authenticate()
		except socket.error as e:
			sys.stderr.write('Network connection problem ({0})'.format(e))
			sys.exit(1)
		#except (ValueError, TypeError) as e:
		#	sys.stderr.write('Authentication failed ({0})'.format(e))
		#	self.connection.sock.close()
		#	sys.exit(1)

		for service in services_list:
			# send service description
			desc_packet = PacketDESC(service.service_class, service.name, service.unit, service.min_value, service.max_value)
			self.send_packet(desc_packet, True)

			rcv_packet = self.parse_packet()
			if not isinstance(rcv_packet, PacketACK):
				raise TypeError('Wrong packet received')

			service.set_id(rcv_packet.fields.service_id)

		self.connection.close_connection()


	def parse_packet(self):
		packets_data = self.connection.next_packet()
		print("Received {} bytes of data".format(len(packets_data)))

		# encrypted
		if packets_data[1]:
			packets_buf = self.cipher_aes.decrypt_aes(packets_data[0])
		else:
			packets_buf = packets_data[0]

		# TODO exceptions handling
		packet = deserialize(packets_buf)
		print('Packet received:')
		print(packet.fields)
		return packet

	def send_packet(self, packet, should_encrypt):
		packets_data = serialize(packet)
		initial_data_length = len(packets_data)

		if should_encrypt:
			packets_data = self.cipher_aes.encrypt_aes(packets_data)

		prefix = self.prefix_struct.pack(initial_data_length, int(should_encrypt == 'true'))
		# TODO exceptions handling
		self.connection.send_data(prefix + packets_data)
		print('Packet sent:')
		print(packet.fields)


	def send_NAK(self):
		nak_packet = PacketNAK.create(0)
		self.connection.send_packet(nak_packet)