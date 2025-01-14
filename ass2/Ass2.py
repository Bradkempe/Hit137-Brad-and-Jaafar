import os

# Helper function to convert a character to a number between 0-51
def char_to_num(c):
    if 'a' <= c <= 'z':  # Lowercase letters
        return ord(c) - ord('a')
    elif 'A' <= c <= 'Z':  # Uppercase letters
        return ord(c) - ord('A') + 26
    return -1  # Non-alphabet characters

# Helper function to convert a number back to a character
def num_to_char(num):
    if 0 <= num <= 25:  # Lowercase letters
        return chr(num + ord('a'))
    elif 26 <= num <= 51:  # Uppercase letters
        return chr(num - 26 + ord('A'))
    return chr(num)  # Non-alphabet characters (if any)

# Function to encrypt text
def encrypt_text(text, n, m):
    encrypted_text = []

    for char in text:
        num = char_to_num(char)

        if num == -1:
            encrypted_text.append(char)  # Non-alphabet characters remain unchanged
        else:
            # Encrypt based on the character's number and predefined ranges
            if 0 <= num <= 12:  # Lowercase a-m shifted forward by n * m
                num = (num + (n * m)) % 26  # Wrap around if it exceeds 'z'
            elif 13 <= num <= 25:  # Lowercase n-z shifted backward by n + m
                num = (num - (n + m)) % 26  # Wrap around if it goes below 'a'
            elif 26 <= num <= 38:  # Uppercase A-M shifted forward by n
                num = (num + n) % 26 + 26  # Wrap around if it exceeds 'Z'
            elif 39 <= num <= 51:  # Uppercase N-Z shifted forward by m^2
                num = (num + (m ** 2)) % 26 + 26  # Wrap around if it exceeds 'Z'

            encrypted_text.append(num_to_char(num))

    return ''.join(encrypted_text)

# Function to decrypt text
def decrypt_text(encrypted_text, n, m):
    decrypted_text = []

    for char in encrypted_text:
        num = char_to_num(char)

        if num == -1:
            decrypted_text.append(char)  # Non-alphabet characters remain unchanged
        else:
            # Decrypt based on the character's number and predefined ranges
            if 0 <= num <= 12:  # Lowercase a-m shifted forward by n * m
                # Reverse the shift applied to a-m range (move backward by (n * m))
                num = (num - (n * m)) % 26  # Wrap around if it goes below 'a'
                if num < 0:
                    num += 26  # Ensure non-negative values
            elif 13 <= num <= 25:  # Lowercase n-z shifted backward by n + m
                # Reverse the shift applied to n-z range (move forward by (n + m))
                num = (num + (n + m)) % 26  # Wrap around if it exceeds 'z'
            elif 26 <= num <= 38:  # Uppercase A-M shifted forward by n
                # Reverse the shift applied to A-M range (move backward by n)
                num = (num - n) % 26 + 26  # Wrap around if it goes below 'A'
            elif 39 <= num <= 51:  # Uppercase N-Z shifted forward by m^2
                # Reverse the shift applied to N-Z range (move backward by m^2)
                num = (num - (m ** 2)) % 26 + 26  # Wrap around if it goes below 'A'

            decrypted_text.append(num_to_char(num))

    return ''.join(decrypted_text)

def main():
    # Get the directory where the .py file is located
    script_directory = os.path.dirname(os.path.abspath(__file__))
    raw_text_file_path = os.path.join(script_directory, 'raw_text.txt')

    # Check if the file exists in the same directory as the script
    if not os.path.exists(raw_text_file_path):
        print(f"Error: 'raw_text.txt' file not found in {script_directory}!")
        return

    # Open the raw text file
    with open(raw_text_file_path, 'r') as file:
        raw_text = file.read()

    print("Found 'raw_text.txt' at:", raw_text_file_path)

    # Display the original text
    print("Original Text:\n", raw_text)

    # Get the encryption parameters from the user
    n = int(input("Enter value of n: "))
    m = int(input("Enter value of m: "))

    # Encrypt the text
    encrypted_text = encrypt_text(raw_text, n, m)
    print("\nEncrypted Text:\n", encrypted_text)

    # Save encrypted text to a new file
    with open('encrypted_text.txt', 'w') as encrypted_file:
        encrypted_file.write(encrypted_text)
    print("\nEncrypted text saved to 'encrypted_text.txt'")

    # Decrypt the text
    decrypted_text = decrypt_text(encrypted_text, n, m)
    print("\nDecrypted Text:\n", decrypted_text)

    # Check for discrepancies in decryption
    discrepancies = 0
    for i in range(min(len(raw_text), len(decrypted_text))):
        if raw_text[i] != decrypted_text[i]:
            discrepancies += 1
            print(f"Discrepancy at index {i}: Expected '{raw_text[i]}', but got '{decrypted_text[i]}'")

    if discrepancies == 0:
        print("\nDecryption successful, no discrepancies found!")
    else:
        print(f"\nDecryption failed with {discrepancies} discrepancies.")

# Run the main function
if __name__ == "__main__":
    main()
