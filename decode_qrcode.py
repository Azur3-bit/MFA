from pyzbar.pyzbar import decode
from PIL import Image

def decode_qr_code(image_path):
    # Open image
    image = Image.open(image_path)
    # Decode QR code
    decoded_objects = decode(image)
    if decoded_objects:
        # Print each decoded object
        for obj in decoded_objects:
            print(f"Data: {obj.data.decode('utf-8')}")
    else:
        print("No QR code found")

image_path = "example.png"
decode_qr_code(image_path)
