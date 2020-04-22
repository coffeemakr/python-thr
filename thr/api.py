from .messages import Message, TextMessage
from .cache import InMemoryCache
import requests
import urllib.parse
import libnacl.public

def _url_join(base_url, *parts):
    return base_url + '/'.join(map(urllib.parse.quote, parts))

class Threema:
    def __init__(self, identity: str, secret, key, base_url="https://msgapi.threema.ch/", cache=None):
        if cache is None:
            cache = InMemoryCache()
        self.cache = cache 

        key = bytes.fromhex(key)
        if len(identity) != 8:
            raise ValueError("identity must be 8 characters long")
        self.identity = identity
        self.secret = secret
        self.key = libnacl.public.SecretKey(key)
        self.base_url = base_url

    def _query(self, method, *url_parts, **kwargs):
        url = _url_join(self.base_url, *url_parts)   
        respone = requests.request(method, url, **kwargs)
        print(respone.text)
        respone.raise_for_status()
        return respone

    def lookup_pubkey(self, identity: str) -> bytes:
        if len(identity) != 8:
            raise ValueError("identity must be 8 characters long")
        response = self._query("GET", 'pubkeys', identity, params={
            'from': self.identity, 
            'secret': self.secret
        })
        return bytes.fromhex(response.text)

    def get_pubkey(self, identity: str) -> bytes:
        return self.cache.get_or_call(identity, self.lookup_pubkey)

    def send_message(self, message: Message, recipient: str):
        '''
        Send a message
        '''
        public_key = self.get_pubkey(recipient)
        encrypted = message.encrypt_for(our_secret=self.key, their_public=public_key)
        response = self._query("POST", "send_e2e", data={
            'nonce': encrypted.nonce.hex(),
            'box': encrypted.data.hex(),
            'secret': self.secret,
            'from': self.identity,
            'to': recipient
        }, headers={
            'Content-Type': 'application/x-www-form-urlencoded'
        })
        return response.text

    def send_text_message(self, recipient: str, content: str):
        message = TextMessage(content)
        return self.send_message(
            message=message,
            recipient=recipient)