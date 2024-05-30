import secrets
import string

def generate_alphanumeric_key(length):
    alphabet = string.ascii_letters + string.digits
    key = ''.join(secrets.choice(alphabet) for _ in range(length))
    return key
key = generate_alphanumeric_key(16)  
print( key)
