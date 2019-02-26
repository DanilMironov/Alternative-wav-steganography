import unittest
import os
from lsb_stuff import LSBStuff


class TestStuff(unittest.TestCase):
    def test_find_index_of_data(self):
        test_list = bytearray(bytes('купил мужик шляпу', 'utf-8'))
        result = LSBStuff.find_index_of_the_start_of_data(test_list)
        self.assertEqual(result, 7)

    def test_read_the_file(self):
        with open('filename.txt', 'w') as file:
            file.write('blablabla')
        result = LSBStuff.read_the_file('filename.txt')
        os.remove('filename.txt')
        self.assertIsInstance(result, bytearray)

    def test_bin_str_from_bytearray(self):
        test_array = bytearray(bytes('а она ему', 'utf-8'))
        result = LSBStuff.get_bin_str_from_bytearray(test_array)
        self.assertIsInstance(result, str)

    def test_get_hash(self):
        test_array = bytearray(bytes('как раз', 'utf-8'))
        result = LSBStuff.get_hash(test_array)
        self.assertIsInstance(result, int)

    def test_get_hash_again(self):
        test_array = bytearray(b'0')
        result = LSBStuff.get_hash(test_array)
        self.assertIsInstance(result, int)

    def test_get_bin_from_int(self):
        byte = 5
        result = LSBStuff.get_bin_from_int(byte)
        self.assertEqual(result, '00000101')

    def test_split_string_into_chars(self):
        test_string = '01001010'
        result = LSBStuff.split_the_string_into_chars(test_string)
        expectation = ['0', '1', '0', '0', '1', '0', '1', '0']
        self.assertEqual(result, expectation)

    def test_split_into_two_bits(self):
        test_string = '01001010'
        result = LSBStuff.split_in_two_bits(test_string)
        expectation = ['01', '00', '10', '10']
        self.assertEqual(result, expectation)

    def test_get_int_from_bin(self):
        bin_string = '00001010'
        result = LSBStuff.get_int_from_bin(bin_string)
        self.assertEqual(result, 10)


if __name__ == '__main__':
    unittest.main()
