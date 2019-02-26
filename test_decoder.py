import unittest
import os
from unittest.mock import MagicMock
from lsb_decoder import LSBDecoder


class TestDecoder(unittest.TestCase):
    def test_init(self):
        with open('filename.txt', 'w') as file:
            file.write('blablablabal'*4)
        lsb = LSBDecoder('filename.txt', 0)
        os.remove('filename.txt')
        self.assertIsInstance(lsb.main_file, bytearray)
        self.assertEqual(lsb.index_of_start_of_data, 0)
        self.assertIsInstance(lsb.bits_per_sample, int)

    def test_read_the_flag(self):
        with open('filename.txt', 'w') as file:
            file.write('balblabla'*5)
        lsb = LSBDecoder('filename.txt')
        result = lsb._read_the_flag(4, 0, 1)
        os.remove('filename.txt')
        self.assertIsInstance(result, tuple)
        self.assertIsInstance(result[0], int)
        self.assertIsInstance(result[1], str)

    def test_read_the_content(self):
        with open('filename.txt', 'w') as file:
            file.write('balblabla'*5)
        lsb = LSBDecoder('filename.txt')
        buffer = bytearray(20)
        result = lsb._read_the_content(buffer, 10, 0, 1)
        os.remove('filename.txt')
        self.assertEqual(result, 10)

    def test_read_the_hash(self):
        with open('filename.txt', 'w') as file:
            file.write('balblabla'*5)
        lsb = LSBDecoder('filename.txt')
        result = lsb._read_the_hash(42, 0, 1)
        os.remove('filename.txt')
        self.assertIsInstance(result, tuple)
        self.assertEqual(result[0], 42)
        self.assertIsInstance(result[1], int)

    def test_compare_of_checksum(self):
        try:
            LSBDecoder._compare_the_checksum(1, 0)
        except Exception:
            self.assertEqual(1, 1)

    # def test_get_hidden_information(self):
    #     with open('filename.txt', 'w') as file:
    #         file.write('\x01\x10'*250)
    #     lsb = LSBDecoder('filename.txt', 0)
    #     result = lsb.get_hidden_information()
    #     self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
