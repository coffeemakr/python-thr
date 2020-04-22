import libnacl.public
import libnacl.sealed
nonce = libnacl.utils.rand_nonce()
from collections import namedtuple

Box = namedtuple("Box", ["nonce", "data"])

def box_encrypt(content: bytes, our_secret: bytes, their_public: bytes) -> Box:
    if isinstance(their_public, bytes):
        their_public = libnacl.public.PublicKey(their_public)
    if isinstance(our_secret, bytes):
        our_secret = libnacl.public.SecretKey(our_secret)
    box = libnacl.public.Box(sk=our_secret, pk=their_public)
    # Encrypt messages
    nonce, data = box.encrypt(content, pack_nonce=False)
    return Box(nonce=nonce, data=data)