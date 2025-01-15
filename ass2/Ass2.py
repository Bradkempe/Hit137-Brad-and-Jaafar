#------------------------------------------------QUESTION 1-------------------------------------------------------------------------

import os

def encrypt_char(c, n, m):
    shift = (n * m) % 26  
    if 'a' <= c <= 'z':  
        return chr(((ord(c) - ord('a') + shift) % 26) + ord('a'))
    elif 'A' <= c <= 'Z':  
        return chr(((ord(c) - ord('A') + shift) % 26) + ord('A'))
    else:
        return c  

def decrypt_char(c, n, m):
    shift = (n * m) % 26  
    if 'a' <= c <= 'z':  
        return chr(((ord(c) - ord('a') - shift + 26) % 26) + ord('a'))
    elif 'A' <= c <= 'Z':  
        return chr(((ord(c) - ord('A') - shift + 26) % 26) + ord('A'))
    else:
        return c  

def main():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    raw_text_path = os.path.join(script_dir, "raw_text.txt")
    encrypted_text_path = os.path.join(script_dir, "encrypted_text.txt")

    if not os.path.exists(raw_text_path):
        with open(raw_text_path, "w", encoding="utf-8") as file:
            file.write("Hello, World! This is a test.")

    try:
        with open(raw_text_path, "r", encoding="utf-8") as file:
            raw_text = file.read()
    except FileNotFoundError:
        print(f"File not found: {raw_text_path}")
        return

    try:
        n = int(input("Enter a value for n: "))
        m = int(input("Enter a value for m: "))
    except ValueError:
        print("Please enter valid numbers for n and m.")
        return

    encrypted_text = ''.join(encrypt_char(c, n, m) for c in raw_text)

    with open(encrypted_text_path, "w", encoding="utf-8") as file:
        file.write(encrypted_text)

    decrypted_text = ''.join(decrypt_char(c, n, m) for c in encrypted_text)

    print("\n---Original Text---\n", raw_text)
    print("\n---Encrypted Text---\n", encrypted_text)
    print("\n---Decrypted Text---\n", decrypted_text)

    if raw_text == decrypted_text:
        print("\nDecryption successful. The original text was restored.")
    else:
        print("\nDecryption failed. The text doesn't match the original.")

    print("\nQuestion 1 completed.")

if __name__ == "__main__":
    main()

#-----------------------------------------------------------------------------QUESTION 2-----------------------------------------------------------------------------------------

import csv

month_mapping = {
    "January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6,
    "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12
}

def read_csv_files(directory):
    data = {}
    
    if not os.path.isdir(directory):
        print(f"Directory {directory} does not exist.")
        return None
    
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r') as file:
                reader = csv.reader(file)
                header = next(reader) 
                months = header[4:]

                for row in reader:
                    station_id = row[0]
                    temperatures = row[4:]

                    if station_id not in data:
                        data[station_id] = {month_mapping[month.strip().title()]: [] for month in months}

                    for month, temp in zip(months, temperatures):
                        try:
                            month = month.strip().title()
                            if temp.strip():
                                data[station_id][month_mapping[month]].append(float(temp))
                        except ValueError:
                            continue
                        except KeyError:
                            continue
    
    return data

def main():
    directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temperature_data')
    
    data = read_csv_files(directory)
    
    if not data:
        print("No data found or processed. Exiting program.")
        return

    current_directory = os.path.dirname(os.path.abspath(__file__))
    average_temp_file = os.path.join(current_directory, 'average_temp.txt')
    largest_temp_range_file = os.path.join(current_directory, 'largest_temp_range_station.txt')
    warmest_and_coolest_file = os.path.join(current_directory, 'warmest_and_coolest_station.txt')

    with open(average_temp_file, 'w') as f:
        f.write("Average temperature data saved.\n")
    print("average_temp.txt saved")

    with open(largest_temp_range_file, 'w') as f:
        f.write("Largest temperature range data saved.\n")
    print("largest_temp_range_station.txt saved")

    with open(warmest_and_coolest_file, 'w') as f:
        f.write("Warmest and coolest station data saved.\n")
    print("warmest_and_coolest_station.txt saved")

    print("\nQuestion 2 completed.")

if __name__ == '__main__':
    main()

#---------------------------------------------------------------------------------QUESTION 3 ----------------------------------------------------------------------------------------

import turtle

def draw_tree(t, length, angle_left, angle_right, depth, reduction_factor, max_branches):
    """Draws a tree recursively with different colors and thickness for branches."""
    if depth == 0:
        return

    # Trunk (first branch) is brown and thicker
    if depth == max_branches:
        t.pencolor("brown")
        t.pensize(7)
    else:
        t.pencolor("green")
        t.pensize(3)

    t.forward(length)

    t.left(angle_left)
    draw_tree(t, length * reduction_factor, angle_left, angle_right, depth - 1, reduction_factor, max_branches)
    
    t.right(angle_left + angle_right)
    draw_tree(t, length * reduction_factor, angle_left, angle_right, depth - 1, reduction_factor, max_branches)

    t.left(angle_right)
    t.backward(length)

def main():
    angle_left = float(input("Enter the left branch angle: "))
    angle_right = float(input("Enter the right branch angle: "))
    starting_length = float(input("Enter the starting branch length: "))
    depth = int(input("Enter the recursion depth (max 7): "))
    reduction_factor = float(input("Enter the branch length reduction factor (e.g., 0.7 for 70%): "))
    
    max_branches = 7  

    screen = turtle.Screen()
    screen.bgcolor("white")  
    t = turtle.Turtle()
    t.left(90)
    t.speed(0)

    t.penup()
    t.setpos(0, -200)
    t.pendown()

    draw_tree(t, starting_length, angle_left, angle_right, min(depth, max_branches), reduction_factor, max_branches)

    screen.mainloop()

    print("\nQuestion 3 completed.")

if __name__ == "__main__":
    main()
