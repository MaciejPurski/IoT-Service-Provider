#!/usr/bin/python3.6

from CryptoCore import *


cipher = CipherRSA('server-public.pem', 'server-private.pem')

msg = b'HWDP JP 100%!'

signature = cipher.sign(msg)

print(cipher.verify(msg, signature))
print(len(signature))
