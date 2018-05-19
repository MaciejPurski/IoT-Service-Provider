#!/usr/bin/python3.6

import unittest

from AESTestFixture import AESTestCase

def suite():
	suite = unittest.TestSuite()
	suite.addTest(AESTestCase('test_short_msg'))
	suite.addTest(AESTestCase('test_random_long_msgs'))

	return suite

if __name__ == '__main__':
	runner = unittest.TextTestRunner()
	runner.run(suite())