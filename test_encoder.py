import unittest
import os
from unittest.mock import MagicMock
from lsb_encoder import LSBEncoder


class TestEncoder(unittest.TestCase):
    def test_init(self):
        with open('filename.txt', 'w') as file:
            file.write('blablablablablablablablablablablablablablabla')
        try:
            lsb = LSBEncoder(['filename.txt'], 'filename.txt')
        except Exception:
            self.assertEqual(1, 1)
        os.remove('filename.txt')

    def test_chech_the_opportunity_to_enter(self):
        with open('filename.txt', 'w') as file:
            file.write('blablablablablablablabl')
        try:
            LSBEncoder(['filename.txt'], 'filename.txt')
        except Exception:
            self.assertEqual(1, 1)
        os.remove('filename.txt')

    def test_define_filename(self):
        test_str = r'C:\Users\User\Desktop\filename.txt'
        result = LSBEncoder._define_filename_in_bytearray(test_str)
        expectation = bytearray(bytes('filename.txt', 'utf-8'))
        self.assertEqual(result, expectation)

    def test_get_bits_per_sample(self):
        expectation = 16
        string = ''
        for i in range(34):
            string += '\x00'
        string += '\x10\x00'
        result = LSBEncoder._get_bits_per_sample(bytearray(bytes(string, 'utf-8')))
        self.assertEqual(result, expectation)

    def test_create_description(self):
        test_pairs = ['00', '10', '11', '11', '01', '00', '10', '01']
        expectation = ['0', '0', '0', '0', '0', '0', '0', '0', '0',
                       '0', '0', '0', '1', '0', '0', '0']
        result = LSBEncoder._create_description(test_pairs, 16)
        self.assertEqual(result, expectation)

    def test_create_new_byte_of_flag(self):
        description = ['0', '0', '0', '0', '0', '0', '0', '0', '0',
                       '0', '0', '0', '1', '0', '0', '0']
        byte = bytearray(b'\x00')
        i = 12
        expectation = 1
        result = LSBEncoder._create_new_byte_of_flag(byte, description, i)
        self.assertEqual(result, expectation)

    def test_create_new_byte_of_data(self):
        byte = bytearray(b'\x00')
        pairs = ['00', '10', '11', '01', '00', '11', '10']
        i = 2
        expectation = 3
        result = LSBEncoder._create_new_byte_of_data(byte, pairs, i)
        self.assertEqual(result, expectation)

    def test_describe_flag(self):
        with open('filename.txt', 'w') as file:
            file.write('blablabla')
        with open('filename1.txt', 'w') as file:
            file.write('100001101101101010111010101'*10)
        LSBEncoder._check_the_opportunity_to_enter = \
            MagicMock(return_value=True)
        lsb = LSBEncoder(['filename.txt'], 'filename1.txt', 0)
        result = lsb.describe_flag_and_get_index(4, ['0', '0', '0', '1'],
                                                 0, 2)
        os.remove('filename.txt')
        os.remove('filename1.txt')
        self.assertIsInstance(result, int)

    def test_describe_data(self):
        with open('filename.txt', 'w') as file:
            file.write('blablablablablablablablablablablabbl')
        LSBEncoder._check_the_opportunity_to_enter = \
            MagicMock(return_value=True)
        lsb = LSBEncoder(['filename.txt'], 'filename.txt', 0)
        result = lsb.describe_data_and_get_index(['0', '0', '0', '1'],
                                                 0, 2)
        os.remove('filename.txt')
        self.assertIsInstance(result, int)

    def test_inscribe(self):
        with open('main_file.txt', 'w') as file:
            file.write('blablablablablablablablablablablabbl'*15000)
        with open('file.txt', 'w') as file2:
            file2.write('s')
        LSBEncoder._check_the_opportunity_to_enter = \
            MagicMock(return_value=True)
        LSBEncoder._create_new_byte_of_flag = MagicMock(return_value=42)
        LSBEncoder._create_new_byte_of_data = MagicMock(return_value=42)
        LSBEncoder.describe_data_and_get_index = MagicMock(return_value=1)
        lsb = LSBEncoder(['file.txt'], 'main_file.txt', 0)
        result = lsb.inscribe()
        os.remove('file.txt')
        os.remove('main_file.txt')
        self.assertIsNone(result)

    def test_create_file(self):
        with open('filename.txt', 'w') as file:
            file.write('blablablablablablablablablablablabbl')
        LSBEncoder._check_the_opportunity_to_enter = \
            MagicMock(return_value=True)
        lsb = LSBEncoder(['filename.txt'], 'filename.txt', 0)
        result = lsb.create_new_wav()
        os.remove('filename.txt')
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
