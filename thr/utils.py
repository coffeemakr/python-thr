import hmac

EMAIL_HMAC_KEY = b'0\xa5P\x0f\xed\x97\x01\xfam\xef\xdba\x08A\x90\x0f\xeb\xb8\xe40\x88\x1fz\xd8\x16\x82bd\xec\t\xba\xd7'

PHONE_HMAC_KEY = bytes.fromhex("85adf8226953f3d96cfd5d09bf29555eb955fcd8aa5ec4f9fcd869e258370723")

def hash_email(email: str):
    '''
    Hashes an e-mail for reverse lookup.

    >>> hash_email("Test@Threema.ch")
    1ea093239cc5f0e1b6ec81b866265b921f26dc4033025410063309f4d1a8ee2c
    '''
    return hmac.digest(
        key=EMAIL_HMAC_KEY, 
        msg=email.strip().lower(), 
        digestmod="sha256")

def hash_phone(phone):
    '''

    >>> hash_phone("41791234567")
    85adf8226953f3d96cfd5d09bf29555eb955fcd8aa5ec4f9fcd869e258370723
    '''
    return hmac.digest(
        key=EMAIL_HMAC_KEY, 
        msg=phone, 
        digestmod="sha256")
