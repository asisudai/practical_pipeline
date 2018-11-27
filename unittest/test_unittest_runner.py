#!/usr/bin/env python
import unittest

# import your test modules
import test_unittest_01
import test_unittest_02
import test_unittest_03
import test_unittest_04

if __name__ == '__main__':

    # initialize the test suite
    loader = unittest.TestLoader()
    suite  = unittest.TestSuite()

    # add tests to the test suite
    suite.addTests(loader.loadTestsFromModule(test_unittest_01))
    suite.addTests(loader.loadTestsFromModule(test_unittest_02))
    suite.addTests(loader.loadTestsFromModule(test_unittest_03))
    suite.addTests(loader.loadTestsFromModule(test_unittest_04))

    # initialize a runner, pass it your suite and run it
    runner = unittest.TextTestRunner(verbosity=3)
    result = runner.run(suite)
