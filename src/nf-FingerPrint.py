import win32com.client

def enroll_fingerprint():
    try:
        # Create Biometric Enrollment object
        biometric_enrollment = win32com.client.Dispatch("BiometricEnrollment.Enrollment")

        # Start enrollment
        result = biometric_enrollment.StartEnrollment()
        if result != 0:
            print("Failed to start enrollment.")
            return False
        
        # Wait for enrollment to complete
        print("Please place your finger on the sensor for enrollment...")
        while biometric_enrollment.Status != 2:  # EnrollmentStatus_Completed
            pass
        
        print("Enrollment completed successfully.")
        return True
    
    except Exception as e:
        print("Error during enrollment:", e)
        return False

def verify_fingerprint():
    try:
        # Create Biometric Service object
        biometric_service = win32com.client.Dispatch("BiometricAuthentication.BiometricService")

        # Start authentication
        result = biometric_service.StartAuthentication()
        if result != 0:
            print("Failed to start authentication.")
            return False
        
        # Wait for authentication to complete
        print("Please place your finger on the sensor for verification...")
        while biometric_service.Status != 2:  # AuthenticationStatus_Completed
            pass
        
        print("Verification completed successfully.")
        return True
    
    except Exception as e:
        print("Error during verification:", e)
        return False

# Example usage:
# Enroll fingerprint
enroll_fingerprint()

# Verify fingerprint
verify_fingerprint()

