import sys
from ProtocolLayer import Protocol

if len(sys.argv) != 5:
	print("not enough arguments")
	sys.exit(1)

protocol = Protocol(*sys.argv[1:])
