import os
import winbio

def enroll_fingerprint():
    try:
        session = winbio.open_session(winbio.WINBIO_TYPE_FINGERPRINT)
        print("Place your finger on the sensor for enrollment...")
        result = session.enroll_begin()
        if result != winbio.ERROR_SUCCESS:
            print("Failed to start enrollment.")
            return False
        
        while True:
            result, unit_id, reject_detail = session.capture_sample(winbio.WINBIO_NO_PURPOSE_AVAILABLE)
            if result == winbio.ERROR_SUCCESS:
                print("Sample captured successfully.")
                break
            elif result == winbio.WINBIO_E_BAD_CAPTURE:
                print("Bad capture. Please try again...")
            else:
                print("Capture failed with error:", result)
                return False
        
        result = session.enroll_commit(unit_id)
        if result == winbio.ERROR_SUCCESS:
            print("Enrollment completed successfully.")
            return True
        else:
            print("Enrollment failed with error:", result)
            return False
    
    except Exception as e:
        print("Error during enrollment:", e)
        return False

def verify_fingerprint():
    try:
        session = winbio.open_session(winbio.WINBIO_TYPE_FINGERPRINT)
        print("Place your finger on the sensor for verification...")
        result, unit_id, reject_detail = session.capture_sample(winbio.WINBIO_NO_PURPOSE_AVAILABLE)
        if result != winbio.ERROR_SUCCESS:
            print("Capture failed with error:", result)
            return False
        
        result, identity = session.identify(winbio.WINBIO_SUBTYPE_ANY)
        if result == winbio.ERROR_SUCCESS:
            print("Fingerprint matched with identity:", identity)
            return True
        elif result == winbio.WINBIO_E_NO_MATCH:
            print("Fingerprint does not match.")
            return False
        else:
            print("Identification failed with error:", result)
            return False
    
    except Exception as e:
        print("Error during verification:", e)
        return False

# Print the current directory
print("Current directory:", os.getcwd())

# Example usage:
# Enroll fingerprint
enroll_fingerprint()

# Verify fingerprint
verify_fingerprint()
