from pyzbar.pyzbar import decode
from PIL import Image


def decode_qr_code():
    # Open image
    image_path = "example.png"

    image = Image.open(image_path)
    # Decode QR code
    decoded_objects = decode(image)
    if decoded_objects:
        # Print each decoded object
        for obj in decoded_objects:
            print(f"Data: {obj.data.decode('utf-8')}")
            return obj.data.decode("utf-8")
    else:
        print("No QR code found")


# decode_qr_code()
