import pathlib
import sys
root = pathlib.Path(__file__).parent.parent.absolute()
sys.path.insert(0, str(root))

import thr

def send_text(recipient):
    '''
    Send a predefined text message to the recipient.
    '''
    threema = thr.Threema.from_environment()
    contact = threema.lookup(recipient)
    threema.send_text_message(content="Hello!", recipient=contact)


if __name__ == "__main__":
    recipient = input("recipient: ")
    send_text(recipient)
