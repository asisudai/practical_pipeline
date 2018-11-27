#!/usr/bin/env python
'''
Run unittest within mayapy environment.

usage:

    # Run all tests
    mayapy  ../test_unittest_maya_runner.py
'''
import unittest

if __name__ == '__main__':

    # Initialize Maya
    import maya.standalone
    maya.standalone.initialize('python')

    # Find all tests in and under current directory
    root = os.path.dirname(__file__)
    pattern = 'test*.py'

    loader = unittest.TestLoader().discover(root, pattern=pattern)
    suite = unittest.TestSuite()

    if loader.countTestCases():
        suite.addTests(loader)

    runner = unittest.TextTestRunner(verbosity=3)
    runner.run(suite)

    # Uninitialize Maya
    maya.standalone.uninitialize()
