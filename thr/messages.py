import struct
import secrets
from typing import Tuple
from .crypto import box_encrypt, Box

def generate_padding():
    n = secrets.randbelow(256)
    padding = n.to_bytes(1, byteorder='big')
    return padding * n

class Message:
    def to_bytes(self) -> bytes:
        raise NotImplementedError("as_bytes")

    def encrypt_for(self, our_secret: bytes, their_public: bytes) -> Box:
        return box_encrypt(
            content=self.to_bytes(), 
            our_secret=our_secret, 
            their_public=their_public)
        

class TextMessage(Message):
    def __init__(self, content: str):
        self.content = content

    def to_bytes(self) -> bytes:
        content = self.content.encode('utf-8')
        if len(content) > 3500:
            raise ValueError("content may only be 3500 UTF-8 bytes long")
        return b'\x01' + content + generate_padding()
