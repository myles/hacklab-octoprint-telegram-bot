#!/usr/bin/env python

import unittest

import utils


class TestUtils(unittest.TestCase):

    def setUp(self):
        self.seconds_to_human = utils.seconds_to_human

    def test_seconds_to_human(self):
        self.assertEqual(self.seconds_to_human(1), '1 second')
        self.assertEqual(self.seconds_to_human(20), '20 seconds')
        self.assertEqual(self.seconds_to_human(60), '1 minute')
        self.assertEqual(self.seconds_to_human(20*20), '6 minutes 40 seconds')


if __name__ == '__main__':
    unittest.main()
