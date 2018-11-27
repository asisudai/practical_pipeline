#!/usr/bin/env python
import unittest

class TestCaseExample(unittest.TestCase):

    def setUp(self):
        # Optional function. Called before each test_ function is run.
        # Useful to set-up the environment for the test.
        # For example, create a temporary folder.
        pass

    def tearDown(self):
        # Optional function. Called after each test_ function is run.
        # Useful to tear-down the environment of the test.
        # For example, remove a temporary folder.
        pass

    def test_one(self):
        # a test function.
        # for example, testing random int is less then 10
        import random
        self.assertLess(random.randint(1,5), 10 )

    def test_two(self):
        # another test function.
        # for example, testing 'hello' == 'hello'
        value = u'hello'
        self.assertEqual(value, u'hello')
        self.assertNotEqual(value, u'goodbye')

if __name__ == '__main__':
    unittest.main()
