# Function to encrypt the given text using the parameters n and m
def encrypt_text(text, n, m):
    encrypted = ""
    for char in text:
        if 'a' <= char <= 'm':  # For lowercase letters in the first half of the alphabet
            encrypted += chr((ord(char) - ord('a') + n * m) % 26 + ord('a'))
        elif 'n' <= char <= 'z':  # For lowercase letters in the second half of the alphabet
            encrypted += chr((ord(char) - ord('a') - (n + m)) % 26 + ord('a'))
        elif 'A' <= char <= 'M':  # For uppercase letters in the first half of the alphabet
            encrypted += chr((ord(char) - ord('A') - n) % 26 + ord('A'))
        elif 'N' <= char <= 'Z':  # For uppercase letters in the second half of the alphabet
            encrypted += chr((ord(char) - ord('A') + m**2) % 26 + ord('A'))
        else:  # Keep non-alphabetic characters unchanged
            encrypted += char
    return encrypted

# Function to decrypt the given text using the same parameters n and m
def decrypt_text(text, n, m):
    decrypted = ""
    for char in text:
        if 'a' <= char <= 'm':  # First half of lowercase letters
            decrypted += chr((ord(char) - ord('a') - n * m) % 26 + ord('a'))
        elif 'n' <= char <= 'z':  # Second half of lowercase letters
            decrypted += chr((ord(char) - ord('a') + (n + m)) % 26 + ord('a'))
        elif 'A' <= char <= 'M':  # First half of uppercase letters
            decrypted += chr((ord(char) - ord('A') + n) % 26 + ord('A'))
        elif 'N' <= char <= 'Z':  # Second half of uppercase letters
            decrypted += chr((ord(char) - ord('A') - m**2) % 26 + ord('A'))
        else:  # Keep non-alphabetic characters unchanged
            decrypted += char
    return decrypted

# Function to verify if the decrypted text matches the original text
def verify_decryption(original, decrypted):
    return original == decrypted

# Main execution logic
if __name__ == "__main__":
    print("Welcome to the Text Encryptor and Decryptor! Let's get started.")

    # Prompt the user for the encryption parameters
    try:
        n = int(input("Please enter the first number (n): "))
        m = int(input("Please enter the second number (m): "))
    except ValueError:
        print("Oops! It looks like you didn't enter valid numbers. Please try again.")
        exit(1)

    # Try to read the input text from a file
    try:
        print("Reading the input text from 'raw_text.txt'...")
        with open("raw_text.txt", "r", encoding="utf-8") as file:
            raw_text = file.read()
    except FileNotFoundError:
        print("Error: We couldn't find 'raw_text.txt'. Please make sure the file is in the same folder.")
        exit(1)

    # Encrypt the text
    encrypted_text = encrypt_text(raw_text, n, m)
    print("\nThe text has been encrypted successfully! The encrypted text is now saved to 'encrypted_text.txt'.")
    with open("encrypted_text.txt", "w", encoding="utf-8") as file:
        file.write(encrypted_text)

    # Now, let's decrypt the text and check if it matches the original
    decrypted_text = decrypt_text(encrypted_text, n, m)
    if verify_decryption(raw_text, decrypted_text):
        print("\nSuccess! The decryption was successful and the text matches the original.")
    else:
        print("\nOops! Something went wrong with the decryption. The text doesn't match.")

    # Show the decrypted text to the user
    print("\nHere is the decrypted text:")
    print(decrypted_text)