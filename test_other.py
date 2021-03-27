import unittest

class Tests(unittest.TestCase):
    def test_dummy(self):
        self.assertEqual(1, 1)

    def test_dummy_also(self):
        self.assertNotEqual(2, 1)

if __name__ == '__main__':
    unittest.main()
