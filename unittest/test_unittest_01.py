#!/usr/bin/env python
import unittest

class TestMath(unittest.TestCase):

    def test_one(self):
        # assertEqual will fail if 1+1 != 2
        self.assertEqual(1+1, 2)

    def test_two(self):
        # assertTrue will fail if 1 is False
        self.assertTrue(1)
        # assertTrue will fail if 0 is True
        self.assertFalse(0)

if __name__ == '__main__':
    unittest.main()
