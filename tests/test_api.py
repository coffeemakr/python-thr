import unittest
from thr.api import Threema
from thr.api import SecretKey
from libnacl.utils import salsa_key
import binascii

class TestApi(unittest.TestCase):
    
    def test_constructor_from_object_secret(self):
        binary_key = b'q{\x1f\xb0\xf3\xe6\x88\x84T\xf2\x1a\x01,\xeck\xe6\x18\x1a0\x8c\xe8\x9fJs8i\x84\x8f\xd6\xedt\xbb'
        key = SecretKey(binary_key)
        api = Threema(identity="*ABCDEFG", key=key, secret='0' * 16)
        self.assertEqual(api.identity, "*ABCDEFG")
        self.assertEqual(api.key.pk, key.pk)

    def test_constructor_from_binary_secret(self):
        binary_key = b'q{\x1f\xb0\xf3\xe6\x88\x84T\xf2\x1a\x01,\xeck\xe6\x18\x1a0\x8c\xe8\x9fJs8i\x84\x8f\xd6\xedt\xbb'
        key = SecretKey(binary_key)
        api = Threema(identity="*ABCDEFG", key=binary_key, secret='0' * 16)
        self.assertEqual(api.identity, "*ABCDEFG")
        self.assertEqual(api.key.pk, key.pk)

    def test_constructor_from_hex_secret(self):
        binary_key = b'q{\x1f\xb0\xf3\xe6\x88\x84T\xf2\x1a\x01,\xeck\xe6\x18\x1a0\x8c\xe8\x9fJs8i\x84\x8f\xd6\xedt\xbb'
        hex_key = "717b1fb0f3e6888454f21a012cec6be6181a308ce89f4a733869848fd6ed74bb"
        key = SecretKey(binary_key)
        api = Threema(identity="*ABCDEFG", key=hex_key, secret='0' * 16)
        self.assertEqual(api.identity, "*ABCDEFG")
        self.assertEqual(api.key.pk, key.pk)
