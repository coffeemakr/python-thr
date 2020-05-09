import struct
import secrets
from typing import Tuple
import json
from .crypto import NONCE_LENGTH, SYMMETRIC_KEY_LENGTH

def generate_padding():
    n = secrets.randbelow(256)
    padding = n.to_bytes(1, byteorder='big')
    return padding * n


class Message:

    type_byte: bytes

    def get_data(self) -> bytes:
        raise NotImplementedError()

    def to_bytes(self) -> bytes:
        return self.type_byte + self.get_data() + generate_padding()


class TextMessage(Message):
    type_byte = b'\x01'

    def __init__(self, content: str):
        self.content = content

    def get_data(self) -> bytes:
        data = self.content.encode('utf-8')
        if len(data) > 3500:
            raise ValueError("content may only be 3500 UTF-8 bytes long")
        return data

def _require_size(name, value, size):
    if len(value) != size:
        raise ValueError(f"{name} needs size of {size}")
    return value

class ImageMessage(Message):

    type_byte = b'\x02'

    def __init__(self, blob_id: str, size: int, nonce: bytes):
        self.blob_id = blob_id
        self.size = size
        self.nonce = nonce

    def get_data(self) -> bytes:
        data = self.blob_id.encode('ascii') + self.size.to_bytes(4, "big") + self.nonce
        if len(data) != 44:
            raise ValueError("Size of data is not 44 it's " + len(data))
        return data

class FileMessage(Message):

    type_byte = b'\x17'

    def __init__(self, blob_id: bytes, size: int, key: bytes, mime_type: str, filename: str = None, thumbnail_blob_id=None, description=None):
        self.blob_id = blob_id
        self.size = size
        self.key = _require_size("key", key, SYMMETRIC_KEY_LENGTH)
        self.mime_type = mime_type
        self.filename = filename
        self.thumbnail_blob_id = thumbnail_blob_id
        self.description = description
    
    def get_data(self) -> bytes:
        value = {
            'b': self.blob_id.hex(),
            'k': self.key.hex(),
            'm': self.mime_type,
            's': self.size,
            'i': 0
        }

        if self.description is not None:
            value['d'] = self.description
        
        if self.filename is not None:
            value['n'] = self.filename
        
        if self.thumbnail_blob_id is not None:
            value['t'] = self.thumbnail_blob_id.hex()
        result = json.dumps(value, separators=(',', ':')).encode('utf-8')
        print(result)
        return result