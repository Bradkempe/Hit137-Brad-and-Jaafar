def encrypt(text, n, m):
    encrypted_text = []

    for char in text:
        if 'a' <= char <= 'm':  # For lowercase first half
            shift = n * m
            encrypted_text.append(chr(((ord(char) - ord('a') + shift) % 26) + ord('a')))
        elif 'n' <= char <= 'z':  # For lowercase second half
            shift = -(n + m)
            encrypted_text.append(chr(((ord(char) - ord('a') + shift) % 26) + ord('a')))
        elif 'A' <= char <= 'M':  # For uppercase first half
            shift = -n
            encrypted_text.append(chr(((ord(char) - ord('A') + shift) % 26) + ord('A')))
        elif 'N' <= char <= 'Z':  # For uppercase second half
            shift = m * m
            encrypted_text.append(chr(((ord(char) - ord('A') + shift) % 26) + ord('A')))
        else:
            encrypted_text.append(char)  # non-alphabet characters remain unchanged
    
    return ''.join(encrypted_text)


def decrypt(text, n, m):
    decrypted_text = []

    for char in text:
        if 'a' <= char <= 'm':  # For lowercase first half
            shift = -(n * m)
            decrypted_text.append(chr(((ord(char) - ord('a') + shift) % 26) + ord('a')))
        elif 'n' <= char <= 'z':  # For lowercase second half
            shift = n + m
            decrypted_text.append(chr(((ord(char) - ord('a') + shift) % 26) + ord('a')))
        elif 'A' <= char <= 'M':  # For uppercase first half
            shift = n
            decrypted_text.append(chr(((ord(char) - ord('A') + shift) % 26) + ord('A')))
        elif 'N' <= char <= 'Z':  # for uppercase second half
            shift = -(m * m)
            decrypted_text.append(chr(((ord(char) - ord('A') + shift) % 26) + ord('A')))
        else:
            decrypted_text.append(char)  # non-alphabet characters remain unchanged
    
    return ''.join(decrypted_text)


def check_correctness(original, decrypted):
    return original == decrypted


def main():
    # Taking The user input
    n = int(input("Enter the value of n: "))
    m = int(input("Enter the value of m: "))

    # This read the raw text file
    with open("raw_text.txt", "r") as f:
        raw_text = f.read()

    # Encrypt the text
    encrypted_text = encrypt(raw_text, n, m)

    # Write the encrypted text to new file
    with open("encrypted_text.txt", "w") as f:
        f.write(encrypted_text)

    # Try decrypt the encrypted text to check correctness
    decrypted_text = decrypt(encrypted_text, n, m)

    # Check if the decrypted text matches the original raw text
    if check_correctness(raw_text, decrypted_text):
        print("Decryption successful: The decrypted text has matched the original text.")
    else:
        print("Decryption failed: The decrypted text has not matched the original text.")

if __name__ == "__main__":
    main()
    
