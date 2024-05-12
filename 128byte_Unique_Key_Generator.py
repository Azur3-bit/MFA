import secrets
import string
import time

def generate_unique_key(length):
    timestamp = str(int(time.time()))
    alphabet = string.ascii_letters + string.digits
    random_chars = ''.join(secrets.choice(alphabet) for _ in range(length - len(timestamp)))
    
    key = timestamp + random_chars
    return key

key = generate_unique_key(128) 
print(key)
