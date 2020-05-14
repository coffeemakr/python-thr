import hmac

EMAIL_HMAC_KEY = b'0\xa5P\x0f\xed\x97\x01\xfam\xef\xdba\x08A\x90\x0f\xeb\xb8\xe40\x88\x1fz\xd8\x16\x82bd\xec\t\xba\xd7'
PHONE_HMAC_KEY = b'\x85\xad\xf8"iS\xf3\xd9l\xfd]\t\xbf)U^\xb9U\xfc\xd8\xaa^\xc4\xf9\xfc\xd8i\xe2X7\x07#'


def hash_email(email: str):
    '''
    Hashes an e-mail for reverse lookup.

    >>> hash_email("Test@Threema.ch")
    1ea093239cc5f0e1b6ec81b866265b921f26dc4033025410063309f4d1a8ee2c
    '''
    return hmac.digest(
        key=EMAIL_HMAC_KEY,
        msg=email.strip().lower().encode("ascii"),
        digest="sha256").hex()


def hash_phone(phone):
    '''

    >>> hash_phone("41791234567")
    ad398f4d7ebe63c6550a486cc6e07f9baa09bd9d8b3d8cb9d9be106d35a7fdbc
    '''
    return hmac.digest(
        key=PHONE_HMAC_KEY,
        msg=phone.encode("ascii"),
        digest="sha256").hex()
