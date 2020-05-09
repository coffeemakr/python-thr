from libnacl.public import Box, PublicKey, SecretKey
from libnacl import crypto_box_NONCEBYTES, crypto_box_SECRETKEYBYTES, crypto_secretbox
import libnacl.utils
import libnacl.sealed
from collections import namedtuple

EncryptedBox = namedtuple("EncryptedBox", ["nonce", "data"])
SymmetricEncryptedData = namedtuple("SymmetricEncryptedData", ["key", "data"])

NONCE_LENGTH = crypto_box_NONCEBYTES
SYMMETRIC_KEY_LENGTH = crypto_box_SECRETKEYBYTES

# Predefined nonces (I know right?)
VIDEO_NONCE = (b'\x00' * 23) + b'\x01'
FILE_NONCE = (b'\x00' * 23) + b'\x01'
THUMBNAIL_NONCE = (b'\x00' * 23) + b'\x02'


def box_encrypt(content: bytes, secret_key: SecretKey, public_key: PublicKey) -> EncryptedBox:
    if isinstance(public_key, bytes):
        public_key = libnacl.public.PublicKey(public_key)
    if isinstance(secret_key, bytes):
        secret_key = libnacl.public.SecretKey(secret_key)
    box = libnacl.public.Box(sk=secret_key, pk=public_key)
    # Encrypt messages
    nonce, data = box.encrypt(content, pack_nonce=False)
    return EncryptedBox(nonce=nonce, data=data)


def encrypt_with_nonce(content: bytes, nonce: bytes, key=None):
    if len(nonce) != NONCE_LENGTH:
        raise ValueError(
            f"Invalid nonce size. Got {len(nonce)}, but expected {NONCE_LENGTH}")
    if key is None:
        key = libnacl.utils.salsa_key()
    box = libnacl.secret.SecretBox(key=key)
    _, data = box.encrypt(content, nonce=nonce, pack_nonce=False)
    return SymmetricEncryptedData(key=key, data=data)

def encrypt_file(content: bytes, **kwargs) -> SymmetricEncryptedData:
    return encrypt_with_nonce(content=content, nonce=FILE_NONCE, **kwargs)

def encrypt_thumbnail(content: bytes, **kwargs):
    return encrypt_with_nonce(content=content, nonce=THUMBNAIL_NONCE, **kwargs)

def encrypt_video(content: bytes, **kwargs):
    return encrypt_with_nonce(content=content, nonce=VIDEO_NONCE, **kwargs)
