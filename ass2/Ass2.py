# Question 1
def encrypt(text, n, m):
    encrypted_text = []
    for char in text:
        if char.islower():
            if 'a' <= char <= 'm':
                encrypted_char = chr(((ord(char) - ord('a') + n * m) % 26) + ord('a'))
            else:
                encrypted_char = chr(((ord(char) - ord('n') - (n + m)) % 26) + ord('n'))
        elif char.isupper():
            if 'A' <= char <= 'M':
                encrypted_char = chr(((ord(char) - ord('A') - n) % 26) + ord('A'))
            else:
                encrypted_char = chr(((ord(char) - ord('N') + m ** 2) % 26) + ord('N'))
        else:
            encrypted_char = char  # Keep special characters unchanged
        encrypted_text.append(encrypted_char)
    return ''.join(encrypted_text)

def decrypt(encrypted_text, n, m):
    decrypted_text = []
    for char in encrypted_text:
        if char.islower():
            if 'a' <= char <= 'm':
                decrypted_char = chr(((ord(char) - ord('a') - n * m) % 26) + ord('a'))
            else:
                decrypted_char = chr(((ord(char) - ord('n') + (n + m)) % 26) + ord('n'))
        elif char.isupper():
            if 'A' <= char <= 'M':
                decrypted_char = chr(((ord(char) - ord('A') + n) % 26) + ord('A'))
            else:
                decrypted_char = chr(((ord(char) - ord('N') - m ** 2) % 26) + ord('N'))
        else:
            decrypted_char = char  # Keep special characters unchanged
        decrypted_text.append(decrypted_char)
    return ''.join(decrypted_text)

def check_correctness(original, decrypted):
    return original == decrypted

def main_question_1():
    # Reading the raw text file
    with open('raw_text.txt', 'r') as file:
        text = file.read()

    # Getting user inputs
    n = int(input("Enter value of n: "))
    m = int(input("Enter value of m: "))

    # Encrypting text
    encrypted_text = encrypt(text, n, m)

    # Writing encrypted text -> file
    with open('encrypted_text.txt', 'w') as file:
        file.write(encrypted_text)

    # Decrypting the text
    decrypted_text = decrypt(encrypted_text, n, m)

    # Checking if decryption is correct
    if check_correctness(text, decrypted_text):
        print("Decryption is successful and correct!")
    else:
        print("Decryption failed!")

# Question 2:
import os
import csv

def calculate_average_temp(directory):
    month_temps = {i: [] for i in range(1, 13)}  # To store temperatures for each month
    stations_temp_range = {}
    warmest_station = None
    coolest_station = None

    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            with open(os.path.join(directory, filename), 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip the header
                for row in reader:
                    station, date, temp = row[0], row[1], float(row[2])
                    month = int(date.split('-')[1])
                    month_temps[month].append(temp)

                    if station not in stations_temp_range:
                        stations_temp_range[station] = []
                    stations_temp_range[station].append(temp)

    # Calculate monthly averages
    monthly_averages = {month: sum(temps) / len(temps) for month, temps in month_temps.items()}

    # Find the station with the largest temperature range
    largest_range_station = None
    largest_range = -float('inf')
    for station, temps in stations_temp_range.items():
        temp_range = max(temps) - min(temps)
        if temp_range > largest_range:
            largest_range = temp_range
            largest_range_station = station

    # Find the warmest and coolest stations
    for station, temps in stations_temp_range.items():
        avg_temp = sum(temps) / len(temps)
        if warmest_station is None or avg_temp > sum(warmest_station[1]) / len(warmest_station[1]):
            warmest_station = (station, temps)
        if coolest_station is None or avg_temp < sum(coolest_station[1]) / len(coolest_station[1]):
            coolest_station = (station, temps)

    # Writing results to files
    with open('average_temp.txt', 'w') as file:
        for month, avg_temp in monthly_averages.items():
            file.write(f'Month {month}: {avg_temp:.2f}\n')

    with open('largest_temp_range_station.txt', 'w') as file:
        file.write(f'Station with largest temperature range: {largest_range_station}\n')

    with open('warmest_and_coolest_station.txt', 'w') as file:
        file.write(f'Warmest station: {warmest_station[0]}\n')
        file.write(f'Coolest station: {coolest_station[0]}\n')

# Question 3:
import turtle

def draw_tree(t, branch_length, angle_left, angle_right, depth, reduction_factor):
    if depth == 0:
        return
    else:
        t.forward(branch_length)
        t.left(angle_left)
        draw_tree(t, branch_length * reduction_factor, angle_left, angle_right, depth - 1, reduction_factor)
        t.right(angle_left + angle_right)
        draw_tree(t, branch_length * reduction_factor, angle_left, angle_right, depth - 1, reduction_factor)
        t.left(angle_right)
        t.backward(branch_length)

def main_question_3():
    angle_left = float(input("Enter the left branch angle: "))
    angle_right = float(input("Enter the right branch angle: "))
    start_length = float(input("Enter the starting branch length: "))
    depth = int(input("Enter the recursion depth: "))
    reduction_factor = float(input("Enter the branch length reduction factor (0 < x < 1): "))

    screen = turtle.Screen()
    screen.bgcolor("white")
    t = turtle.Turtle()
    t.left(90)  # Initial direction of the tree

    draw_tree(t, start_length, angle_left, angle_right, depth, reduction_factor)

    turtle.done()

# Main execution
if __name__ == "__main__":
    # Call the functions for each question
    print("Starting Question 1: Encryption and Decryption")
    main_question_1()

    print("\nStarting Question 2: Temperature Analysis")
    calculate_average_temp('temperature_data')  # Changed folder path to 'temperature_data'

    print("\nStarting Question 3: Recursive Tree with Turtle Graphics")
    main_question_3()
