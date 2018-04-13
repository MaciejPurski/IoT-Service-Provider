import SocketLayer
import Packets
import socket
import sys
from Packets import packet_factory
from CryptoCore import CipherRSA


class Protocol:
	def __init__(self, server_ip, port, public_key, private_key):
		self.cipher_rsa = CipherRSA(public_key, private_key)
		self.connection = SocketLayer.Connection(server_ip, port)

	def authenticate(self):
		# TODO handle error
		rcv_packet = self.connection.packet_read(False)
		if not isinstance(rcv_packet, Packets.PacketCHALL):
			raise TypeError('wrong packet received')

		encrypted_bytes = CipherRSA.encrypt_rsa(rcv_packet.random_bytes())
		chall_resp = packet_factory(Packets.PacketType.CHALL_RESP)
		chall_resp.set_fields(encrypted_bytes)

		self.connection.packet_send(chall_resp, False)
		


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