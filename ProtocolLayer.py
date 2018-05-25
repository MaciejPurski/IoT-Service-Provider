import SocketLayer
from Packets import *
import socket
import sys
from Crypto import Random
from CryptoCore import *
import struct
import time


class Protocol:
	def __init__(self, server_ip, port, device_id, public_key, private_key):
		self.cipher_rsa = CipherRSA(public_key, private_key)
		self.connection = SocketLayer.Connection(server_ip, port)
		self.device_id = int(device_id)
		self.cipher_aes = CipherAES()

	def authenticate(self):
		# introduce client to the server
		self.send_packet(PacketID.create(self.device_id))

		# authenticate client
		rcv_packet = self.parse_packet()
		if not isinstance(rcv_packet, PacketCHALL):
			raise TypeError('Wrong packet received')

		# send encrypted challenge response
		challenge_bytes = rcv_packet.fields.random_bytes
		signature = self.cipher_rsa.sign(challenge_bytes)
		self.send_packet(PacketCHALL_RESP.create(signature))

		# server authentication - send random bytes
		random_bytes = get_random_bytes(8)
		chall = PacketCHALL.create(random_bytes)
		self.send_packet(chall, False)

		# verify server's signature
		rcv_packet = self.parse_packet()
		if not isinstance(rcv_packet, PacketCHALL_RESP):
			raise TypeError('wrong packet received')

		if not self.cipher_rsa.verify(random_bytes,
		                              rcv_packet.fields.encrypted_bytes):
			self.send_NAK()
			raise RuntimeError('Server verification failed')

		print('Server verified successfully!')

		# if the authentication goes OK, the server should send the symmetric key
		self.receive_session_key()


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

		print('Begin sending device descriptors:')
		self.send_descriptors(services_list)

		print('Registration finished successfully')
		self.connection.close_connection()

	def transmission(self, services_list):
		self.connection.establish_connection()
		print("Transmission began")

		# wait for the new session key
		self.receive_session_key()

		self.send_values(services_list)
		print("Values sent")

		# receive set
		for i in range(0, len(services_list)):
			packet = self.parse_packet()

			if isinstance(packet, PacketEOT):
				break

			if isinstance(packet, PacketEXIT):
				print("Received EXIT command, exiting")
				self.connection.close_connection()
				exit(0)

			if not isinstance(packet, PacketSET):
				raise RuntimeError('Wrong packet received')

			# try setting the received value
			set_success = services_list[packet.fields.service_id].set_value(packet.fields.value)

			if set_success:
				self.send_packet(PacketACK.create(0), encrypt=True)
			else:
				self.send_packet(PacketNAK.create(0), encrypt=True)

		self.connection.close_connection()
		print("Transmission finished")

	def parse_packet(self):
		packets_data = self.connection.next_packet()

		# encrypted
		if packets_data[1]:
			packets_buf = self.cipher_aes.decrypt(packets_data[0])
		else:
			packets_buf = packets_data[0]

		# TODO exceptions handling
		packet = deserialize(packets_buf)
		print('Packet received:')
		print(type(packet.fields).__name__)
		return packet

	def send_packet(self, packet, encrypt=False):
		prefix_struct = struct.Struct('=I B')
		packets_data = serialize(packet)
		initial_data_length = len(packets_data)

		if encrypt:
			packets_data = self.cipher_aes.encrypt(packets_data)

		prefix = prefix_struct.pack(initial_data_length, 0x01 if encrypt else 0x00)
		# TODO exceptions handling
		self.connection.send_data(prefix + packets_data)
		print('Packet sent:')
		print(type(packet.fields).__name__)


	def receive_session_key(self):
		rcv_packet = self.parse_packet()
		if not isinstance(rcv_packet, PacketKEY):
			raise TypeError('Wrong packet received')

		encrypted_symmetric_key = rcv_packet.fields.symmetric_key

		self.cipher_aes.set_key(self.cipher_rsa.decrypt(encrypted_symmetric_key))
		print('Symmetric key received')

	def send_values(self, services_list):
		# send values read from all the services
		for service in services_list:
			val_packet = PacketVAL.create(service.id, service.get_value(), int(time.time()))
			print("value: {}".format(service.id))
			self.send_packet(val_packet, encrypt=True)
		# after all values has been sent, send EOT packet
		self.send_packet(PacketEOT.create(), encrypt=True)

	def send_descriptors(self, services_list):
		for service in services_list:
			# send service description
			desc_packet = PacketDESC.create(service.service_class,
											service.name,
											service.unit,
											service.min_value,
											service.max_value)
			self.send_packet(desc_packet, encrypt=True)

			rcv_packet = self.parse_packet()
			if isinstance(rcv_packet, PacketNAK):
				raise RuntimeError('Service: {} rejected by the server'.format(service.name))

			if not isinstance(rcv_packet, PacketACK):
				raise RuntimeError('Wrong packet received')

			service.set_id(rcv_packet.fields.service_id)
			print("Service: {} registered succesfully received nr: {}".format(service.name, service.id))

		self.send_packet(PacketEOT.create(), encrypt=True)