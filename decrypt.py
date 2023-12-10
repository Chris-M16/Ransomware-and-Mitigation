from cryptography.fernet import Fernet
import os

# Load the symmetric key from file
with open("smem-enc", "rb") as key_file:
    symmetric_key = key_file.read()

# Creates a Fernet cipher with the key
cipher = Fernet(symmetric_key)

# Define the directory being decrypted
directory_to_decrypt = "/home/chris/Documents"

# Loop through each encrypted file in the directory and decrypt the contents of the file and create a new file
for filename in os.listdir(directory_to_decrypt):
    filepath = os.path.join(directory_to_decrypt, filename)

    # Check if it's an encrypted file
    if os.path.isfile(filepath) and filename.endswith(".pp"):
        # Read the contents of the encrypted files
        with open(filepath, "rb") as file:
            ciphertext = file.read()

        # Decrypt the file content
        plaintext = cipher.decrypt(ciphertext)

        # Create a new filename without the ".pp" extension
        decrypted_filename = os.path.splitext(filename)[0]
        decrypted_filepath = os.path.join(directory_to_decrypt, decrypted_filename)

        # Write the decrypted content to the new file
        with open(decrypted_filepath, "wb") as decrypted_file:
            decrypted_file.write(plaintext)

        # Delete the original encrypted file
        os.remove(filepath)

print("Decryption completed.")
