import json

def convert_to_json(data_string):
    lines = data_string.strip().split('\n')
    header = lines[0].split(',')
    entries = []
    
    for line in lines[1:]:
        values = line.split(',')
        entry = {}
        for i, h in enumerate(header):
            # Cleanup the header and values
            clean_header = h.strip().lower().replace('/', '_').replace(' ', '_')
            entry[clean_header] = values[i].strip()
        entries.append(entry)
    
    return entries

def main():
    all_data = {}
    
    for year in range(1970, 2023):
        print(f"Enter data for {year}. When done, enter 'END' on a new line.")
        
        # Collect the data
        lines = []
        while True:
            line = input()
            if line == 'END':
                break
            lines.append(line)
        
        # Convert the collected data to JSON format
        year_data = convert_to_json("\n".join(lines))
        all_data[year] = year_data
    
    # Output the combined data to a file
    with open("combined_data.json", "w") as out_file:
        json.dump(all_data, out_file, indent=4)
    print("Data saved to 'combined_data.json'.")

if __name__ == "__main__":
    main()
