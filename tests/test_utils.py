from thr.utils import hash_email, hash_phone
import unittest


class TestUtils(unittest.TestCase):
    def test_hash_phone(self):
        digest = hash_phone("41791234567")
        expected = "ad398f4d7ebe63c6550a486cc6e07f9baa09bd9d8b3d8cb9d9be106d35a7fdbc"
        self.assertEqual(digest, expected)

    def test_hash_email(self):
        digest = hash_email("Test@Threema.ch")
        expected = "1ea093239cc5f0e1b6ec81b866265b921f26dc4033025410063309f4d1a8ee2c"
        self.assertEqual(digest, expected)
