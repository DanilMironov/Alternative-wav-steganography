import unittest
from main import Main


class TestMain(unittest.TestCase):
    def test_parse_args(self):
        parser = Main.parse_args(['-en', '-dec'])
        self.assertTrue(parser.encode)


if __name__ == '__main__':
    unittest.main()
