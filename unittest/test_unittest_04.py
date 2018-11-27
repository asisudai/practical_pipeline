#!/usr/bin/env python
import unittest
import tempfile
import os
import shutil

class TestCaseExample(unittest.TestCase):

    def setUp(self):
        '''Create a temporary directory, before each test start'''
        self.temp_folder = tempfile.mkdtemp()

    def tearDown(self):
        '''Remove the temporary directory, after each test finish'''
        shutil.rmtree(self.temp_folder)

    def test_one(self):
        '''Create a temporary file in our temp_folder'''
        target = create_file(self.temp_folder)

        # Confirm that the target file exists:
        self.assertTrue(os.path.isfile(target))

        # Confirm the target content:
        with open(target, 'r') as fs:
            data = fs.read()

        self.assertEqual(data, 'to test or not to test')

def create_file(root):
    '''Create a file in given root'''
    target = os.path.join(root, 'test_file.txt')
    with open(target, 'w') as fs:
        fs.write('to test or not to test')
    return target

if __name__ == '__main__':
    unittest.main()
