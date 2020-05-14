import unittest
from thr.messages import TextMessage

class MessageTest(unittest.TestCase):
    def test_text_message(self):
        message = TextMessage("hello threema")
        self.assertEqual(b'\x01hello threema\x07\x07\x07\x07\x07\x07\x07', message.to_bytes(padding_length=7))
