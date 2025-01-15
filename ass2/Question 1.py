import os

def encrypt_char(c, n, m):
    """Encrypts a character using a simple shift cipher."""
    shift = (n * m) % 26  
    if 'a' <= c <= 'z':  
        return chr(((ord(c) - ord('a') + shift) % 26) + ord('a'))
    elif 'A' <= c <= 'Z':  
        return chr(((ord(c) - ord('A') + shift) % 26) + ord('A'))
    else:
        return c  

def decrypt_char(c, n, m):
    """Decrypts a character by reversing the shift."""
    shift = (n * m) % 26  
    if 'a' <= c <= 'z':  
        return chr(((ord(c) - ord('a') - shift + 26) % 26) + ord('a'))
    elif 'A' <= c <= 'Z':  
        return chr(((ord(c) - ord('A') - shift + 26) % 26) + ord('A'))
    else:
        return c  

def main():
    """Reads a file, encrypts its content, then decrypts it."""
    script_dir = os.path.dirname(os.path.realpath(__file__))
    raw_text_path = os.path.join(script_dir, "raw_text.txt")
    encrypted_text_path = os.path.join(script_dir, "encrypted_text.txt")

    # Create a sample file if it doesn't exist
    if not os.path.exists(raw_text_path):
        with open(raw_text_path, "w", encoding="utf-8") as file:
            file.write("Hello, World! This is a test.")

    # Read the original text
    try:
        with open(raw_text_path, "r", encoding="utf-8") as file:
            raw_text = file.read()
    except FileNotFoundError:
        print(f"File not found: {raw_text_path}")
        return

    # Get user input
    try:
        n = int(input("Enter a value for n: "))
        m = int(input("Enter a value for m: "))
    except ValueError:
        print("Please enter valid numbers for n and m.")
        return

    # Encrypt the text
    encrypted_text = ''.join(encrypt_char(c, n, m) for c in raw_text)

    # Save the encrypted text
    with open(encrypted_text_path, "w", encoding="utf-8") as file:
        file.write(encrypted_text)

    # Decrypt the text
    decrypted_text = ''.join(decrypt_char(c, n, m) for c in encrypted_text)

    # Show results
    print("\nOriginal Text:\n", raw_text)
    print("\nEncrypted Text:\n", encrypted_text)
    print("\nDecrypted Text:\n", decrypted_text)

    # Verify if the decryption worked
    if raw_text == decrypted_text:
        print("\nDecryption successful. The original text was restored.")
    else:
        print("\nDecryption failed. The text doesn't match the original.")

if __name__ == "__main__":
    main()
