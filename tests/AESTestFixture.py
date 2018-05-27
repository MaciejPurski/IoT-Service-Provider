#!/usr/bin/python3.6

import unittest

from Crypto import Random
from communication.CryptoCore import *
import random


class AESTestCase(unittest.TestCase):
	def setUp(self):
		key = get_random_bytes(block_size_AES)
		self.cipher = CipherAES()
		self.cipher.set_key(key)

	def test_short_msg(self):
		msg = b'abcdef'
		in_file = open('in', 'wb')
		in_file.write(msg)
		in_file.close()

		encrypted = self.cipher.encrypt(msg)
		encr_file = open('encrypted', 'wb')
		encr_file.write(encrypted)
		encr_file.close()
		decrypted = self.cipher.decrypt(encrypted)

		self.assertEqual(msg, decrypted)
		self.assertEqual(len(encrypted), block_size_AES + len(CipherAES.pad(msg)))

	def test_random_long_msgs(self):
		random.seed()
		for i in range(0, 100):
			length = random.randint(32, 1024)
			msg = Random.new().read(length)

			encrypted = self.cipher.encrypt(msg)
			decrypted = self.cipher.decrypt(encrypted)

			self.assertEqual(msg, decrypted)
			self.assertEqual(len(encrypted), block_size_AES + len(CipherAES.pad(msg)))


if __name__ == '__main__':
	unittest.main()
