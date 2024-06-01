import json

# Function to read the data from a text file
def read_data_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = file.readlines()
    return [line.strip() for line in data if line.strip()]

# Function to parse the data into key-value pairs
def parse_data(data):
    parsed_data = []
    for line in data:
        if 'payment' in line.lower() or 'fee' in line.lower() or 'tuition' in line.lower() or 'student' in line.lower():
            parts = line.split('-')
            if len(parts) == 2:
                category = parts[0].strip()
                description = parts[1].strip()
            else:
                category = "General"
                description = line.strip()
            parsed_data.append({
                "category": category,
                "description": description
            })
        else:
            parsed_data.append({
                "category": "General",
                "description": line.strip()
            })
    return parsed_data

# Function to save parsed data to a JSON file
def save_to_json(parsed_data, output_file):
    json_data = json.dumps(parsed_data, indent=4)
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(json_data)
        print(f"Filtered data saved to '{output_file}'")
    except IOError as e:
        print(f"File write failed: {e}")

# Main function to execute the process
def main(input_file, output_file):
    data = read_data_from_file(input_file)
    parsed_data = parse_data(data)
    save_to_json(parsed_data, output_file)

# Execute the main function with the appropriate file paths
input_file = 'filtered_new_students_payment_data.txt'  # Replace with your actual input file path
output_file = 'new_students_payment_data.json'
main(input_file, output_file)
