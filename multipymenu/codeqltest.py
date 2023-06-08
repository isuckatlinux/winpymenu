def check_password(password):
    hardcoded_password = "MySecretPassword"

    if password == hardcoded_password:
        return True
    else:
        return False

# Test the check_password function
user_input = input("Enter a password: ")
if check_password(user_input):
    print("Access granted!")
else:
    print("Access denied!")
