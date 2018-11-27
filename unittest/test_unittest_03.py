#!/usr/bin/env python
import unittest

class TestFunctions(unittest.TestCase):

    def test_function_fail(self):
        function_fail()

    def test_function_true(self):
        result = function_return_true()
        self.assertEqual(result, True)
        self.assertTrue(result)
        self.assertIsInstance(result, bool)

def function_fail():
    # this function is sure to fail
    0/0
    return True

def function_return_true():
    return True

if __name__ == '__main__':
    unittest.main()
