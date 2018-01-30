# -*- coding: utf-8 -*-
import requests
import unittest

HOST = 'localhost:8000'

class IndexTest(unittest.TestCase):

    def index_test(self):
        uri = '/api/blogs'
        res = requests.get(HOST+uri)
        self.assertEqual(200, res.status_code)


if __name__ == '__main__':
    unittest.main()

