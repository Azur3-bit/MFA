from pyfingerprint.pyfingerprint import PyFingerprint

def enroll_fingerprint():
    # Initialize fingerprint sensor
    try:
        f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)
        if not f.verifyPassword():
            raise ValueError('The given fingerprint sensor password is wrong!')

    except Exception as e:
        print('Exception message: ' + str(e))
        return False

    # Wait for a finger to be read
    print('Waiting for finger...')

    while not f.readImage():
        pass

    # Convert read image to characteristics and store it
    f.convertImage(0x01)
    print('Remove finger...')
    time.sleep(2)

    print('Place the same finger again...')

    while not f.readImage():
        pass

    # Convert read image to characteristics and store it
    f.convertImage(0x02)

    # Create a template
    f.createTemplate()

    # Save template to file
    template = f.downloadCharacteristics()

    with open('fingerprint_template.bin', 'wb') as file:
        file.write(template)

    print('Fingerprint enrolled successfully.')
    return True

def verify_fingerprint():
    # Initialize fingerprint sensor
    try:
        f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)
        if not f.verifyPassword():
            raise ValueError('The given fingerprint sensor password is wrong!')

    except Exception as e:
        print('Exception message: ' + str(e))
        return False

    # Wait for a finger to be read
    print('Waiting for finger...')

    while not f.readImage():
        pass

    # Convert read image to characteristics and store it
    f.convertImage(0x01)

    # Search for a match
    result = f.searchTemplate()
    positionNumber = result[0]

    if positionNumber == -1:
        print('No match found.')
        return False
    else:
        print('Fingerprint matched with position number: ', positionNumber)
        return True

# Example usage:
# Enroll fingerprint
enroll_fingerprint()

# Verify fingerprint
verify_fingerprint()
