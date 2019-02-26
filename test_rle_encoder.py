import unittest
from collections import deque
from rle_encoder import RLEEncoder


class TestRLEEncoder(unittest.TestCase):
    def test_init(self):
        data = bytearray(b'aaazaaa')
        rle = RLEEncoder(data)
        self.assertIsInstance(rle.result_data, bytearray)
        self.assertIsInstance(rle.data_to_encode, bytearray)

    def test_review_the_same_bytes(self):
        rle = RLEEncoder(bytearray(b''))
        result = rle.review_the_same_bytes(256, 12)
        self.assertIsInstance(result, int)

    def test_review_diff_bytes(self):
        rle = RLEEncoder(bytearray(b''))
        deq = deque()
        for i in range(200):
            deq.append(1)
        result = rle.review_diff_bytes(deq)
        self.assertIsInstance(result, deque)

    def test_encode(self):
        data = bytearray(b'sssasassssaaaassasa')
        rle = RLEEncoder(data)
        res = rle.encode()
        self.assertIsInstance(res, bytearray)

    def test_encode_again(self):
        data = bytearray(b'sas')
        rle = RLEEncoder(data)
        res = rle.encode()
        self.assertIsInstance(res, bytearray)


if __name__ == '__main__':
    unittest.main()
