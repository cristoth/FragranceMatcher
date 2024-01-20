import csv


def create_unique_fragrances_csv(input_file, output_file):
    fragrances = set()  # keep track of unique fragrances
    unique_fragrances = []  # store unique fragrances along with their IDs

    # Read the input CSV file and extract unique fragrance names
    with open(input_file, 'r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            fragrances.update(row['Note'].split(','))

    # Generate unique IDs for each fragrance
    id = 1
    for fragrance in fragrances:
        unique_fragrances.append({"id": "(" + str(id), "name": "'" + fragrance + "')"})
        id += 1

    # Write the unique fragrances and IDs to a new CSV file
    with open(output_file, 'w', newline='', encoding='utf-8-sig') as file:
        fieldnames = ['id', 'name']
        writer = csv.DictWriter(file, fieldnames=fieldnames, lineterminator=',\n')
        writer.writeheader()
        writer.writerows(unique_fragrances)


# Example usage
create_unique_fragrances_csv('../data/perfume_data.csv', '../data/fragrances.csv')
