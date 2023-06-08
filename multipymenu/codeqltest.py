import os

def process_file(file_path):
    secret_key = "MySecretKey"

    # Process the file
    with open(file_path, 'r') as file:
        contents = file.read()

    encrypted_data = encrypt(contents, secret_key)


def encrypt(data, key):
    pass

# Main code
file_path = input("Enter file path: ")
process_file(file_path)
