#!/usr/bin/env python
import unittest

class TestFailure(unittest.TestCase):

    def test_one(self):
        '''Test assert Equal'''
        # assertEqual will fail if 1+1 != 2
        self.assertEqual(1+1, 2)

    def test_two(self):
        '''Test assert True/False'''
        # assertTrue will fail if 1 is False
        self.assertTrue(1)
        # assertTrue will fail if 0 is True
        self.assertFalse(0)

    def test_failure(self):
        """This test will fail and that's ok"""
        self.assertFalse(True)

if __name__ == '__main__':
    unittest.main()
