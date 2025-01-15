import os
import csv

# Mapping of month names to month numbers
month_mapping = {
    "January": 1,
    "February": 2,
    "March": 3,
    "April": 4,
    "May": 5,
    "June": 6,
    "July": 7,
    "August": 8,
    "September": 9,
    "October": 10,
    "November": 11,
    "December": 12
}

def read_csv_files(directory):
    data = {}
    stations = set()  # Initialize the set for stations
    
    # Check if the directory exists
    if not os.path.isdir(directory):
        print(f"Directory {directory} does not exist.")
        return None, None
    
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            file_path = os.path.join(directory, filename)
            
            with open(file_path, 'r') as file:
                reader = csv.reader(file)
                header = next(reader)  # First row contains the month names
                
                # Skip the first 4 columns (stn ID, latitude, longitude, and an extra column)
                months = header[4:]
                
                # Read each row, which corresponds to a weather station
                for row in reader:
                    station_id = row[0]  # Assuming the first column is station ID
                    temperatures = row[4:]  # Temperatures start at column index 4
                    
                    # Ensure data entry for the station, including a dictionary for each month
                    if station_id not in data:
                        data[station_id] = {month_mapping[month.strip().title()]: [] for month in months}
                    
                    for month, temp in zip(months, temperatures):
                        try:
                            # Clean and standardize the month name to match the month_mapping
                            month = month.strip().title()  # Strip spaces and ensure title case
                            
                            # Only process valid numeric temperatures
                            if temp.strip():
                                temperature = float(temp)
                                # Map month name to month number and store the temperature
                                if month in month_mapping:
                                    month_number = month_mapping[month]
                                    data[station_id][month_number].append(temperature)
                        except ValueError:
                            print(f"Skipping invalid temperature data for {station_id}, month {month}: {temp}")
                            continue
                        except KeyError:
                            print(f"Invalid month name found in data for {station_id}: {month}")
                            continue
                
                stations.add(station_id)
    
    return data, stations

def main():
    # Directory where temperature CSV data is stored
    directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temperature_data')
    
    print("Starting the program...")
    print(f"Looking for temperature data in: {directory}")
    
    # Read the data from CSV files in the directory
    data, stations = read_csv_files(directory)
    
    if not data:
        print("No data found or processed. Exiting program.")
        return
    
    print("Finished reading data and found the following stations:")
    print(stations)
    
    # Initialize variables for finding the stations with the largest range, warmest, and coolest temperatures
    largest_range = float('-inf')
    largest_temp_range_station = None
    warmest_temp = float('-inf')
    coolest_temp = float('inf')
    warmest_stations = []
    coolest_stations = []

    # Compute the average temperature for each station and track the largest range
    for station, months_data in data.items():
        all_temps = []
        for month, temps in months_data.items():
            if temps:
                average_temp = sum(temps) / len(temps)
                all_temps.extend(temps)
                
                # Track largest temperature range station
                temp_range = max(temps) - min(temps)
                if temp_range > largest_range:
                    largest_range = temp_range
                    largest_temp_range_station = station
                
                # Track warmest and coolest stations
                if average_temp > warmest_temp:
                    warmest_temp = average_temp
                    warmest_stations = [station]
                elif average_temp == warmest_temp:
                    warmest_stations.append(station)
                
                if average_temp < coolest_temp:
                    coolest_temp = average_temp
                    coolest_stations = [station]
                elif average_temp == coolest_temp:
                    coolest_stations.append(station)

    # Get the current working directory where the Python file is located
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # File paths for saving the results in the same directory as the Python script
    largest_temp_range_file = os.path.join(current_directory, 'largest_temp_range_station.txt')
    warmest_and_coolest_file = os.path.join(current_directory, 'warmest_and_coolest_station.txt')
    average_temp_file = os.path.join(current_directory, 'average_temp.txt')

    # Save the average temperatures to 'average_temp.txt'
    with open(average_temp_file, 'w') as f:
        for station, months_data in data.items():
            f.write(f"Data for station {station}:\n")
            for month, temps in months_data.items():
                if temps:
                    average_temp = sum(temps) / len(temps)
                    f.write(f"  Month {month}: Average Temperature = {average_temp:.2f}\n")
                else:
                    f.write(f"  Month {month}: No data available\n")
    
    print("Average temperatures have been saved to 'average_temp.txt'.")

    # Save the largest temperature range station data
    with open(largest_temp_range_file, 'w') as f:
        f.write(f"Station with largest temperature range: {largest_temp_range_station}\n")
        f.write(f"Temperature range: {largest_range:.2f}°C\n")
    
    print("Largest temperature range station has been saved to 'largest_temp_range_station.txt'.")

    # Save the warmest and coolest station data
    with open(warmest_and_coolest_file, 'w') as f:
        f.write(f"Warmest station(s): {', '.join(warmest_stations)} with {warmest_temp:.2f}°C\n")
        f.write(f"Coolest station(s): {', '.join(coolest_stations)} with {coolest_temp:.2f}°C\n")
    
    print("Warmest and coolest station data has been saved to 'warmest_and_coolest_station.txt'.")

if __name__ == '__main__':
    main()
