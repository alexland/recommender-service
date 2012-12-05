#!/usr/local/bin/python
# encoding: utf-8


import os
import flaskr
import unittest
import tempfile

"""
even before config params are set, this test module can still be run
to check that this module is syntactically valid
"""


class FlaskrTestCase(unittest.TestCase):

	def setUp(self):
		self.db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
		flaskr.app.config['TESTING'] = True
		self.app = flaskr.app.test_client()
		flaskr.init_db()

	def tearDown(self):
		os.close(self.db_fd)
		os.unlink(flaskr.app.config['DATABASE'])
		
		
		
if __name__ == '__main__':
	unittest.main()