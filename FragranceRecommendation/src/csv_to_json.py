import csv
import json


def csv_to_json(csv_file, json_file):
    id_counter = 1
    unique_perfumes = {}

    # Read the CSV file
    with open(csv_file, 'r', encoding='utf-8-sig') as file:
        csv_data = csv.DictReader(file)

        # Transform the CSV data into JSON
        for row in csv_data:
            perfume_name = row['Perfume Name']

            # Skip if the perfume name is empty
            if not perfume_name:
                continue

            note = row['Note']
            if perfume_name not in unique_perfumes:
                # Create a new entry for a unique perfume name
                unique_perfumes[perfume_name] = {
                    'id': id_counter,
                    'perfume': perfume_name,
                    'brand': row['Brand'],
                    'country': row['Country'],
                    'release_year': row['Release Year'],
                    'fragrances': []
                }
                id_counter += 1

            # Append the note to the fragrances list
            unique_perfumes[perfume_name]['fragrances'].append(note)

        # Return the JSON data
        # return json.dumps(list(unique_perfumes.values()), indent=4)

    with open(json_file, 'w') as file:
        json.dump(list(unique_perfumes.values()), file, indent=4)


# Usage example
csv_file = '../data/perfume_data.csv'  # Replace with the actual CSV file path
json_file = '../data/perfume_data.json'  # Replace with the desired output JSON file path
csv_to_json(csv_file, json_file)
