import unittest
from rle_decoder import RLEDecoder
from rle_encoder import RLEEncoder


class TestRLEDecoder(unittest.TestCase):
    def test_init(self):
        rle = RLEDecoder(bytearray(b''))
        self.assertIsInstance(rle.data, bytearray)
        self.assertIsInstance(rle.result, bytearray)

    def test_decode(self):
        data = bytearray(b'zhzhzhhhh')
        encoder = RLEEncoder(data)
        res = encoder.encode()
        decoder = RLEDecoder(res)
        dec = decoder.decode()
        self.assertEqual(data, dec)


if __name__ == '__main__':
    unittest.main()
