import pathlib
import sys
root = pathlib.Path(__file__).parent.parent.absolute()
sys.path.insert(0, str(root))

import thr

def send_image(recipient):
    '''
    The image.jpg from the data directory to the recipient.

    The thumbnail.jpg is used as the thumbnail for the file message.
    '''
    data_dir = pathlib.Path(__file__).parent / "data"

    threema = thr.Threema.from_environment()
    # Upload the file
    message = threema.upload_file(data_dir /  "image.jpg")

    # Upload the thumbnail
    with open(data_dir / "thumbnail.jpg", "rb") as thumnail_file:
        thumbnail_content = thumnail_file.read()
    message.thumbnail_blob_id = threema.upload_thumbnail(
        thumbnail_content, key=message.key)

    contact = threema.lookup(recipient)

    threema.send_message(
        message=message,
        recipient=contact)


if __name__ == "__main__":
    recipient = input("recipient: ")
    send_image(recipient)
