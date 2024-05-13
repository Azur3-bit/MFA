import psutil

def is_removable_disk(path):
    """Check if the path is on a removable disk."""
    partitions = psutil.disk_partitions()
    for partition in partitions:
        if path.startswith(partition.mountpoint):
            if 'removable' in partition.opts or 'cdrom' in partition.opts:
                return True
    return False

def compare_file_with_key(filename, saved_key):
    try:
        if not is_removable_disk(filename):
            print("File is not on a removable storage device.")
            return False
        
        # Open the file and read its content
        with open(filename, 'r') as file:
            file_content = file.read()
        
        # Compare the file content with the saved key
        if file_content.strip() == saved_key.strip():
            return True
        else:
            return False
    except FileNotFoundError:
        print("File not found!")
        return False
    except Exception as e:
        print("An error occurred:", e)
        return False

# Example usage:
saved_key = "This is the saved key content"  # Pre-saved key content
filename = "/media/username/removable_drive/example.txt"  # Path to the text file on removable storage

# Check if the content of the file matches the saved key
result = compare_file_with_key(filename, saved_key)
print("Content matches saved key:", result)
